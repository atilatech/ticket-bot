import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';
import SafeApiKit from '@safe-global/api-kit'
import { ethers } from 'ethers'
import { EthersAdapter } from '@safe-global/protocol-kit'
import { proposeTransaction } from './transaction';
import bodyParser from 'body-parser';


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
    const proposeResponse = await proposeTransaction(safeAddress);
    res.send(proposeResponse);

});

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});