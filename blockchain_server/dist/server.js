"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const dotenv_1 = __importDefault(require("dotenv"));
// Import Moralis
const Moralis = require("moralis").default;
// Import the EvmChain dataType
const { EvmChain } = require("@moralisweb3/common-evm-utils");
const transaction_1 = require("./transaction");
const body_parser_1 = __importDefault(require("body-parser"));
const nft_1 = require("./nft");
const MORALIS_API_KEY = process.env.MORALIS_API_KEY;
dotenv_1.default.config();
const app = (0, express_1.default)();
const port = process.env.PORT || 5001;
app.use(body_parser_1.default.json());
app.get('/', (req, res) => {
    res.send('Express + TypeScript Server');
});
app.post('/propose-transaction', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    console.log(req.body);
    const safeAddress = req.body.address;
    const chainId = req.body.chain_id;
    const proposeResponse = yield (0, transaction_1.proposeTransaction)(safeAddress, chainId);
    return res.json({ response: proposeResponse });
}));
app.post('/has-nft', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    console.log(req.body);
    const address = req.body.address;
    const chainId = req.body.chain_id;
    const hasNft = yield (0, nft_1.walletHasNFT)(chainId, address);
    return res.json({ hasNft });
}));
// Add this a startServer function that initialises Moralis
const startServer = () => __awaiter(void 0, void 0, void 0, function* () {
    yield Moralis.start({
        apiKey: MORALIS_API_KEY,
    });
    app.listen(port, () => {
        console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
    });
});
startServer();
