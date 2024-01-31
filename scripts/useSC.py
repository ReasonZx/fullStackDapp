from brownie import config, network
from scripts import helpfulScripts, deployDappSC, deployTokenFarmSC
from web3 import Web3
import yaml
import json
import os
import shutil


KEPT_BALANCE = Web3.toWei(100, "ether")



def deployTokenFarmDappToken(frontEndUpdate=False):
    account = helpfulScripts.getAccount()
    dappToken = deployDappSC.deployDapp()
    tokenFarmSC = deployTokenFarmSC.deploytokenFarm(dappToken)

    tx = dappToken.transfer(tokenFarmSC.address, dappToken.totalSupply() - KEPT_BALANCE, {'from': account})
    tx.wait(1)

    wethToken   = helpfulScripts.getContract("wethToken")
    stsToken    = helpfulScripts.getContract("stsToken")
    
    AllowedTokensToPriceFeed = {
        dappToken: helpfulScripts.getContract("dai_usd_price_feed"),
        stsToken: helpfulScripts.getContract("dai_usd_price_feed"),
        wethToken: helpfulScripts.getContract("eth_usd_price_feed"),
    }
    
    addAllowedTokens(tokenFarmSC, AllowedTokensToPriceFeed, account)
    
    if frontEndUpdate:
        updateFrontEnd()
    return tokenFarmSC, dappToken
    
    
    
def addAllowedTokens(tokenFarm, AllowedTokensToPriceFeed, account):
    for token in AllowedTokensToPriceFeed:
        addTx = tokenFarm.addAllowedTokens(token.address, {"from": account})
        addTx.wait(1)
        addTx = tokenFarm.setPriceFeedContract(
            token.address, AllowedTokensToPriceFeed[token], {"from": account}
        )
        addTx.wait(1)
    return tokenFarm

def updateFrontEnd():
    # Send the build folder
    copyFoldersToFrontEnd("./build", "./frontend/src/chain-info")

    # Sending the front end our config in JSON format
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open("./frontend/src/brownie-config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json)
    print("Front end updated!")
    
    
def copyFoldersToFrontEnd(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    
def main():
    deployTokenFarmDappToken(frontEndUpdate=True)