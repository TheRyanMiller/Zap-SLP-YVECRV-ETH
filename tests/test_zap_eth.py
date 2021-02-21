from brownie import Wei
from helpers import zapBalances
from datetime import datetime

def test_zap_eth_swap(zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    
    """
        ETH Part: 1
        Currently, it is more economical to swap for yveCRV than to mint it
        directly via the vault. This first set of 6 tests will move the price
        of yveCRV up until it becomes more efficient to mint via the vault.
    """

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

def test_zap_eth_vault(zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    """
        ETH Part: 2
        The remainder of these ETH tests should be routed
        through the vault due to the previous tests raising
        the price of yveCRV against ETH.
    """

    # Deposit 1 ETH - 
    amount = 1e18
    eth_whale.transfer(zap.address, amount)
    acceptable_dust = 1e10
    assert pickleJar.balanceOf(eth_whale) > 0
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