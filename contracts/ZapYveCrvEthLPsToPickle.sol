// SPDX-License-Identifier: AGPL-3.0
pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

import {Math} from "@openzeppelin/contracts/math/Math.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {SafeERC20, SafeMath, IERC20, Address} from "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";
import {SignedSafeMath} from "@openzeppelin/contracts/math/SignedSafeMath.sol";

import {IUniswapV2Router02} from "../interfaces/uniswap/IUniswapV2Router02.sol";
import {IUniswapV2Pair} from "../interfaces/uniswap/IUniswapV2Pair.sol";
import {IveCurveVault} from "../interfaces/yearn/IveCurveVault.sol";
import {IPickleJar} from "../interfaces/pickle/IPickleJar.sol";
import {IPickleStake} from "../interfaces/pickle/IPickleStake.sol";

// import "@uniswap/lib/contracts/libraries/Babylonian.sol";
library Babylonian {
    function sqrt(int256 y) internal pure returns (int256 z) {
        if (y > 3) {
            z = y;
            int256 x = y / 2 + 1;
            while (x < z) {
                z = x;
                x = (y / x + x) / 2;
            }
        } else if (y != 0) {
            z = 1;
        }
    }
}

contract ZapYveCrvEthLPsToPickle is Ownable {
    using SafeERC20 for IERC20;
    using Address for address;
    using SafeMath for uint256;
    using SignedSafeMath for int256;

    // Tokens
    address public constant ethYveCrv = 0x10B47177E92Ef9D5C6059055d92DdF6290848991; // LP Token
    address public constant yveCrv = 0xc5bDdf9843308380375a611c18B50Fb9341f502A;
    address public constant crv = 0xD533a949740bb3306d119CC777fa900bA034cd52;
    address public constant weth = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    IPickleJar public pickleJar = IPickleJar(0x5Eff6d166D66BacBC1BF52E2C54dD391AE6b1f48);
    IPickleStake public pickleStake = IPickleStake(0xbD17B1ce622d73bD438b9E658acA5996dc394b0d);
    IveCurveVault public yVault = IveCurveVault(yveCrv);

    // DEXes
    address public activeDex = 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F; // Sushi default
    address public sushiswapRouter = 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F;
    address public uniswapRouter = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    IUniswapV2Router02 public swapRouter;
    
    // ETH/CRV pair we want to swap with
    address public swapPair = 0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009; // Initialize with Sushiswap
    address public sushiswapPair = 0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009;
    address public uniswapPair = 0x3dA1313aE46132A397D90d95B1424A9A7e3e0fCE;
    
    // Dex swap paths
    address[] public swapEthPath;
    address[] public swapCrvPath;
    address[] public swapForYveCrvPath;

    // Misc
    address payable public governance = 0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52;

    modifier onlyGovernance() {
        require(msg.sender == governance, "!authorized");
        _;
    }

    constructor() public Ownable() {
        // Initialize with Sushiswap
        swapRouter = IUniswapV2Router02(activeDex);

        // Setup some initial approvals
        IERC20(crv).safeApprove(activeDex, uint256(-1)); // For curve swaps on dex
        IERC20(crv).safeApprove(yveCrv, uint256(-1));// approve vault to take curve
        IERC20(yveCrv).safeApprove(sushiswapRouter, uint256(-1));
        IERC20(ethYveCrv).safeApprove(address(pickleJar), uint256(-1)); // For staking into pickle jar

        swapEthPath = new address[](2);
        swapEthPath[0] = weth;
        swapEthPath[1] = crv;

        swapCrvPath = new address[](2);
        swapCrvPath[0] = crv;
        swapCrvPath[1] = weth;

        swapForYveCrvPath = new address[](2);
        swapForYveCrvPath[0] = weth;
        swapForYveCrvPath[1] = yveCrv;
    }

    function setGovernance(address payable _governance) external onlyGovernance {
        governance = _governance;
    }

    /*  ETH Zap  */
    function zapInETH() external payable {
        _zapIn(true, msg.value);
    }

    /*  CRV Zap  (denominated in wei) */
    function zapInCRV(uint256 crvAmount) external {
        require(crvAmount != 0, "0 CRV");
        IERC20(crv).transferFrom(msg.sender, address(this), crvAmount);
        _zapIn(false, IERC20(crv).balanceOf(address(this))); // Include any dust from prev txns
    }

    function _zapIn(bool _isEth, uint256 _haveAmount) internal returns (uint256) {
        IUniswapV2Pair lpPair = IUniswapV2Pair(ethYveCrv); // Pair we LP against
        (uint112 lpReserveA, uint112 lpReserveB, ) = lpPair.getReserves();

        //  Check if it's worthwhile to use the Yearn yveCRV vault
        bool useVault = shouldUseVault(lpReserveA, lpReserveB);  
        if(useVault){
            // Calculate swap amount
            uint256 amountToSwap = calculateSwapAmount(_isEth, _haveAmount);
            _tokenSwap(_isEth, amountToSwap);
            yVault.depositAll();
        }
        else if(!_isEth){
            // User sent CRV: Must convert all CRV to ETH first
            IUniswapV2Router02(sushiswapRouter).swapExactTokensForETH(_haveAmount, 0, swapCrvPath, address(this), now);
        }
        if(!useVault){
            // We can assume we have a full ETH balance now, time to swap for a the right amount of yveCRV for a single-sided deposit
            int256 amountToSell = calculateSingleSided(lpReserveA, address(this).balance);
            swapRouter.swapExactETHForTokens{value: uint256(amountToSell)}(1, swapForYveCrvPath, address(this), now)[swapEthPath.length - 1];
        }
        
        //  Now we should have proper vaules. Time to provide some liquidity.
        IUniswapV2Router02(sushiswapRouter).addLiquidityETH{value: address(this).balance}( 
            yveCrv, yVault.balanceOf(address(this)), 1, 1, address(this), now
        );
       
        //  Deposit LP tokens to Pickle jar and send tokens back to user
        pickleJar.depositAll();
        IERC20(address(pickleJar)).safeTransfer(msg.sender, pickleJar.balanceOf(address(this)));

        // Staking on behalf of user is not possible 
        // uint256 pickleBalance = IERC20(address(pickleJar)).balanceOf(address(this));
        // pickleStake.deposit(26, pickleBalance); // 26 is the Pool ID for ETH/yveCRV SLPs
    }

    function _tokenSwap(bool _isEth, uint256 _amountIn) internal returns (uint256) {
        uint256 amountOut = 0;
        if (_isEth) {
            amountOut = swapRouter.swapExactETHForTokens{value: _amountIn}(1, swapEthPath, address(this), now)[swapEthPath.length - 1];
        } else {
            amountOut = swapRouter.swapExactTokensForETH(_amountIn, 0, swapCrvPath, address(this), now)[swapCrvPath.length - 1];
        }
        require(amountOut > 0, "Error Swapping Tokens");
        return amountOut;
    }

    function setActiveDex(uint256 exchange) public onlyGovernance {
        if(exchange == 0){
            activeDex = sushiswapRouter;
            swapPair = sushiswapPair;
        }else if (exchange == 1) {
            activeDex = uniswapRouter;
            swapPair = uniswapPair;
        }else{
            require(false, "incorrect pool");
        }
        swapRouter = IUniswapV2Router02(activeDex);
        IERC20(crv).safeApprove(activeDex, uint256(-1));
    }

    function sweep(address _token) external onlyGovernance {
        IERC20(_token).safeTransfer(governance, IERC20(_token).balanceOf(address(this)));
        uint256 balance = address(this).balance;
        if(balance > 0){
            governance.transfer(balance);
        }
    }

    function shouldUseVault(uint256 lpReserveA, uint256 lpReserveB) internal view returns (bool) {
        uint256 safetyFactor = 1e5; // For extra precision
        // Get asset ratio of swap pair
        IUniswapV2Pair pair = IUniswapV2Pair(swapPair); // Pair we might want to swap against
        (uint256 reserveA, uint256 reserveB, ) = pair.getReserves();
        uint256 pool1ratio = reserveB.mul(safetyFactor).div(reserveA);
        // Get asset ratio of LP pair
        uint256 pool2ratio = lpReserveB.mul(safetyFactor).div(lpReserveA);

        return pool1ratio > pool2ratio; // Use vault only if pool 2 offers a better price
    }

    function calculateSingleSided(uint256 reserveIn, uint256 userIn) internal pure returns (int256) {
        return
            Babylonian.sqrt(
                int256(reserveIn).mul(int256(userIn).mul(3988000) + int256(reserveIn).mul(3988009))
            ).sub(int256(reserveIn).mul(1997)) / 1994;
    }

    // This function goes into some complex math which is explained here: 
    // https://hackmd.io/@Ap_76vwNTg-vxJxbiaLMMQ/rkoFT_bz_
    function calculateSwapAmount(bool _isEth, uint256 _haveAmount) internal view returns (uint256) {
        IUniswapV2Pair pair = IUniswapV2Pair(swapPair); // Pair we swap against
        (uint256 reserveA, uint256 reserveB, ) = pair.getReserves();
        int256 pool1HaveReserve = 0;
        int256 pool1WantReserve = 0;
        int256 rb = 0;
        int256 ra = 0;
        
        if(_isEth){
            pool1HaveReserve = int256(reserveA);
            pool1WantReserve = int256(reserveB);
        }
        else{
            pool1HaveReserve = int256(reserveB);
            pool1WantReserve = int256(reserveA);
        }
        
        pair = IUniswapV2Pair(ethYveCrv); // Pair we swap against
        (reserveA, reserveB, ) = pair.getReserves();
        if(_isEth){
            ra = int256(reserveB);
            rb = int256(reserveA);
        }
        else{
            ra = int256(reserveA);
            rb = int256(reserveB);
        }
        
        int256 numToSquare = int256(_haveAmount).mul(997); // This line and the next one add together a part of the formula...
        numToSquare = numToSquare.add(pool1HaveReserve.mul(1000)); // ...which we'll need to square later on.
        int256 FACTOR = 1e20; // To help with precision

        // LINE 1
        int256 h = int256(_haveAmount); // re-assert this or else stack will get too deep and forget it
        int256 a = pool1WantReserve.mul(-1994).mul(ra).div(rb);
        int256 b = h.mul(997);
        b = b.sub(pool1HaveReserve.mul(1000));
        b = a.mul(b);

        // LINE 2
        a = ra.mul(ra).mul(FACTOR).div(rb);
        a = a.div(rb); // We lose some precision here
        int256 c = numToSquare.mul(numToSquare);
        a = c.mul(a).div(FACTOR);
        a = b.add(a); // Add result to total
        
        // LINE 3
        int256 r = pool1WantReserve.mul(pool1WantReserve);
        r = r.mul(994009);
        a = a.add(r); // Add result to total
        
        // Sqaure what we have so far
        int256 sq = Babylonian.sqrt(a);
        
        // LINE 4
        b = h.mul(997).mul(ra).mul(FACTOR).div(rb);
        
        // LINE 5
        FACTOR = 1e20; // re-state, otherwise stack depth is exceeded
        r = pool1HaveReserve.mul(1000);
        r = r.mul(ra).mul(FACTOR);
        r = r.div(rb);
        h = pool1WantReserve.mul(-997);
        h = h.mul(FACTOR).sub(r);
        b = b.add(h).div(FACTOR);
        b = b.add(sq);
        
        // LINE 6
        a = ra.mul(1994);
        a = a.mul(FACTOR).div(rb); // We lose some precision here
        return uint256(b.mul(FACTOR).div(a));
    }

    receive() external payable {
        // Don't zap any ETH we receive from our DEX
        if (msg.sender != activeDex && msg.sender != sushiswapRouter) {
            _zapIn(true, msg.value);
        }
    }
}
