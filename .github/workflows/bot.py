import requests
import tweepy
import os
from datetime import datetime, timezone

# GitHub Secrets'tan anahtarları çek
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

# Tweepy client
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Tek havalimanı (istediğin gibi değiştir)
ICAO = "LTAC"
NAME = "Ankara Esenboğa"

def get_metar_taf(icao):
    url = f"https://aviationweather.gov/api/data/metar?ids={icao}&format=raw&taf=true&hours=0"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            text = r.text.strip()
            if text:
                return text
            else:
                return "METAR/TAF verisi henüz yok."
        else:
            return f"Veri alınamadı (HTTP {r.status_code})"
    except Exception as e:
        return f"Bağlantı hatası: {str(e)}"

# Veri çek ve tweet hazırla
data = get_metar_taf(ICAO)
current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
tweet = f"✈️ {NAME} ({ICAO})\n\n{data}\n\nGüncelleme: {current_time}\n#METAR #TAF #Havacılık"

if len(tweet) > 280:
    tweet = tweet[:277] + "..."

# Tweet at
try:
    response = client.create_tweet(text=tweet)
    print(f"✓ Tweet atıldı! ID: {response.data['id']}")
except Exception as e:
    print(f"✗ Hata: {e}")
