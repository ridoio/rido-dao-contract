import pytest

from eip712.messages import EIP712Message

@pytest.fixture(scope="session")
def Permit(chain, token):
    class Permit(EIP712Message):
        _name_   : "string" = "RIDO"
        _version_: "string" = "1.0"
        _chainId_: "uint256" = chain.chain_id
        
        _verifyingContract_: "address" = token.address

        owner   : "address"
        spender : "address"
        value   : "uint256"
        nonce   : "uint256"
        deadline: "uint256"
    return Permit


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]

@pytest.fixture(scope="session")
def receiptor(accounts):
    return accounts[1]


@pytest.fixture(scope="session")
def minter(accounts):
    return accounts[2]

@pytest.fixture(scope="session")
def gauge_controller(accounts):
    return accounts[3]


@pytest.fixture(scope="session")
def airdrop_data_pool(owner,project):
    return owner.deploy(project.AirdropDataPool)


@pytest.fixture(scope="session")
def airdrop_minter(owner,project,airdrop_data_pool):
    return owner.deploy(project.AirdropMiner,airdrop_data_pool)


@pytest.fixture(scope="session")
def ridoerc20(owner,project,airdrop_minter):
    return owner.deploy(project.ERC20RIDO,"RIDO","RID",18,airdrop_minter)


@pytest.fixture(scope="session")
def airdrop_data_pool(owner,project):
     return owner.deploy(project.AirdropDataPool)