// SPDX-License-Identifier: AGPL-3.0
/**
 *Submitted for verification at Etherscan.io on 2021-02-06
*/

pragma solidity >=0.6.0 <0.7.0;

interface IPickleJar {
    function balanceOf(address account) external view returns (uint256);
    function depositAll() external;
    function deposit(uint256 _amount) external;
    function withdrawAll() external;
}