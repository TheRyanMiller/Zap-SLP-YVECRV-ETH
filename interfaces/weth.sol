// SPDX-License-Identifier: AGPL-3.0
pragma solidity >=0.6.0 <0.7.0;
pragma experimental ABIEncoderV2;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

interface IWETH is IERC20 {
    function deposit() external payable;
    function decimals() external view returns (uint256);
    function withdraw(uint256) external;
}
