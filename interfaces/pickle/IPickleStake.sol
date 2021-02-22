// SPDX-License-Identifier: AGPL-3.0
/**
 *Submitted for verification at Etherscan.io on 2021-02-06
*/

pragma solidity >=0.6.0 <0.7.0;

 interface IPickleStake {

    // Deposit LP tokens to MasterChef for PICKLE allocation.
    function deposit(uint256 _pid, uint256 _amount) external;

    // Withdraw LP tokens from MasterChef.
    function withdraw(uint256 _pid, uint256 _amount) external;

}