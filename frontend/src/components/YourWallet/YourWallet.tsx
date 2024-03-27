import {Token} from "../Main"
import React, { useState } from "react"
import { Box, makeStyles } from "@material-ui/core"
import { TabContext, TabList, TabPanel } from "@material-ui/lab"
import { tokenToString } from "typescript"
import { Tab } from "@material-ui/core"


interface YourWalletProps {
    supportedTokens: Array<Token>
}

export const YourWallet = ({supportedTokens} : YourWalletProps) => {

    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0)

    return (
        <Box>
            <h1> Your Wallet! </h1>
            <Box>
                <TabContext value = {selectedTokenIndex.toString()}>
                    <TabList aria-label="Stake form tabs">
                        {supportedTokens.map((token, index) => {
                            return (
                                <Tab label={token.name}
                                    value={index.toString()}
                                    key={index} />
                            )
                        })}
                    </TabList>
                </TabContext>
            </Box>
        </Box>
    )

}