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

    uint256 public amountOut = 0;

    // Tokens
    address public constant ethYveCrv = 0x10B47177E92Ef9D5C6059055d92DdF6290848991; // LP Token
    address public constant yveCrv = 0xc5bDdf9843308380375a611c18B50Fb9341f502A;
    address public constant crv = 0xD533a949740bb3306d119CC777fa900bA034cd52;
    address public constant weth = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    IPickleJar private pickleJar = IPickleJar(0x5Eff6d166D66BacBC1BF52E2C54dD391AE6b1f48);
    IveCurveVault private yVault = IveCurveVault(yveCrv);

    // DEXes
    address public activeDex = 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F; // Sushi default
    address private uniswapRouter = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private sushiswapRouter = 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F;
    address private mooniswappool = 0x1f629794B34FFb3B29FF206Be5478A52678b47ae;
    IUniswapV2Router02 public swapRouter;
    
    // ETH/CRV pair we want to swap with
    address public swapPair = 0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009; // Initialize with Sushiswap
    
    // Dex swap paths
    address[] public swapEthPath;
    address[] public swapCrvPath;

    // Misc
    bool private reEntry = false;
    address public governance = 0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52;

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
    }

    function setGovernance(address _governance) external onlyGovernance {
        governance = _governance;
    }

    /*  ETH Zap  */
    receive() external payable {
        // Allow ETH to be sent in from DEX routers, but reject for all others when reEntry = true
        if (reEntry && msg.sender != activeDex && msg.sender != sushiswapRouter) {
            //require(msg.value == 0, "No re-entrancy!");
        }
        if(msg.sender != activeDex && msg.sender != sushiswapRouter){
            reEntry = true;
            _zapIn(true, msg.value);
        }
    }

    /*  CRV Zap  */
    function zapIn(uint256 crvAmount) external payable {
        require(crvAmount != 0, "0 CRV");
        require(msg.value == 0, "Single sided zaps only");
        if (reEntry) {
            return;
        }
        reEntry = true;
        IERC20(crv).transferFrom(msg.sender, address(this), crvAmount);
        _zapIn(false, crvAmount);
    }

    function _zapIn(bool _isEth, uint _haveAmount) internal returns (uint256) {

        /*
            Step 1:
            Calculate how much to swap into pool in order to make our balance equal part A and B
            The outputs amounts should be a balanced LP deposit
            calculateSwapInAmount uses algo described in this blog post:
            https://blog.alphafinance.io/onesideduniswap/
        */
        
        uint256 amountToSwap = calculateSwapAmount(_haveAmount, _isEth);
        /*
            Step 2:
            Swap token
        */
        _tokenSwap(amountToSwap, _isEth);
        /*
            Step 3: 
            Deposit CRV into yveCrv and receieve yveCRV tokens
        */
        yVault.depositAll();
        
        /*
            Step 4:
            Add liquidity to the Sushi ETH/yveCrv pair
        
        IUniswapV2Router02(sushiswapRouter).addLiquidityETH{value: address(this).balance}( 
            yveCrv, // The non-ETH token in pair
            yVault.balanceOf(address(this)), // Desired amount of token
            1, // Token min
            1, // Eth min
            address(this), // Where to send LP tokens
            now // deadline
        );*/
        
        /*
            Step 5:
            Deposit LP tokens to Pickle jar and send tokens back to user
        */
        pickleJar.depositAll();
        IERC20(address(pickleJar)).safeTransfer(msg.sender, pickleJar.balanceOf(address(this)));
        
        reEntry = false;
    }

    function _tokenSwap(uint256 _amountIn, bool _isEth) internal returns (uint256) {
        if (_isEth) {
            amountOut = swapRouter.swapExactETHForTokens{value: _amountIn}(1, swapEthPath, address(this), now)[swapEthPath.length - 1];
        } else {
            amountOut = _amountIn;//swapRouter.swapExactTokensForETH(_amountIn, 0, swapCrvPath, address(this), now)[swapCrvPath.length - 1];
        }
        require(amountOut > 0, "Error Swapping Tokens");
        return amountOut;
    }

    function setActiveDex(uint256 exchange, address _pairAddress) public onlyGovernance {
        if(exchange == 0){
            activeDex = uniswapRouter;
        }else if (exchange == 1) {
            activeDex = sushiswapRouter;
        }else if (exchange == 2) {
            activeDex = mooniswappool;
        }else{
            require(false, "incorrect pool");
        }
        swapRouter = IUniswapV2Router02(activeDex);
        swapPair = _pairAddress;
        IERC20(crv).safeApprove(activeDex, uint256(-1));
    }

    function sweep(address _token) external onlyGovernance {
        IERC20(_token).safeTransfer(governance, IERC20(_token).balanceOf(address(this)));
    }

    function calculateSwapAmount(uint256 _haveAmount, bool _isEth) internal view returns (uint256) {
        IUniswapV2Pair pair = IUniswapV2Pair(swapPair); // Pair we target our LP allocation against
        (uint256 reserveA, uint256 reserveB, ) = pair.getReserves();
        int256 pool1HaveReserve = 0;
        int256 pool1WantReserve = 0;
        if(_isEth){
            pool1HaveReserve = int256(reserveA);
            pool1WantReserve = int256(reserveB);
        }
        else{
            pool1HaveReserve = int256(reserveB);
            pool1WantReserve = int256(reserveA);
        }

        pair = IUniswapV2Pair(ethYveCrv);
        (reserveA, reserveB, ) = pair.getReserves();
        int256 rb = 0;
        int256 ra = 0;
        if(_isEth){
            rb = int256(reserveA);
            ra = int256(reserveB);
        }
        else{
            ra = int256(reserveA);
            rb = int256(reserveB);
        }
        
        int256 numToSquare = int256(_haveAmount).mul(997).add(pool1HaveReserve.mul(1000));
        int256 FACTOR = 100000000;
        
        // LINE 1
        int256 a = pool1WantReserve.mul(-1994);
        a = a.mul(ra).mul(FACTOR).div(rb); // Line 1
        int256 b = int256(_haveAmount).mul(997); // line 1 , part 2
        b = b.sub(pool1HaveReserve.mul(1000));
        b = a.mul(b).div(FACTOR); // Compete line 1
        
        // LINE 2
        a = ra.mul(ra).mul(FACTOR).div(rb);
        a = a.div(rb); // We lose some precision here
        int256 c = numToSquare.mul(numToSquare);
        a = c.mul(a).div(FACTOR); // Complete Line 2
        a = b.add(a); // Add line 1
        
        // LINE 3
        int256 h = int256(_haveAmount);
        int256 r = pool1WantReserve.mul(pool1WantReserve); // square this from line 3
        r = r.mul(994009);
        a = a.add(r); // Add line 3 to running total
        
        // Sqaure the total
        int256 sq = Babylonian.sqrt(a);
        
        // LINE 4
        FACTOR = 100000000;
        b = h.mul(997).mul(ra).mul(FACTOR).div(rb); // This is line 4
        // LINE 5
        r = pool1HaveReserve.mul(1000);
        r = r.mul(ra).mul(FACTOR);
        r = r.div(rb);
        h = pool1WantReserve.mul(-997);
        h = h.mul(FACTOR).sub(r);
        
        b = b.add(h).div(FACTOR);
        b = b.add(sq);
        
        // LINE 6
        a = ra.mul(1994).mul(FACTOR);
        a = a.div(rb);
        return uint256(b.mul(FACTOR).div(a));
    }
}
