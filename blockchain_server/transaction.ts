import { ethers } from 'ethers'
import SafeApiKit from '@safe-global/api-kit'
import Safe, { EthersAdapter, SafeFactory, SafeAccountConfig } from '@safe-global/protocol-kit'
import { SafeTransaction, SafeTransactionDataPartial } from '@safe-global/safe-core-sdk-types'
import { CHAIN_INFO } from './chain'

// Run this file:
// source examples/.env
// npx ts-node examples/protocol-kit/index.ts


export async function proposeTransaction(safeAddress: string, amount = '0.005',
  destination = '0x38103603fEB199fba32be9b3A464877f28e659A7', chainId = '5') {

// https://chainlist.org/?search=goerli&testnets=true

const chain = CHAIN_INFO[chainId.toString()];
console.log(chain.rpcUrl);
const provider = new ethers.providers.JsonRpcProvider(chain.rpcUrl)

// Create a wallet instance from the sender's private key
const delegateSigner = new ethers.Wallet(process.env.DELEGATE_PRIVATE_KEY!, provider)
  // Create a transaction object
  amount = ethers.utils.parseUnits(amount, 'ether').toString()

  const safeTransactionData: SafeTransactionDataPartial = {
    to: destination,
    data: '0x',
    value: amount
  }

  const delegateAdapter = new EthersAdapter({
    ethers,
    signerOrProvider: delegateSigner
  })

  const safe = await Safe.create({
    ethAdapter: delegateAdapter,
    safeAddress
  })
  // Create a Safe transaction with the provided parameters
  const safeTransaction: SafeTransaction = await safe.createTransaction({ safeTransactionData })

  // Deterministic hash based on transaction parameters
  const safeTxHash = await safe.getTransactionHash(safeTransaction)

  // Sign transaction to verify that the transaction is coming from owner 1
  const senderSignature = await safe.signTransactionHash(safeTxHash)

  const txServiceUrl = chain.transactionServiceUrl;

  const safeService = new SafeApiKit({ txServiceUrl, ethAdapter: delegateAdapter })

  return await safeService.proposeTransaction({
    safeAddress,
    safeTransactionData: safeTransaction.data,
    safeTxHash,
    senderAddress: await delegateSigner.getAddress(),
    senderSignature: senderSignature.data,
  })
}