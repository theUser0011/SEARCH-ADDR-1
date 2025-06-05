import hashlib
import json, os, shutil
import requests

# List of BIP-39 language files and corresponding short names
language_files = {
    "english": "bip39_english.txt",
    "chinese_simplified": "bip39_chinese_simplified.txt",
    "chinese_traditional": "bip39_chinese_traditional.txt",
    "french": "bip39_french.txt",
    "italian": "bip39_italian.txt",
    # "japanese": "bip39_japanese.txt",
    "korean": "bip39_korean.txt",
    "spanish": "bip39_spanish.txt"
}

base_url = "https://raw.githubusercontent.com/input-output-hk/rust-byron-cardano/master/cardano/src/bip/"

# Download and load wordlists
wordlists = {}
for lang, filename in language_files.items():
    if not os.path.exists(filename):
        url = base_url + filename
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)  # Corrected: save the raw text directly
        # print(f"✅ Downloaded: {filename}")

    # ✅ Load wordlist from JSON array
    with open(filename, "r", encoding="utf-8-sig") as f:
        wordlists[lang] = json.load(f)


# --- Original functions remain unchanged ---
def get_checksum_bits(entropy_bytes):
    sha256_hash = hashlib.sha256(entropy_bytes).digest()
    checksum_length = len(entropy_bytes) * 8 // 32
    return bin(int.from_bytes(sha256_hash, "big"))[2:].zfill(256)[:checksum_length]

def entropy_to_mnemonic(entropy_bytes, wordlist):
    entropy_bits = bin(int.from_bytes(entropy_bytes, 'big'))[2:].zfill(len(entropy_bytes) * 8)
    checksum_bits = get_checksum_bits(entropy_bytes)
    full_bits = entropy_bits + checksum_bits
    words = [wordlist[int(full_bits[i:i+11], 2)] for i in range(0, len(full_bits), 11)]
    return ' '.join(words)

def remove_chars(s, chars_to_remove):
    for char in chars_to_remove:
        s = s.replace(char, '')
    return s

# ✅ Main function to generate mnemonics for all languages
def generate_mnemonics_multilang(start, count=1, word_count=12):
    word_to_entropy_bits = {
        12: 128,
        15: 160,
        18: 192,
        21: 224,
        24: 256
    }

    if word_count not in word_to_entropy_bits:
        raise ValueError("word_count must be one of [12, 15, 18, 21, 24]")

    entropy_len_bytes = word_to_entropy_bits[word_count] // 8
    results = {lang: [] for lang in wordlists.keys()}

    for offset in range(count):
        entropy = (start + offset).to_bytes(entropy_len_bytes, byteorder='big')
        for lang, wl in wordlists.items():
            mnemonic = entropy_to_mnemonic(entropy, wl)
            results[lang].append(mnemonic)

    return results

