from brownie import TokenFarm, DappToken, config, network
from scripts import helpfulScripts


def deploytokenFarmAndDappSC():
    account = helpfulScripts.getAccount()

    DappSC = DappToken.deploy(
        {'from': account},
    )

        
    TokenFarmSC = TokenFarm.deploy(
        DappSC.address,
        {'from': account},
    )

    return TokenFarmSC

def main():
    deploytokenFarmAndDappSC()