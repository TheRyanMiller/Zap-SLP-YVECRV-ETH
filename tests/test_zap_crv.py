from brownie import Wei
from helpers import zapBalances
from datetime import datetime

def test_zap_crv_swap(zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    crv.approve(zap, 5e28, {"from":crv_whale})

    """
        CRV Part: 1
        Currently, it is more economical to swap for yveCRV than to mint it
        directly via the vault. This first set of tests will increasingly move the price
        of CRV up until it becomes more efficient to mint yveCRV via the vault.
    """

    # Zap 0.5
    zap.zapInCRV(1e17, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(crv_whale)

    # Zap 5
    zap.zapInCRV(5e18, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(crv_whale)

    # Zap 50
    zap.zapInCRV(5e19, {"from":crv_whale})
    acceptable_dust = 1e12 
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(crv_whale)
    
    # Zap 500
    zap.zapInCRV(5e20, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(crv_whale)

    # Zap 5,000
    zap.zapInCRV(5e21, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust

    # Zap 50,000
    zap.zapInCRV(5e22, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(crv_whale)

    # Zap 500,000
    zap.zapInCRV(5e23, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust

    #zapBalances(zap, crv, crv_whale, eth_whale, pickleJar, sushiLPs, yveCrv)

def test_zap_crv_vault(zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    crv.approve(zap, 5e28, {"from":crv_whale})

    """
        CRV Part: 2
        The remainder of these CRV tests should be routed
        through the vault due to the previous tests raising
        the price of CRV against ETH.
    """

    # Zap 500,000
    zap.zapInCRV(5e23, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust
    prev_pickle_balance = pickleJar.balanceOf(crv_whale)

    # Zap 5
    zap.zapInCRV(5e18, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust

    # Zap 50
    zap.zapInCRV(5e19, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust

    # Zap 500
    zap.zapInCRV(5e20, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust

    # Zap 5,000
    zap.zapInCRV(5e21, {"from":crv_whale})
    acceptable_dust = 1e12
    assert pickleJar.balanceOf(crv_whale) - prev_pickle_balance > 0
    assert zap.balance() < acceptable_dust
    assert crv.balanceOf(zap) < acceptable_dust
    assert sushiLPs.balanceOf(zap) < acceptable_dust
    assert yveCrv.balanceOf(zap) < acceptable_dust
    assert pickleJar.balanceOf(zap) < acceptable_dust

    #zapBalances(zap, crv, crv_whale, eth_whale, pickleJar, sushiLPs, yveCrv)

