from itertools import count
from brownie import Wei, reverts, network
import brownie
import requests

def zapBalances(zap, crv, pickleJar, sushiLPs, yveCrv):
    print('\n----Zap Balances----')
    
    print('ETH:', zap.balance() /  1e18)
    print('Crv:', crv.balanceOf(zap) /  1e18)
    print('yveCRV:', yveCrv.balanceOf(zap) /  1e18)
    print('sushiLPs:', sushiLPs.balanceOf(zap) /  1e18)
    print('Pickles:', pickleJar.balanceOf(zap) /  1e18)
    print('\n--------')