from brownie import Wei
from helpers import zapBalances
from datetime import datetime
"""
def test_zap_eth(zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    # Deposit 100 ETH
    eth_whale.transfer(zap.address, "100 ether")
    zapBalances(zap, crv, crv_whale, eth_whale, pickleJar, sushiLPs, yveCrv)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(zap.amountOut())
    assert pickleJar.balanceOf(eth_whale) > 0
    assert zap.balance == 0
    assert crv.balanceOf(zap) == 0
    assert sushiLPs.balanceOf(zap) == 0
    assert yveCrv.balanceOf(zap) == 0
    assert pickleJar.balanceOf(zap) == 0
"""
def test_zap_crv(zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    # Deposit 5000 CRV
    crv.approve(zap, 5e28, {"from":crv_whale})
    zap.zapIn(5e21, {"from":crv_whale})
    zapBalances(zap, crv, crv_whale, eth_whale, pickleJar, sushiLPs, yveCrv)
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("amountOUt",zap.amountOut())
    print("pqWant",zap.pool1WantReserve())
    print("p1Have",zap.pool1HaveReserve())
    print("ra:",zap.ra())
    print("rb:",zap.rb())
    assert pickleJar.balanceOf(crv_whale) > 0
    assert zap.balance == 0
    assert crv.balanceOf(zap) == 0
    assert sushiLPs.balanceOf(zap) == 0
    assert yveCrv.balanceOf(zap) == 0
    assert pickleJar.balanceOf(zap) == 0
    
"""
def test_reentrant(zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    crv.approve(zap, 1e28, {"from":crv_whale})
    zap.zapIn(5e22, {"from":crv_whale})
    zap.zapIn(5e22, {"from":crv_whale})
    zapBalances(zap, crv, crv_whale, eth_whale, pickleJar, sushiLPs, yveCrv)
    assert pickleJar.balanceOf(crv_whale) > 0
    assert zap.balance == 0
    assert crv.balanceOf(zap) == 0
    assert sushiLPs.balanceOf(zap) == 0
    assert yveCrv.balanceOf(zap) == 0
    assert pickleJar.balanceOf(zap) == 0

def test_eth_after_throwing_crv_pool_off_balance(sushi_router, weth, zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    # Deposit 100 ETH
    now = datetime.utcnow().timestamp()
    deposit_amt = eth_whale.balance() - 101*1e18
    sushi_router.swapExactETHForTokens(1, [weth.address, crv.address], eth_whale, now, {"from":eth_whale, "value":deposit_amt})
    eth_whale.transfer(zap.address, "100 ether")
    crv.approve(zap, 1e28, {"from":crv_whale})
    zap.zapIn(5e22, {"from":crv_whale})
    zapBalances(zap, crv, crv_whale, eth_whale, pickleJar, sushiLPs, yveCrv)
    assert pickleJar.balanceOf(eth_whale) > 0
    assert pickleJar.balanceOf(crv_whale) > 0
    assert zap.balance == 0
    assert crv.balanceOf(zap) == 0
    assert sushiLPs.balanceOf(zap) == 0
    assert yveCrv.balanceOf(zap) == 0
    assert pickleJar.balanceOf(zap) == 0

def test_crv_after_throwing_crv_pool_off_balance(sushi_router, crv_whale_other, eth_whale_other, weth, zap, gov, dev, crv, pickleJar, sushiLPs, yveCrv, eth_whale, swapPair, crv_whale, interface):
    now = datetime.utcnow().timestamp()
    swap_amount = crv.balanceOf(crv_whale) - 500e18
    print(swap_amount)
    crv.approve(sushi_router, crv.balanceOf(crv_whale), {"from":crv_whale})
    sushi_router.swapExactTokensForETH(swap_amount, 1, [crv.address, weth.address], crv_whale, now, {"from":crv_whale})
    eth_whale_other.transfer(zap.address, "100 ether")
    crv.approve(zap, crv.balanceOf(crv_whale), {"from":crv_whale_other})
    zap.zapIn(crv.balanceOf(crv_whale), {"from":crv_whale_other})
    zapBalances(zap, crv, crv_whale_other, eth_whale_other, pickleJar, sushiLPs, yveCrv)
    assert pickleJar.balanceOf(crv_whale) > 0
    assert zap.balance == 0
    assert crv.balanceOf(zap) == 0
    assert sushiLPs.balanceOf(zap) == 0
    assert yveCrv.balanceOf(zap) == 0
    assert pickleJar.balanceOf(zap) == 0
"""