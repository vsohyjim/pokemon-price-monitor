import requests
import time
from bs4 import BeautifulSoup
import os
import threading
from flask import Flask

# === CONFIG ===
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

# === TELEGRAM ===
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "disable_web_page_preview": False}
    requests.post(url, data=data)

# === PRIX ===
def get_price():
    res = requests.get(URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.find("meta", {"property": "og:price:amount"})
    return float(tag["content"].replace(",", ".")) if tag else None

# === MONITORING LOOP ===
def monitor():
    global last_price
    print("🟢 Suivi du prix lancé...")
    while True:
        try:
            price = get_price()
            if price != last_price:
                msg = f"📦 Prix changé !\nAncien : {last_price}€\nNouveau : {price}€\n🛒 {AMAZON_LINK}"
                send_telegram_message(msg)
                last_price = price
            else:
                print(f"✓ Aucun changement ({price}€)")
        except Exception as e:
            print("Erreur :", e)
        time.sleep(3)

# === FLASK KEEP-ALIVE ===
app = Flask('')
@app.route('/')
def home():
    return "Bot Pokémon actif ✅"

def run_server():
    app.run(host='0.0.0.0', port=8080)

# === LANCEMENT DES THREADS ===
threading.Thread(target=monitor).start()
threading.Thread(target=run_server).start()
