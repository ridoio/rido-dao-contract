from ape import accounts, project
from eth_abi import encode


def main():
    account = accounts.load("rido_test")

    dataPool = project.AirdropDataPool.at("0xda137d79af705BbcF0DE95328314039f35495622")
    reward3 = 1000 * 10 **18    

    uid1 = encode(['bytes32'], [bytes.fromhex('0x07656ef97ae97711b79c9e79b3e0409712a8bb9bf26f3495ad15f48cdd49cfac')])
    t1 = 1
    t2 = 4
    s  = 4
    reward1 = 3_000_000 * 10 ** 18
    reward2 = 500_000 * 10 ** 18
    dataPool.set_data_pools(uid1,t1,t2,s,reward1,1,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward2,2,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward3,3,sender=account)


    uid1 = encode(['bytes32'], [bytes.fromhex('0xd120198a6df8348a9752ec2f515d71bf5d7f262ca8c1db21a1cca7049239cf5f')])
    t1 = 1
    t2 = 4
    s = 1
    reward1 = 1_000_000 * 10 ** 18
    reward2 = 100_000 * 10 ** 18
    dataPool.set_data_pools(uid1,t1,t2,s,reward1,1,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward2,2,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward3,3,sender=account)

    uid1 = encode(['bytes32'], [bytes.fromhex('0x52d3584323b9443df8d939521977cd0952a71ce704d23902819826f18f02138b')])
    dataPool.set_data_pools(uid1,t1,t2,s,reward1,1,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward2,2,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward3,3,sender=account)

    uid1 = encode(['bytes32'], [bytes.fromhex('0xe0792ce04d0f1e3ba04c2b9921f07c44f92b07c4bc02b3de7d4db48c33330180')])
    dataPool.set_data_pools(uid1,t1,t2,s,reward1,1,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward2,2,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward3,3,sender=account)

    uid1 = encode(['bytes32'], [bytes.fromhex('0x56e32a4cda2153ed31b40d740e51b12249b1e47b3ff3ea08183bd771dfb0a62b')])
    dataPool.set_data_pools(uid1,t1,t2,s,reward1,1,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward2,2,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward3,3,sender=account)

    uid1 = encode(['bytes32'], [bytes.fromhex('0xffa193bb8997005d2baa254350274a128b5e8911b650fcc70e1dbb49f29982ac')])
    dataPool.set_data_pools(uid1,t1,t2,s,reward1,1,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward2,2,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward3,3,sender=account)



    uid1 = encode(['bytes32'], [bytes.fromhex('0x3fefc0971918a31a7f430d4091de8acfc30433495b487864cbcf21e16e616cf6')])
    t1 = 1
    t2 = 4
    s = 1
    reward1 = 600_000 * 10 ** 18
    reward2 = 100_000 * 10 ** 18
    dataPool.set_data_pools(uid1,t1,t2,s,reward1,1,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward2,2,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward3,3,sender=account)

    uid1 = encode(['bytes32'], [bytes.fromhex('0x7c73fb2fff66ac0010aee3fdd076540f68beed5f8b53d41a6d75e4d9243490f4')])
    t1 = 1
    t2 = 4
    s = 1
    reward1 = 800_000 * 10 ** 18
    reward2= 100_000 * 10 ** 18
    dataPool.set_data_pools(uid1,t1,t2,s,reward1,1,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward2,2,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward3,3,sender=account)

    uid1 = encode(['bytes32'], [bytes.fromhex('0xbd6a269de18805c7d23e870c4a62d0a60cb0e3cdc1d7269ac0cc6479602bdae4')])
    dataPool.set_data_pools(uid1,t1,t2,s,reward1,1,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward2,2,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward3,3,sender=account)

    uid1 = encode(['bytes32'], [bytes.fromhex('0xb0b2b76caa3bbb60261cb091354fc0effa9f6e04d0a2bbb6b6e593b8c567b46a')])
    dataPool.set_data_pools(uid1,t1,t2,s,reward1,1,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward2,2,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward3,3,sender=account)

    uid1 = encode(['bytes32'], [bytes.fromhex('0x9905bf67752646d97ddffd894b1d5a30d23ea30ca35aa8c8100f0fe92a4c225e')])
    t1 = 1
    t2 = 4
    s = 3
    reward1 = 3_000_000 * 10 ** 18
    reward2= 300_000 * 10 ** 18

    uid1 = encode(['bytes32'], [bytes.fromhex('0x0ead2db8b13f937e1f8652180bb892dc5d78ee63d4b1564abd71ce0a3a304d7d')])
    t1 = 1
    t2 = 4
    s = 4
    reward1 = 3_000_000 * 10 ** 18
    reward2= 500_000 * 10 ** 18
    dataPool.set_data_pools(uid1,t1,t2,s,reward1,1,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward2,2,sender=account)
    dataPool.set_data_pools(uid1,t1,t1,s,reward3,3,sender=account)

