from brownie import Wei
from helpers import zapBalances
from datetime import datetime

def test_zap_eth(zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    # Zap 0.01 ETH
    amount = 1e16
    eth_whale.transfer(zap.address, amount)
    acceptable_dust = 1e10
    assert pickleJar.balanceOf(eth_whale) > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(eth_whale)

    # Zap 0.1 ETH
    amount = 1e17
    eth_whale.transfer(zap.address, amount)
    acceptable_dust = 1e10
    assert pickleJar.balanceOf(eth_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(eth_whale)

    # Deposit 1 ETH
    amount = 1e18
    eth_whale.transfer(zap.address, amount)
    acceptable_dust = 1e10
    assert pickleJar.balanceOf(eth_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(eth_whale)

    # Deposit 10 ETH
    amount = 1e19
    eth_whale.transfer(zap.address, amount)
    acceptable_dust = 1e10
    assert pickleJar.balanceOf(eth_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(eth_whale)

    # Deposit 100 ETH
    amount = 1e20
    eth_whale.transfer(zap.address, amount)
    acceptable_dust = 1e10
    assert pickleJar.balanceOf(eth_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(eth_whale)

    # Deposit 1000 ETH
    amount = 1e21
    eth_whale.transfer(zap.address, amount)
    acceptable_dust = 1e10
    assert pickleJar.balanceOf(eth_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(eth_whale)

def test_zap_crv(zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    crv.approve(zap, 5e28, {"from":crv_whale})

    # Zap 0.5
    zap.zapIn(5e17, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(crv_whale)

    # Zap 5
    zap.zapIn(5e18, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(crv_whale)

    # Zap 50
    zap.zapIn(5e19, {"from":crv_whale})
    acceptable_dust = 1e12 
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(crv_whale)
    
    # Zap 500
    zap.zapIn(5e20, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(crv_whale)

    # Zap 5,000
    zap.zapIn(5e21, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust

    # Zap 50,000
    zap.zapIn(5e22, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(crv_whale)

    # Zap 500,000
    zap.zapIn(5e23, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust