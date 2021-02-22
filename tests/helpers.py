from itertools import count
from brownie import Wei, reverts, network
import brownie
import requests

def zapBalances(zap, crv, crv_whale, eth_whale, pickleJar, sushiLPs, yveCrv, pickleStake):
    print('\n----Zap Contract Balances----')
    print('ETH:', zap.balance() /  1e18)
    print('Crv:', crv.balanceOf(zap) /  1e18)
    print('yveCRV:', yveCrv.balanceOf(zap) /  1e18)
    print('sushiLPs:', sushiLPs.balanceOf(zap) /  1e18)
    print('pickles:', pickleJar.balanceOf(zap) /  1e18)
    print('pickleSTAKE:', pickleStake.userInfo(26, eth_whale)[0] /  1e18)
    print('--------\n')
    print("\n-----ETH Whale Balances----")
    print('Pickle jar:', pickleJar.balanceOf(eth_whale) /  1e18)
    print('CRV:', crv.balanceOf(eth_whale) /  1e18)
    print('ETH:', eth_whale.balance() /  1e18)
    print('pickleSTAKE:', pickleStake.userInfo(26, eth_whale)[0] /  1e18)
    print('--------\n')
    print("\n-----CRV Whale Balances----")
    print('Pickle Jar:', pickleJar.balanceOf(crv_whale) /  1e18)
    print('pickleSTAKE:', pickleStake.userInfo(26, eth_whale)[0] /  1e18)
    print('CRV:', crv.balanceOf(crv_whale) /  1e18)
    print('ETH:', crv_whale.balance() /  1e18)
    print('--------\n')