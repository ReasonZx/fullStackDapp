import { useEthers } from '@usedapp/core';
import { constants } from "ethers"
import helperConfig from "../helper-config.json"
import brownieConfig from "../brownie-config.json"
import networkMapping from "../chain-info/deployments/map.json"
import dapp from "../pepethink.png"
import eth from "../eth.png"
import dai from "../dai.png"
import { YourWallet } from './YourWallet';


export type Token = {
    image: string
    address: string
    name: string
}

export const Main = () => {

    const { chainId, error } = useEthers()
    
    const networkName = chainId ? helperConfig[chainId.toString() as keyof typeof helperConfig]  : "dev"

    console.log(chainId)
    console.log(networkName)

    let stringChainId = String(networkName) as keyof typeof brownieConfig["networks"];
    const networkConfig = brownieConfig["networks"][stringChainId];
    const dappTokenAddress = chainId ? networkMapping[chainId.toString() as keyof typeof networkMapping]["DappToken"][0] : constants.AddressZero
    const wethTokenAddress = networkConfig && "wethToken" in networkConfig ? networkConfig["wethToken"] : constants.AddressZero
    const stsTokenAddress = networkConfig && "stsToken" in networkConfig ? networkConfig["stsToken"] : constants.AddressZero

    const supportedTokens : Array<Token> = [
        {
            image: dapp,
            address: dappTokenAddress,
            name: "Dapp"
        },
        {
            image: eth,
            address: wethTokenAddress,
            name: "Weth"
        },
        {
            image: dai,
            address: stsTokenAddress,
            name: "Dai"
        }
    ]

    return (<>
        <YourWallet supportedTokens={supportedTokens}/>
    </>)
}