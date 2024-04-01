import { Token } from "../Main"
import { useEthers, useTokenBalance } from "@usedapp/core"
// import { formatUnits } from "@ethersproject/units"
// import { BalanceMsg } from "../../components/BalanceMsg"


export interface WalletBalanceProps {
    token: Token
}

export const WalletBallance = ({ token }: WalletBalanceProps) => {

    const { image, address, name } = token
    const { account } = useEthers()
    const tokenBalance = useTokenBalance(address, account)
    console.log(tokenBalance?.toString())

    return (<div>I'm the Wallet Balance</div>)
}