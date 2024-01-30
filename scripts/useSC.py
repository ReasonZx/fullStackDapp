from brownie import config, network
from scripts import helpfulScripts, deployDappSC, deployTokenFarmSC
from web3 import Web3

KEPT_BALANCE = Web3.toWei(100, "ether")



def main():
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
    
def addAllowedTokens(tokenFarm, AllowedTokensToPriceFeed, account):
    for token in AllowedTokensToPriceFeed:
        addTx = tokenFarm.addAllowedTokens(token.address, {"from": account})
        addTx.wait(1)
        addTx = tokenFarm.setPriceFeedContract(
            token.address, AllowedTokensToPriceFeed[token], {"from": account}
        )
        addTx.wait(1)
    return tokenFarm