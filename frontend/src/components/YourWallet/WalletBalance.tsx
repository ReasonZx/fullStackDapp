import { Token } from "../Main"
import { useEthers, useTokenBalance } from "@usedapp/core"
import { formatUnits } from "@ethersproject/units"
// import { BalanceMsg } from "../../components/BalanceMsg"


export interface WalletBalanceProps {
    token: Token
}

export const WalletBallance = ({ token }: WalletBalanceProps) => {

    const { image, address, name } = token
    const { account } = useEthers()
    const tokenBalance = useTokenBalance(address, account)
    const formattedTokenBalance: number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)) : 0
    
    return (<div>{formattedTokenBalance}</div>)
}