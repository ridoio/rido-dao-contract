from ape import accounts, project
from eth_abi import encode

EPOCH_INTERVAL = 3600 * 3
def main():
    account = accounts.load("rido_test")

    # dataPools = project.AirdropDataPool.deploy(sender=account, publish=True)
    dataPools = project.AirdropDataPool.deploy(sender=account)

    # miner = project.AirdropMiner.deploy(dataPools, sender=account,publish=True)
    miner = project.AirdropMiner.deploy(dataPools,EPOCH_INTERVAL, sender=account)

    # rido = project.ERC20SRIDO.deploy("RIDO Integral","RIDO-I",18,miner,10_000_000_000 *10 ** 18,5_000_000_000 *10 ** 18,sender=account,publish=True)
    rido = project.ERC20SRIDO.deploy("RIDO Integral","RIDO-I",18,miner,10_000_000_000 *10 ** 18,5_000_000_000 *10 ** 18,sender=account)
    # rido = project.ERC20SRIDO.at("0x8Be0a7C07D8772edaD46dccd53ec237Ee00E6A8b")


    print(rido.balanceOf(miner))

    print(dataPools.set_gauge_controller(account.address,sender=account))
    print(dataPools.set_minter(account.address,sender=account))

    data_pool = encode(['bytes32'], [bytes.fromhex('44d562ac1d7cd77e232978687fea027ace48f719cf1d58c7888e509663bb87fc')])
    print(dataPools.set_data_pools(data_pool,1,2,8,100 * 10 ** 18,0,sender=account))
    print(dataPools.set_data_pools(data_pool,1,2,8,100 * 10 ** 18,24,sender=account))

    print(miner.start(rido,sender=account))

