import requests
import tweepy
import os
from datetime import datetime, timezone

# GitHub Secrets'tan anahtarları çek
client = tweepy.Client(
    bearer_token=os.getenv('BEARER_TOKEN'),
    consumer_key=os.getenv('CONSUMER_KEY'),
    consumer_secret=os.getenv('CONSUMER_SECRET'),
    access_token=os.getenv('ACCESS_TOKEN'),
    access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')
)

ICAO = "LTAC"
NAME = "Ankara Esenboğa"

def get_metar_taf(icao):
    url = f"https://aviationweather.gov/api/data/metar?ids={icao}&format=raw&taf=true&hours=0"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.text.strip() or "Veri henüz yok."
        else:
            return f"HTTP hatası: {r.status_code}"
    except Exception as e:
        return f"Bağlantı hatası: {str(e)}"

data = get_metar_taf(ICAO)
current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
tweet = f"✈️ {NAME} ({ICAO})\n\n{data}\n\nGüncelleme: {current_time}\n#METAR #TAF #Havacılık"

if len(tweet) > 280:
    tweet = tweet[:277] + "..."

client.create_tweet(text=tweet)
print("✓ Tweet atıldı!")
