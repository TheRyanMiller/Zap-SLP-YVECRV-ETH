import pytest
from brownie import config, Contract


### Tokens

@pytest.fixture
def weth(interface):
    yield interface.ERC20("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")

@pytest.fixture
def crv(interface):
    yield interface.ERC20("0xD533a949740bb3306d119CC777fa900bA034cd52")

@pytest.fixture
def yveCrv(interface):
    yield interface.ERC20("0xc5bDdf9843308380375a611c18B50Fb9341f502A")

@pytest.fixture
def sushiLPs(interface):
    yield interface.ERC20("0x10B47177E92Ef9D5C6059055d92DdF6290848991")

@pytest.fixture
def pickleJar(interface):
    yield interface.ERC20("0x5Eff6d166D66BacBC1BF52E2C54dD391AE6b1f48")

# @pytest.fixture
# def pickleStake(interface):
#     #yield interface.IPickleStake("0xbD17B1ce622d73bD438b9E658acA5996dc394b0d")
#     yield Contract.from_explorer("0xbD17B1ce622d73bD438b9E658acA5996dc394b0d")

@pytest.fixture
def swapPair(interface):
    yield interface.ERC20("0x58dc5a51fe44589beb22e8ce67720b5bc5378009")

### Other Accounts

@pytest.fixture
def gov(accounts):
    yield accounts.at("0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52", force=True)

@pytest.fixture
def dev(accounts):
    yield accounts[0]

@pytest.fixture
def eth_whale(accounts):
    whale1 = accounts.at("0x2bf792Ffe8803585F74E06907900c2dc2c29aDcb", force=True)
    whale2 = accounts.at("0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8", force=True)
    whale1.transfer(whale2, whale1.balance() - 1e18)
    yield whale2

@pytest.fixture
def eth_whale_other(accounts):
    whale = accounts.at("0x1b3cB81E51011b549d78bf720b0d924ac763A7C2", force=True)
    yield whale

@pytest.fixture
def crv_whale(crv, accounts):
    whale1 = accounts.at("0xE93381fB4c4F14bDa253907b18faD305D799241a", force=True)
    whale2 = accounts.at("0xc0AA8046f860996B7B6d366b6d71391e70C74376", force=True)
    # We use tranfer, not transferFrom here because it is not a contract
    crv.transfer(whale2, crv.balanceOf(whale1), {"from":whale1})
    crv.transfer(accounts[5], crv.balanceOf(whale2), {"from":whale2})
    accounts[5].transfer(accounts[9], accounts[5].balance() - 1e18)
    assert crv.balanceOf(accounts[5]) > 0
    yield accounts[5]

@pytest.fixture
def crv_whale_other(crv, accounts):
    whale1 = accounts.at("0x826C3064D4F5b9507152F5cB440ca9326E1ec8FA", force=True)
    yield whale1

@pytest.fixture
def zap(dev, ZapYveCrvEthLPsToPickle):
    yield dev.deploy(ZapYveCrvEthLPsToPickle)

@pytest.fixture
def sushi_router():
    yield Contract.from_explorer("0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F")
