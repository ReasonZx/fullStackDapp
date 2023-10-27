from brownie import config, network
from scripts import helpfulScripts, deployDappSC, deployTokenFarmSC
from web3 import Web3

KEPT_BALANCE = Web3.toWei(100, "ether")



def main():
    account = helpfulScripts.getAccount()
    dappSC = deployDappSC.deployDapp()
    tokenFarmSC = deployTokenFarmSC.deploytokenFarm(dappSC)

    tx = dappSC.transfer(tokenFarmSC.address, dappSC.totalSupply() - KEPT_BALANCE, {'from': account})
    tx.wait(1)