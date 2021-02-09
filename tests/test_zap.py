from brownie import Wei
from helpers import zapBalances

def test_zap_eth(zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    # Deposit 100 ETH
    eth_whale.transfer(zap.address, "100 ether")
    zapBalances(zap, crv, crv_whale, eth_whale, pickleJar, sushiLPs, yveCrv)

def test_zap_crv(zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    crv.approve(zap, 1e28, {"from":crv_whale})
    # Deposit 5000 CRV
    zap.zapIn(5*1e22, {"from":crv_whale})
    zapBalances(zap, crv, crv_whale, eth_whale, pickleJar, sushiLPs, yveCrv)
    
def test_reentrant(zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    crv.approve(zap, 1e28, {"from":crv_whale})
    zap.zapIn(5e22, {"from":crv_whale})
    zap.zapIn(5e22, {"from":crv_whale})
    zapBalances(zap, crv, crv_whale, eth_whale, pickleJar, sushiLPs, yveCrv)