from bip_utils import Bip39SeedGenerator, Bip49, Bip49Coins, Bip44Changes
import hashlib




def generate_bip49_address(mnemonic, lang,addr_data):
    # Generate seed from mnemonic
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    # Use BIP49 to generate a legacy P2SH-P2WPKH address (starts with 3)
    bip49_ctx = Bip49.FromSeed(seed_bytes, Bip49Coins.BITCOIN)

    # Derive first external address: m/49'/0'/0'/0/0
    addr = bip49_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()

    return addr if addr_data.get(addr,None) else None


