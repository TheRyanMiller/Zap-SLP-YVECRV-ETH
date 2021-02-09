from itertools import count
from brownie import Wei, reverts, network
import brownie
import requests

def zapBalances(zap, crv, crv_whale, eth_whale, pickleJar, sushiLPs, yveCrv):
    print('\n----Zap Contract Balances----')
    print('ETH:', zap.balance() /  1e18)
    print('Crv:', crv.balanceOf(zap) /  1e18)
    print('yveCRV:', yveCrv.balanceOf(zap) /  1e18)
    print('sushiLPs:', sushiLPs.balanceOf(zap) /  1e18)
    print('pickles:', pickleJar.balanceOf(zap) /  1e18)
    print("\n-----User Balances----")
    
    print('Eth whale:', pickleJar.balanceOf(eth_whale) /  1e18)
    print('Crv whale:', pickleJar.balanceOf(crv_whale) /  1e18)
    print('--------\n')