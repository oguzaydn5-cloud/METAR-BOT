import os
import requests
from tweepy import Client
from datetime import datetime
import traceback

ICAO = "LTAC"
NAME = "Ankara Esenboğa"

# API URL'leri
METAR_URL = f"https://aviationweather.gov/api/data/metar?ids={ICAO}&format=raw&taf=true&hours=0"
SIGMET_URL = "https://aviationweather.gov/api/data/sigmet?fir=LTAA,LGGG"

PREV_DATA_FILE = "prev_data.txt"

def get_metar_taf():
    try:
        r = requests.get(METAR_URL, timeout=10)
        if r.status_code == 200:
            text = r.text.strip()
            return text if text else "METAR/TAF verisi henüz yok."
        else:
            print("METAR/TAF alınamadı! Status:", r.status_code)
            return None
    except Exception as e:
        print("METAR/TAF hatası:", e)
        return None

def get_sigmet():
    try:
        r = requests.get(SIGMET_URL, timeout=10)
        if r.status_code == 200:
            text = r.text.strip().upper()
            if "NO SIGMET" in text or not text:
                return None
            return "⚠️ AKTİF SIGMET:\n" + r.text.strip()
        else:
            return None
    except Exception as e:
        print("SIGMET hatası:", e)
        return None

def read_prev_data():
    if os.path.exists(PREV_DATA_FILE):
        with open(PREV_DATA_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def save_data(data_text):
    with open(PREV_DATA_FILE, "w", encoding="utf-8") as f:
        f.write(data_text)

def tweet_content(content):
    try:
        client = Client(
            consumer_key=os.getenv("API_KEY"),
            consumer_secret=os.getenv("API_SECRET"),
            access_token=os.getenv("ACCESS_TOKEN"),
            access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
        )

        tweet_text = (
            f"✈️ {NAME} ({ICAO})\n\n"
            f"{content}\n\n"
            f"🕒 {datetime.utcnow().strftime('%d.%m.%Y %H:%M')} UTC\n"
            f"#METAR #TAF #Havacılık"
        )

        # Karakter sınırı
        if len(tweet_text) > 280:
            tweet_text = tweet_text[:277] + "..."

        client.create_tweet(text=tweet_text)
        print("Tweet başarıyla atıldı ✅")

    except Exception as e:
        print("Tweet atılamadı ❌")
        traceback.print_exc()

if __name__ == "__main__":
    print("Bot başladı - Trigger:", os.getenv("GITHUB_EVENT_NAME"))

    metar_taf = get_metar_taf()
    if not metar_taf:
        print("Hata: METAR/TAF alınamadı")
        exit(1)

    sigmet = get_sigmet()

    # Tweet içeriğini oluştur
    content_parts = [metar_taf]
    if sigmet:
        content_parts.append("\n" + sigmet)

    current_content = "\n\n".join(content_parts)

    prev_content = read_prev_data()

    if current_content != prev_content:
        tweet_content(current_content)
        save_data(current_content)
        print("Yeni veri tespit edildi, tweet atıldı ve kaydedildi.")
    else:
        print("Veri değişmemiş, tweet atılmadı 🛑")
