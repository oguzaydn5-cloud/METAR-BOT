import os
import requests
import tweepy
from datetime import datetime
import traceback

try:
    print("Bot başladı")

    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

    print("API Key var mı:", bool(API_KEY))

    ICAO = "LTAC"
    METAR_URL = f"https://aviationweather.gov/api/data/metar?ids={ICAO}&format=raw"

    r = requests.get(METAR_URL, timeout=10)
    print("METAR HTTP Status:", r.status_code)
    print("METAR DATA:", r.text)

    auth = tweepy.OAuth1UserHandler(
        API_KEY,
        API_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)

    tweet = f"✈️ {ICAO} METAR\n\n{r.text.strip()}"
    api.update_status(tweet)

    print("Tweet başarıyla atıldı")

except Exception as e:
    print("HATA VAR ❌")
    traceback.print_exc()
    exit(1)
