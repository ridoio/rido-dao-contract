import ape
import pytest

AIRDROP_SUPPLY = 50_000_000 * 10 ** 18

def test_airdrop_mint(chain,ridoerc20, owner, airdrop_minter,receiptor, airdrop_data_pool):
    assert ridoerc20.balanceOf(airdrop_minter) == AIRDROP_SUPPLY
    assert airdrop_minter.admin() == owner

    airdrop_minter.start(ridoerc20, sender = owner)
    assert airdrop_minter.token() == ridoerc20
    assert airdrop_minter.minting_epoch() == 0
    assert airdrop_minter.total_supply() == 0

    chain.pending_timestamp += 86000 * 14 + 4000


    airdrop_minter.update_mining_parameters(sender = receiptor)
    assert airdrop_minter.minting_epoch() == 1 
    assert airdrop_minter.total_supply() == 0

    byte_array = bytes([0] * 65)

    airdrop_minter.mint_for(receiptor,[],byte_array,sender = receiptor)
    assert airdrop_minter.minting_epoch() == 1 
    print(airdrop_minter.total_supply())
    print(ridoerc20.balanceOf(receiptor))
    assert airdrop_minter.total_supply() == 10 ** 18
    assert ridoerc20.balanceOf(receiptor) == 10 ** 18



