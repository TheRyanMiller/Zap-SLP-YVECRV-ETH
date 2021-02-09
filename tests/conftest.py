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
    yield accounts.at("0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8", force=True)

@pytest.fixture
def crv_whale(accounts):
    yield accounts.at("0xc0AA8046f860996B7B6d366b6d71391e70C74376", force=True)

@pytest.fixture
def zap(dev, ZapYveCrvEthLPsToPickle):
    yield dev.deploy(ZapYveCrvEthLPsToPickle)