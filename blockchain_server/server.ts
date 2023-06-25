import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';
// Import Moralis
const Moralis = require("moralis").default;
// Import the EvmChain dataType
const { EvmChain } = require("@moralisweb3/common-evm-utils");
import { proposeTransaction } from './transaction';
import bodyParser from 'body-parser';
import { walletHasNFT } from './nft';
const MORALIS_API_KEY = process.env.MORALIS_API_KEY;

dotenv.config();

const app: Express = express();
const port = process.env.PORT || 5001;
app.use(bodyParser.json());

app.get('/', (req: Request, res: Response) => {
  res.send('Express + TypeScript Server');
});

app.post('/propose-transaction', async (req: Request, res: Response) => {

    console.log(req.body);
    const safeAddress = req.body.address;
    const chainId = req.body.chain_id;
    const proposeResponse = await proposeTransaction(safeAddress, chainId);
    return res.json({response: proposeResponse});

});

app.post('/has-nft', async (req: Request, res: Response) => {

  console.log(req.body);
  const address = req.body.address;
  const chainId = req.body.chain_id;
  const hasNft = await walletHasNFT(chainId, address);
  return res.json({hasNft});

});

// Add this a startServer function that initialises Moralis
const startServer = async () => {
  await Moralis.start({
    apiKey: MORALIS_API_KEY,
  });

  app.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
  });
};

startServer();