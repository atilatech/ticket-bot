import { CHAIN_INFO } from "./chain";

const Moralis = require("moralis").default;

export async function walletHasNFT(chainId: string, address: string) {
    const chain = CHAIN_INFO[chainId.toString()];
    const nftAddress = chain.nftAddress;
    const nftsBalances = await Moralis.EvmApi.nft.getWalletNFTs({
      address,
      chain: chainId,
      limit: 10,
    });

    // chek if any of the nfts is the one we are looking for
    const nft = nftsBalances.raw.result.find((nft: any) => nft.token_address === nftAddress);

    return nft !== undefined;

  }