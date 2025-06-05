from get_all_lang_address_for_seed import generate_bip49_address
from download_all_seeds_and_load import generate_mnemonics_multilang
from download_data import get_json_data
from pymongo import MongoClient
import os,time,traceback,requests

def get_telegram_config():
    key_doc = MongoClient(mongo_url)['STORING_KEYS']['tele_bot_1'].find_one()
    return {
        "token": key_doc['TELEGRAM_BOT_TOKEN'],
        "chat_id": key_doc['TELEGRAM_CHAT_ID'],
        "uname": key_doc['TELEGRAM_UNAME']
    }

def send_to_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{telegram_config['token']}/sendMessage"
        payload = {
            "chat_id": telegram_config['chat_id'],
            "text": msg,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"❌ Telegram send failed: {response.text}")
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")


def get_mnemonics_data(start):        
    return [
        generate_mnemonics_multilang(start, count=1, word_count=12),
        generate_mnemonics_multilang(start, count=1, word_count=15),
        generate_mnemonics_multilang(start, count=1, word_count=18),
        generate_mnemonics_multilang(start, count=1, word_count=21),
        generate_mnemonics_multilang(start, count=1, word_count=24),
    ]

# --- Setup ---
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client['START_DB']
collection = db['start_one']
doc_1 = collection.find_one({"doc_num": 1})
start_point = int(doc_1['start_point'])
addr_data = get_json_data()
telegram_config = get_telegram_config()





# --- Main Execution ---
num = start_point
start_time = time.time()
max_duration = 3 * 60 * 60  # 3 hours in seconds

try:
    while time.time() - start_time < max_duration:
        mnemonics_lst = get_mnemonics_data(num)
        for mnemonics in mnemonics_lst:    
            for lang, phrases in mnemonics.items():
                for phrase in phrases:
                    try:
                        address = generate_bip49_address(phrase, lang, addr_data)
                        
                        if address:
                            print(f"\n🔤 Language: {lang}")
                            print(f"🧠 Mnemonic: {phrase}")
                            print(f"🏦 Address: {address}")
                            
                            msg = (
                                f"🔔 *New BIP49 Address Found!*\n"
                                f"🌐 Language: `{lang}`\n"
                                f"🧠 Mnemonic: `{phrase}`\n"
                                f"🏦 Address: `{address}`"
                            )
                            send_to_telegram(msg)


                    except Exception as e:
                        print(f"❌ Error for {lang} mnemonic: {e}")
                        traceback.print_exc()
        num += 1

except Exception as e:
    print(f"\n🛑 Unhandled exception occurred: {e}")
    traceback.print_exc()

finally:
    print(f"\n💾 Saving progress at num={num}")
    collection.update_one({"doc_num": 1}, {"$set": {"start_point": num}})
