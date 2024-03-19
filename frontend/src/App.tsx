import React from 'react';
import { ChainId, DAppProvider, Sepolia } from '@usedapp/core';
import { Header } from './components/Header';
import { Container } from "@material-ui/core"
import { Main } from "./components/Main"

function App() {
  return (
    <DAppProvider config={{
      networks: [Sepolia]
    }}>
      <Header />
      <Container maxWidth="md">
        <div>Hi!</div>
          <Main />
      </Container>
    </DAppProvider>
      

  );
}

export default App;
