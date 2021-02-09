/**
 *Submitted for verification at Etherscan.io on 2020-11-05
 */

// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.7.0;

interface IveCurveVault {
    function depositAll() external;
    function deposit(uint256 _amount) external;
    function approve(address spender, uint256 amount) external returns (bool);
    function transfer(address dst, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}