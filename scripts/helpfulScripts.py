from brownie import (accounts, network, config, Contract, MockV3Aggregator, MockWETH, MockDAI)



INITIAL_PRICE_FEED_VALUE = 2000000000000000000000
DECIMALS = 18

contractsToMock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "dai_usd_price_feed": MockV3Aggregator,
    "stsToken": MockDAI,
    "wethToken": MockWETH,
}



def getAccount():
    if network.show_active() == "development" or ("fork" in network.show_active()):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def getContractAddress(_contractName, _account=None):
    if network.show_active() == "development":
        mockAggregator = MockV3Aggregator.deploy(18, 2000000000000000000000, {"from": _account})
        return mockAggregator.address
    else:
        return config["networks"][network.show_active()][_contractName]


def getContract(_contractName, _account=None):
    SCaddress = getContractAddress(_contractName, _account)
    if network.show_active() == "development":
        print("Functionality not available in development network. Use testnet or local fork.")
        exit()
    elif(SCaddress):
        print("Getting SmartContract of " + _contractName + "...")
        contractType = contractsToMock[_contractName]
        contract = Contract.from_abi(contractType._name, SCaddress, contractType.abi)
    else:
        print("Using MockWETH as default Token to fund contract")
        contract = Contract.from_abi(MockWETH.name, SCaddress, MockWETH.abi)
    
    return contract 




def deployMocks(decimals=DECIMALS, initialValue=INITIAL_PRICE_FEED_VALUE):
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = getAccount()
    print("Deploying Mock Price Feed...")
    mockPriceFeed = MockV3Aggregator.deploy(
        decimals, initialValue, {"from": account}
    )
    print(f"Deployed to {mockPriceFeed.address}")
    print("Deploying Mock DAI...")
    daiToken = MockDAI.deploy({"from": account})
    print(f"Deployed to {daiToken.address}")
    print("Deploying Mock WETH")
    wethToken = MockWETH.deploy({"from": account})
    print(f"Deployed to {wethToken.address}")