import ape
import pytest

# Standard test comes from the interpretation of EIP-20
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


# def test_initial_state(ridoerc20, owner):
#     """
#     Test inital state of the contract.
#     """
#     # Check the token meta matches the deployment
#     # token.method_name() has access to all the methods in the smart contract.
#     assert ridoerc20.name() == "RIDO"
#     assert ridoerc20.symbol() == "RID"
#     assert ridoerc20.decimals() == 18

#     # Check of intial state of authorization
#     assert ridoerc20.admin() == owner
#     assert ridoerc20.minter() == ZERO_ADDRESS
#     assert ridoerc20.airdropMinter() == ZERO_ADDRESS

#     # Check intial balance of tokens
#     assert ridoerc20.balanceOf(owner) == 1_303_030_303 * 10 ** 18
#     assert ridoerc20.total_supply() == 1_303_030_303 * 10 ** 18
#     assert ridoerc20.start_epoch_time() == 0


def test_airdrop_minter(ridoerc20,airdrop_minter,owner):
    print(ridoerc20.admin())
    print(owner)
    print(ridoerc20.airdropMinter())
    print(ridoerc20.minter())

    tx = ridoerc20.set_airdrop_minter(airdrop_minter, sender = owner)
    assert ridoerc20.airdropMinter() == airdrop_minter
    print(ridoerc20.airdropMinter())

    tx = ridoerc20.airdrop_mint(airdrop_minter,1000000, sender = airdrop_minter)
    logs = list(tx.decode_logs(ridoerc20.SetAirdropMinter))
    assert len(logs) == 1
    assert logs[0]._from == ZERO_ADDRESS
    assert logs[0]._to == airdrop_minter
    assert logs[0]._value == 1000000

    assert ridoerc20.balanceOf(airdrop_minter) == 1000000


    
