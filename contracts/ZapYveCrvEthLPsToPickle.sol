// SPDX-License-Identifier: AGPL-3.0
pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

import {Math} from "@openzeppelin/contracts/math/Math.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {SafeERC20, SafeMath, IERC20, Address} from "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

import {IUniswapV2Router02} from "../interfaces/uniswap/IUniswapV2Router02.sol";
import {IUniswapV2Pair} from "../interfaces/uniswap/IUniswapV2Pair.sol";
import {IveCurveVault} from "../interfaces/yearn/IveCurveVault.sol";
import {IPickleJar} from "../interfaces/pickle/IPickleJar.sol";

// import "@uniswap/lib/contracts/libraries/Babylonian.sol";
library Babylonian {
    function sqrt(uint256 y) internal pure returns (uint256 z) {
        if (y > 3) {
            z = y;
            uint256 x = y / 2 + 1;
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

    // Tokens
    address public constant ethYveCrv = 0x10B47177E92Ef9D5C6059055d92DdF6290848991; // LP Token
    address public constant yveCrv = 0xc5bDdf9843308380375a611c18B50Fb9341f502A;
    address public constant crv = 0xD533a949740bb3306d119CC777fa900bA034cd52;
    address public constant weth = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    IPickleJar private pickleJar = IPickleJar(0x5Eff6d166D66BacBC1BF52E2C54dD391AE6b1f48);
    IveCurveVault private yVault = IveCurveVault(yveCrv);

    // DEXes
    address public activeDex = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private uniswapRouter = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private sushiswapRouter = 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F;
    address private mooniswappool = 0x1f629794B34FFb3B29FF206Be5478A52678b47ae;
    IUniswapV2Router02 public swapRouter;
    
    // Sushi Pair
    address public swapPair = 0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009;
    // Uniswap Pair
    address public constant ethCrvU = 0x3dA1313aE46132A397D90d95B1424A9A7e3e0fCE;
    //Paths
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

    function setGovernance(address _governance) external onlyGovernance{
        governance = _governance;
    }

    // Accept ETH and zap in with no token swap
    receive() external payable {
        if (reEntry && msg.sender != activeDex) {
            return;
        }
        if(msg.sender != activeDex){
            reEntry = true;
            _zapIn(true, address(this).balance);
        }
    }

    function zapIn(uint256 crvAmount) external payable {
        require(crvAmount != 0, "0 CRV");
        if (reEntry) {
            return;
        }
        reEntry = true;
        require(msg.value == 0, "Single sided zaps only!"); // Require single-sided
        IERC20(crv).safeTransferFrom(msg.sender, address(this), crvAmount);
        _zapIn(false, crvAmount);
    }

    function _zapIn(bool _isEth, uint _haveAmount) internal returns (uint256) {
        IUniswapV2Pair pair = IUniswapV2Pair(swapPair);
        
        // Step 1:
        // Get current amounts of each token in the swap pair
        (uint256 reserveA, uint256 reserveB, ) = pair.getReserves();

        // Step 2:
        // Calculate how much to swap into pool in order to make our balance equal part A and B
        // The outputs will be the balanced LP deposit
        uint256 amountToSwap = 0;
        uint256 amtEthToLP = 0;
        uint256 amtYveCrvToLP = 0;
        if(_isEth){
            amountToSwap = calculateSwapInAmount(reserveA, _haveAmount);
            amtYveCrvToLP = _tokenSwap(amountToSwap, true);
            amtEthToLP = address(this).balance;
        }
        else{
            amountToSwap = calculateSwapInAmount(reserveB, _haveAmount);
            amtEthToLP = _tokenSwap(amountToSwap, false);
            amtYveCrvToLP = IERC20(crv).balanceOf(address(this));
        }
        
        // Step 3: 
        // Deposit CRV into yveCrv and receieve yveCRV tokens
        yVault.depositAll();
        
        // Step 4:
        // LP in the Sushi ETH/yveCrv pair
        (uint256 amtYveCrvAdded, uint256 amtETHAdded, uint256 amountLPs) = IUniswapV2Router02(sushiswapRouter).addLiquidityETH{value: address(this).balance}( 
            yveCrv, // Non-ETH token of pool
            yVault.balanceOf(address(this)), // Desired amount of token
            1, // Token min
            1, // Eth min
            address(this), // Where to send LP tokens
            now // deadline
        );
        
        // Step 5:
        // Deposit to Pickle jar and send tokens to user
        pickleJar.depositAll();
        // Send user their Pick Sushi LPs
        IERC20(address(pickleJar)).safeTransfer(msg.sender, pickleJar.balanceOf(address(this)));

        reEntry = false;
    }

    function checkBalances() external view returns (uint256 _crv, uint256 _eth, uint256 _yvecrv, uint256 _pSLP, uint _ethYveCrv){
        _pSLP = IERC20(address(pickleJar)).balanceOf(address(this));
        _crv = IERC20(address(crv)).balanceOf(address(this));
        _eth = address(this).balance;
        _yvecrv = IERC20(address(yVault)).balanceOf(address(this));
        _ethYveCrv = IERC20(address(ethYveCrv)).balanceOf(address(this));
    }

    function calculateSwapInAmount(uint256 reserveIn, uint256 userIn) internal pure returns (uint256) {
        return
            Babylonian.sqrt(
                reserveIn.mul(userIn.mul(3988000) + reserveIn.mul(3988009))
            ).sub(reserveIn.mul(1997)) / 1994;
    }

    function _tokenSwap(uint256 _amountIn, bool _isEth) internal returns (uint256 amountOut) {
        if (_isEth) {
            amountOut = swapRouter.swapExactETHForTokens{value: _amountIn}(1, swapEthPath, address(this), now)[swapEthPath.length - 1];
        } else {
            amountOut = swapRouter.swapExactTokensForETH(_amountIn, 1, swapCrvPath, address(this), now)[swapCrvPath.length - 1];
        }
        require(amountOut > 0, "Error Swapping Tokens");
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
}
