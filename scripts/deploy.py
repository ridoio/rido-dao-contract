from ape import accounts, project, networks

account = accounts.load("rido_test")
dataPools = project.AirdropDataPool.deploy(sender=account, publish=True)
miner = project.AirdropMiner.deploy(dataPools, sender=account,publish=True)

