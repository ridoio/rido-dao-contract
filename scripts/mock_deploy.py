from ape import accounts, project
from eth_abi import encode


def main():
    account = accounts.load("rido_test")

    # dataPools = project.AirdropDataPool.deploy(sender=account, publish=True)
    project.IAirdropMiner.deploy(sender=account)

