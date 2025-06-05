from bip_utils import Bip39SeedGenerator, Bip49, Bip49Coins, Bip44Changes, Bip39Languages

LANG_MAP = {
    "english": Bip39Languages.ENGLISH,
    "japanese": Bip39Languages.JAPANESE,
    "spanish": Bip39Languages.SPANISH,
    "french": Bip39Languages.FRENCH,
    "italian": Bip39Languages.ITALIAN,
    "korean": Bip39Languages.KOREAN,
    "chinese_simplified": Bip39Languages.CHINESE_SIMPLIFIED,
    "chinese_traditional": Bip39Languages.CHINESE_TRADITIONAL,
    # Add any other languages your mnemonics might be in
}

def generate_bip49_address(mnemonic, lang_str, addr_data):
    lang_enum = LANG_MAP.get(lang_str.lower())
    if lang_enum is None:
        raise ValueError(f"Unsupported mnemonic language: {lang_str}")

    # Generate seed from mnemonic and language
    seed_bytes = Bip39SeedGenerator(mnemonic, lang_enum).Generate()

    # Generate BIP49 address
    bip49_ctx = Bip49.FromSeed(seed_bytes, Bip49Coins.BITCOIN)
    addr = bip49_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()

    return addr if addr_data.get(addr, None) else None
