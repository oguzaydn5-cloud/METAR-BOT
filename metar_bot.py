import requests
import tweepy
from datetime import datetime

# ==============================
# TWITTER (X) API BİLGİLERİ
# ==============================
API_KEY = "API_KEYİN"
API_SECRET = "API_SECRETİN"
ACCESS_TOKEN = "ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "ACCESS_TOKEN_SECRET"

# ==============================
# METAR AYARLARI
# ==============================
ICAO = "LTAC"
METAR_URL = f"https://aviationweather.gov/api/data/metar?ids={ICAO}&format=raw"

# ==============================
# METAR ÇEK
# ==============================
def get_metar():
    response = requests.get(METAR_URL, timeout=10)
    if response.status_code == 200 and response.text.strip():
        return response.text.strip()
    else:
        return None

# ==============================
# TWEET AT
# ==============================
def tweet_metar(metar):
    auth = tweepy.OAuth1UserHandler(
        API_KEY,
        API_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)

    tweet_text = (
        f"✈️ {ICAO} METAR\n\n"
        f"{metar}\n\n"
        f"🕒 {datetime.utcnow().strftime('%d.%m.%Y %H:%M')} UTC"
    )

    api.update_status(tweet_text)
    print("Tweet atıldı!")

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    metar = get_metar()
    if metar:
        tweet_metar(metar)
    else:
        print("METAR alınamadı.")
