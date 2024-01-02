from ape import accounts, project

account = accounts.load("rido_test")
dataPools = project.AirdropDataPool.deploy(sender=account)
miner = project.AirdropMiner.deploy(dataPools, sender=account)