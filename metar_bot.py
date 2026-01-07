import os
import requests
from tweepy import Client
from datetime import datetime
import traceback

ICAO = "LTAC"
METAR_URL = f"https://aviationweather.gov/api/data/metar?ids={ICAO}&format=raw"
PREV_METAR_FILE = "prev_metar.txt"

def get_metar():
    r = requests.get(METAR_URL, timeout=10)
    if r.status_code == 200:
        return r.text.strip()
    else:
        print("METAR alınamadı! Status:", r.status_code)
        return None

def read_prev_metar():
    if os.path.exists(PREV_METAR_FILE):
        with open(PREV_METAR_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_metar(metar_text):
    with open(PREV_METAR_FILE, "w") as f:
        f.write(metar_text)

def tweet_metar(metar_text):
    try:
        client = Client(
            consumer_key=os.getenv("API_KEY"),
            consumer_secret=os.getenv("API_SECRET"),
            access_token=os.getenv("ACCESS_TOKEN"),
            access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
        )

        tweet_text = (
            f"✈️ {ICAO} METAR\n\n"
            f"{metar_text}\n\n"
            f"🕒 {datetime.utcnow().strftime('%d.%m.%Y %H:%M')} UTC"
        )

        client.create_tweet(text=tweet_text)
        print("Tweet başarıyla atıldı ✅")

    except Exception as e:
        print("Tweet atılamadı ❌")
        traceback.print_exc()

if __name__ == "__main__":
    print("Bot başladı")
    metar = get_metar()
    if not metar:
        print("Hata: METAR alınamadı")
        exit(1)

    prev_metar = read_prev_metar()
    if metar != prev_metar:
        tweet_metar(metar)
        save_metar(metar)
    else:
        print("METAR değişmemiş, tweet atılmadı 🛑")
