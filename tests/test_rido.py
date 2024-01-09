import ape
import pytest
from decimal import Decimal
from eth_abi import encode
from ape import chain

EPOCH_INTERVAL = 3600 * 2

def test_airdrop_data_pool(airdrop_data_pool, owner,gauge_controller,airdrop_minter,ridoerc20):
    assert airdrop_data_pool.admin() == owner
    airdrop_data_pool.set_minter(airdrop_minter, sender = owner)
    airdrop_data_pool.set_gauge_controller(gauge_controller, sender = owner)
    assert airdrop_data_pool.mintingEpoch() == 0


    data_pool = encode(['bytes32'], [bytes.fromhex('0bdc3271b3654ea1e0709a1b711aad16d52abdd80e9117ebac9a5dbfae326c3d')])
    data_pool2 = encode(['bytes32'], [bytes.fromhex('0bdc3271b3654ea1e0709a1b711aad16d52abdd80e9117ebac9a5dbfae326c3f')])

    assert len(airdrop_data_pool.get_data_pools()) == 0
    airdrop_data_pool.set_data_pools(data_pool, 1, 2 , 2, 10 ** 16, 0, sender = gauge_controller)
    assert airdrop_data_pool.get_data_pool_info(0,data_pool)[0] == Decimal(0.5)
    assert airdrop_data_pool.get_data_pool_info(0,data_pool)[1] == 2
    assert airdrop_data_pool.get_data_pool_info(0,data_pool)[2] == 10 ** 16

    assert airdrop_data_pool.get_data_pools()[0].hex() == '0x0bdc3271b3654ea1e0709a1b711aad16d52abdd80e9117ebac9a5dbfae326c3d'

    airdrop_minter.start(ridoerc20,sender = owner)
    chain.pending_timestamp += EPOCH_INTERVAL * 2 + 1
    airdrop_minter.epoch_write(sender = gauge_controller)

    assert airdrop_data_pool.mintingEpoch() == 3

    airdrop_data_pool.set_data_pools(data_pool, 1, 2 , 2, 5 * 10 ** 16, 3, sender = gauge_controller)
    airdrop_data_pool.set_data_pools(data_pool2, 1, 2 , 2 ,5 * 10 ** 16, 3, sender = gauge_controller)


    assert airdrop_data_pool.get_data_pool_info(0,data_pool)[0] == Decimal(0.5)
    assert airdrop_data_pool.get_data_pool_info(0,data_pool)[1] == 2
    assert airdrop_data_pool.get_data_pool_info(0,data_pool)[2] == 10 ** 16

    assert airdrop_data_pool.get_data_pool_info(1,data_pool)[0] == Decimal(0.5)
    assert airdrop_data_pool.get_data_pool_info(1,data_pool)[1] == 2
    assert airdrop_data_pool.get_data_pool_info(1,data_pool)[2] == 10 ** 16

    assert airdrop_data_pool.get_data_pool_info(2,data_pool)[0] == Decimal(0.5)
    assert airdrop_data_pool.get_data_pool_info(2,data_pool)[1] == 2
    assert airdrop_data_pool.get_data_pool_info(2,data_pool)[2] == 10 ** 16

    assert airdrop_data_pool.get_data_pool_info(3,data_pool)[0] == Decimal(0.5)
    assert airdrop_data_pool.get_data_pool_info(3,data_pool)[1] == 2
    assert airdrop_data_pool.get_data_pool_info(3,data_pool)[2] == 5 * 10 ** 16

    assert airdrop_data_pool.get_data_pool_info(1,data_pool2)[0] == Decimal(0)
    assert airdrop_data_pool.get_data_pool_info(1,data_pool2)[1] == 0
    assert airdrop_data_pool.get_data_pool_info(1,data_pool2)[2] == 0

    assert airdrop_data_pool.get_data_pool_info(1,data_pool2)[0] == Decimal(0)
    assert airdrop_data_pool.get_data_pool_info(1,data_pool2)[1] == 0
    assert airdrop_data_pool.get_data_pool_info(1,data_pool2)[2] == 0

    assert airdrop_data_pool.get_data_pool_info(2,data_pool2)[0] == Decimal(0)
    assert airdrop_data_pool.get_data_pool_info(2,data_pool2)[1] == 0
    assert airdrop_data_pool.get_data_pool_info(2,data_pool2)[2] == 0

    assert airdrop_data_pool.get_data_pool_info(3,data_pool2)[0] == Decimal(0.5)
    assert airdrop_data_pool.get_data_pool_info(3,data_pool2)[1] == 2
    assert airdrop_data_pool.get_data_pool_info(3,data_pool2)[2] == 5 * 10 ** 16


    airdrop_data_pool.set_data_pools(data_pool2, 1, 2 , 2, 5 * 10 ** 16, 10, sender = gauge_controller)
    assert airdrop_data_pool.get_data_pool_info(4,data_pool2)[0] == Decimal(0)
    assert airdrop_data_pool.get_data_pool_info(4,data_pool2)[1] == 0
    assert airdrop_data_pool.get_data_pool_info(4,data_pool2)[2] == 0

    assert airdrop_data_pool.get_data_pool_info(10,data_pool2)[0] == Decimal(0.5)
    assert airdrop_data_pool.get_data_pool_info(10,data_pool2)[1] == 2
    assert airdrop_data_pool.get_data_pool_info(10,data_pool2)[2] == 5 * 10 ** 16


    chain.pending_timestamp += EPOCH_INTERVAL
    airdrop_data_pool.update_each_epoch_attestations([data_pool,data_pool,data_pool,data_pool],[0,1,2,3], [1000,1000,2000,3000], sender = owner)

    assert airdrop_data_pool.mintingEpoch() == 4

    assert airdrop_data_pool.get_total_attestations(0,data_pool) == 1000
    assert airdrop_data_pool.get_total_attestations(1,data_pool) == 1000
    assert airdrop_data_pool.get_total_attestations(2,data_pool) == 2000
    assert airdrop_data_pool.get_total_attestations(3,data_pool) == 3000

    assert airdrop_data_pool.piecewise_function(2,1,2,1) == 10_000_000_000
    assert airdrop_data_pool.piecewise_function(2,1,2,2) == 20_000_000_000
    assert airdrop_data_pool.piecewise_function(2,1,2,3) == 25_000_000_000
    assert airdrop_data_pool.piecewise_function(2,1,2,4) == 30_000_000_000
    assert airdrop_data_pool.piecewise_function(2,1,2,9) == 38_125_000_000

    assert airdrop_data_pool.reward_remaining(data_pool,2) == 10 ** 16

    assert airdrop_data_pool.get_rate_of_pool(2, 2000, data_pool, 2) == 10 ** 13
    
    s = bytes.fromhex('e7a51bada338ecbec162f2c488b7802985c2632f4de70ec18d04ffee1b8aac2218d2552d69e70b5151ebbcf89601052c94cf18e5ca6fcc026d72d55bcf0aecd300')
    assert airdrop_data_pool.hash_user_extract_info(owner,[data_pool,data_pool],[1,2],[4,9],s) == '0x471543A3bd04486008c8a38c5C00543B73F1769e'

    rido_addr = '0x471543A3bd04486008c8a38c5C00543B73F1769e'
    airdrop_data_pool.set_admin(rido_addr,sender = owner)
    assert airdrop_data_pool.admin() == rido_addr
    tx = airdrop_minter.mint([data_pool,data_pool],[1,2],[4,9],s, sender = owner)
    logs = list(tx.decode_logs(airdrop_data_pool.ExtractReward))
    assert len(logs) == 2
    assert logs[0].extractor == logs[1].extractor and logs[1].extractor == owner
    assert logs[0].extract== 30000000000000       and logs[1].extract == 19062500000000
    assert logs[0].epoch == 1                     and logs[1].epoch == 2
    assert logs[0].attestation == 4               and logs[1].attestation==9
    assert logs[0].total ==  1000                 and logs[1].total == 2000

    assert airdrop_data_pool.withdrawed_epoch(owner,[data_pool])[0].hex() == "0x0bdc3271b3654ea1e0709a1b711aad16d52abdd80e9117ebac9a5dbfae326c3d"
    assert airdrop_data_pool.withdrawed_epoch(owner,[data_pool])[1][0] == 1000 
    assert airdrop_data_pool.withdrawed_epoch(owner,[data_pool])[1][1] == 2000 
    assert airdrop_data_pool.withdrawed_epoch(owner,[data_pool])[2][0] == 1 
    assert airdrop_data_pool.withdrawed_epoch(owner,[data_pool])[2][1] == 2 
    assert airdrop_data_pool.withdrawed_epoch(owner,[data_pool])[3][0] == 4 
    assert airdrop_data_pool.withdrawed_epoch(owner,[data_pool])[3][1] == 9 

    assert airdrop_data_pool.reward_remaining(data_pool,2) == 9980937500000000
    assert airdrop_data_pool.reward_remaining(data_pool,1) == 9970000000000000

