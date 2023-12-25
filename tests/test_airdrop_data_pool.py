import ape
import pytest
from decimal import Decimal
from eth_abi import encode

def test_airdrop_data_pool(airdrop_data_pool, owner, airdrop_minter,gauge_controller):
    assert airdrop_data_pool.admin() == owner
    airdrop_data_pool.set_minter(gauge_controller, sender = owner)
    airdrop_data_pool.set_gauge_controller(gauge_controller, sender = owner)
    assert airdrop_data_pool.mintingEpoch() == 0
    
    airdrop_data_pool.set_epoch(1, sender = gauge_controller)
    assert airdrop_data_pool.mintingEpoch() == 1

    test_schema_uid = encode(['bytes32'], [b'a'])

    airdrop_data_pool.set_data_pools(test_schema_uid, 1, 2 , 2, 10 ** 16, 1, sender = gauge_controller)
    assert airdrop_data_pool.get_data_pool_info(1,test_schema_uid)[0] == Decimal(0.5)
    assert airdrop_data_pool.get_data_pool_info(1,test_schema_uid)[1] == 2
    assert airdrop_data_pool.get_data_pool_info(1,test_schema_uid)[2] == 10 ** 16


    airdrop_data_pool.set_epoch(3,sender = gauge_controller)
    assert airdrop_data_pool.mintingEpoch() == 3
    airdrop_data_pool.set_data_pools(test_schema_uid, 1, 2 , 2, 5 * 10 ** 16, 3, sender = gauge_controller)
    assert airdrop_data_pool.get_data_pool_info(1,test_schema_uid)[0] == Decimal(0.5)
    assert airdrop_data_pool.get_data_pool_info(1,test_schema_uid)[1] == 2
    assert airdrop_data_pool.get_data_pool_info(1,test_schema_uid)[2] == 10 ** 16

    assert airdrop_data_pool.get_data_pool_info(2,test_schema_uid)[0] == Decimal(0.5)
    assert airdrop_data_pool.get_data_pool_info(2,test_schema_uid)[1] == 2
    assert airdrop_data_pool.get_data_pool_info(2,test_schema_uid)[2] == 10 ** 16

    assert airdrop_data_pool.get_data_pool_info(3,test_schema_uid)[0] == Decimal(0.5)
    assert airdrop_data_pool.get_data_pool_info(3,test_schema_uid)[1] == 2
    assert airdrop_data_pool.get_data_pool_info(3,test_schema_uid)[2] == 5 * 10 ** 16


    airdrop_data_pool.update_each_epoch_attestations([test_schema_uid,test_schema_uid,test_schema_uid],[1,2,3], [1000,2000,3000], sender = owner)
    assert airdrop_data_pool.get_total_attestations(1,test_schema_uid) == 1000
    assert airdrop_data_pool.get_total_attestations(2,test_schema_uid) == 2000
    assert airdrop_data_pool.get_total_attestations(3,test_schema_uid) == 3000

    assert airdrop_data_pool.piecewise_function(2,1,2,2) == 20_000_000_000
    assert airdrop_data_pool.piecewise_function(2,1,2,3) == 25_000_000_000
    assert airdrop_data_pool.piecewise_function(2,1,2,4) == 30_000_000_000
    assert airdrop_data_pool.piecewise_function(2,1,2,5) == 32_500_000_000

    assert airdrop_data_pool.get_rate_of_pool(2, 2000, test_schema_uid, 2) == 10 ** 13
    
    hash = encode(['bytes32'],[bytes.fromhex('bc36789e7a1e281436464229828f817d6612f7b477d66591ff96a9e064bcc98a')])
    s = bytes.fromhex('477b6de519d36351f3805369c1d9688ed47ea4cd980909426172019fec7b7d8f48e84fdcfa9e261bd35c565cf464919150acfeaa4ec0aed0442ce07f97b55b9a00')

    print(len(s),len(hash))
    assert airdrop_data_pool.ecrecoverSig(hash,s) == '0x471543A3bd04486008c8a38c5C00543B73F1769e'


    # assert airdrop_data_pool.mintingEpoch() == 312122



    # assert airdrop_minter.admin() == owner
    # airdrop_minter.start(ridoerc20, sender = owner)
    # assert airdrop_minter.token() == ridoerc20
    # assert airdrop_minter.minting_epoch() == 0
    # assert airdrop_minter.total_supply() == 0

    # airdrop_minter.update_mining_parameters(sender = receiptor)
    # assert airdrop_minter.minting_epoch() == 1 
    # assert airdrop_minter.total_supply() == 0

    # byte_array = bytes([0] * 65)

    # airdrop_minter.mint_for(receiptor,[],byte_array,sender = receiptor)
    # assert airdrop_minter.minting_epoch() == 1 
    # print(airdrop_minter.total_supply())
    # print(ridoerc20.balanceOf(receiptor))
    # assert airdrop_minter.total_supply() == 10 ** 18
    # assert ridoerc20.balanceOf(receiptor) == 10 ** 18
