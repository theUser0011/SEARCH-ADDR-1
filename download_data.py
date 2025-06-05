import gdown
import pickle
import json
import os

def get_json_data():
        
    id = '1Sc841jM8uRce8s00APPLjGiCMMeCLfT7'
    title = 'data.json'


    # Google Drive download URL
    url = f'https://drive.google.com/uc?id={id}'
    print(f"Trying to download: {title} from {url}")

    try:
        gdown.download(url, output=title, quiet=False)
    except Exception as e:
        print(f"Skipping {title} due to error: {e}")
    with open("data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data