from bip_utils import Bip39SeedGenerator, Bip49, Bip49Coins, Bip44Changes, Bip39Languages

LANG_MAP = {
    "chinese_simplified" : Bip39Languages.CHINESE_SIMPLIFIED,
    "chinese_traditional" : Bip39Languages.CHINESE_TRADITIONAL,
    "czech" : Bip39Languages.CZECH,
    "english" : Bip39Languages.ENGLISH,
    "french" : Bip39Languages.FRENCH,
    "italian" : Bip39Languages.ITALIAN,
    "korean" : Bip39Languages.KOREAN,
    "portuguese" : Bip39Languages.PORTUGUESE,
    "spanish" : Bip39Languages.SPANISH,
    # Add any other languages your mnemonics might be in
}

def generate_bip49_address(mnemonic, lang_str, addr_data):
    lang_enum = LANG_MAP.get(lang_str.lower())
    
    if lang_enum is None:
        print(f"Skipping unsupported language: {lang_str}")
        return None
    
    # Generate seed from mnemonic and language
    seed_bytes = Bip39SeedGenerator(mnemonic, lang_enum).Generate()

    # Generate BIP49 address
    bip49_ctx = Bip49.FromSeed(seed_bytes, Bip49Coins.BITCOIN)
    addr = bip49_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()

    return addr if addr_data.get(addr, None) else None
