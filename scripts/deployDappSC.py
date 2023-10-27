from brownie import TokenFarm, DappToken, config, network
from scripts import helpfulScripts


def deployDapp():
    account = helpfulScripts.getAccount()

    DappSC = DappToken.deploy({'from': account})

    return DappSC




def main():
    deployDapp()