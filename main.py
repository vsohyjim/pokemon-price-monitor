import requests
import time
from bs4 import BeautifulSoup
import os

URL = "https://www.pokepixel.net/products/b0chbcsr4j-pokemon-asmodee-scarlet-et-violet-151-3-5-pack-of-6-booster-packs-151-board-games-card-games-playing-and-collecting-cards-ages-6"
AMAZON_LINK = "https://amazon.de/dp/B0CHBCSR4J"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Pragma": "no-cache",
    "Accept": "*/*"
}
last_price = 46.75

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }
    requests.post(url, data=data)

def get_price():
    res = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.find("meta", {"property": "og:price:amount"})
    return float(tag["content"].replace(",", ".")) if tag else None

print("🟢 Suivi activé")
while True:
    try:
        price = get_price()
        if price and price != last_price:
            msg = f"📦 Changement de prix !\n💶 Ancien : {last_price}€\n💸 Nouveau : {price}€\n🛒 {AMAZON_LINK}"
            send_telegram_message(msg)
            last_price = price
        else:
            print(f"✓ Aucun changement ({price}€)")
    except Exception as e:
        print("[ERREUR]", e)
    time.sleep(1)
