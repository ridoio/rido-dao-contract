# import ape
# import pytest

# Standard test comes from the interpretation of EIP-20
# ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
# INITIAL_SUPPLY = 1_303_030_303
# AIRDROP_SUPPLY = 303
# YEAR = 86400 * 365
# INITIAL_RATE = 8714335457889396245


# def test_initial_state(ridoerc20, owner, airdrop_minter):
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


#     # Check intial balance of tokens
#     assert ridoerc20.balanceOf(owner) == (INITIAL_SUPPLY  - AIRDROP_SUPPLY)* 10 ** 18
#     assert ridoerc20.balanceOf(airdrop_minter) == AIRDROP_SUPPLY  * 10 ** 18
#     assert ridoerc20.total_supply() == INITIAL_SUPPLY * 10 ** 18
#     assert ridoerc20.start_epoch_time() == 0


# def test_start_data_mint(ridoerc20,minter,owner):

#     tx = ridoerc20.start_data_mint(minter, sender = owner)
    

#     assert ridoerc20.minter() == minter
#     assert ridoerc20.mining_epoch() == -1
#     assert ridoerc20.rate() == 0
#     assert ridoerc20.available_supply() == INITIAL_SUPPLY * 10 ** 18

#     tx = ridoerc20.update_mining_parameters(sender = owner)
#     assert ridoerc20.mining_epoch() == 0
#     assert ridoerc20.rate() == INITIAL_RATE



    
