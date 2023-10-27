from brownie import TokenFarm
from scripts import helpfulScripts


def deploytokenFarm(_DappSC):
    account = helpfulScripts.getAccount()
        
    TokenFarmSC = TokenFarm.deploy(
        _DappSC.address,
        {'from': account},
    )

    return TokenFarmSC




def main():
    deploytokenFarm()