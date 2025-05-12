import requests
import time
import os
import threading
from flask import Flask

# === CONFIG ===
TELEGRAM_TOKEN = os.getenv("7955874330:AAGMas9suuaSvlfMO63H3peuav8s_heyB7Q")
TELEGRAM_CHAT_ID = os.getenv("-4603633681")
URL = "https://store.fcbarcelona.com/fr/products/fc-barcelona-ldts-away-shirt-24-25?country=FR"
CHECK_INTERVAL = 3  # secondes
PRODUCT_ID = "fc-barcelona-ldts-away-shirt-24-25"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Pragma": "no-cache",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.8"
}

notified_sizes = set()

# === TELEGRAM NOTIF ===
def send_telegram_message(size):
    message = (
        f"🔥 Maillot Travis Scott disponible en taille *{size}* !\n\n"
        f"🔗 [Clique ici pour l'acheter]({URL})"
    )
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    requests.post(telegram_url, data=data)

# === STOCK CHECK ===
def check_stock():
    json_url = f"https://store.fcbarcelona.com/products/{PRODUCT_ID}.js"
    try:
        response = requests.get(json_url, headers=HEADERS, timeout=10)
        data = response.json()
        variants = data.get("variants", [])
        for v in variants:
            size = v.get("public_title")
            available = v.get("available")
            if available and size not in notified_sizes:
                print(f"[ALERTE] Taille dispo : {size}")
                send_telegram_message(size)
                notified_sizes.add(size)
            else:
                print(f"🔍 Taille {size} : {'✅' if available else '❌'}")
    except Exception as e:
        print("[Erreur]", e)

def monitoring_loop():
    print("🟢 Bot Travis Scott lancé...")
    while True:
        check_stock()
        time.sleep(CHECK_INTERVAL)

# === FLASK SERVER POUR GARANTIR LE UPTIME ===
app = Flask(__name__)

@app.route('/')
def home():
    return "🟣 Bot Travis Scott actif ✅"

def run_server():
    app.run(host="0.0.0.0", port=8080)

# === THREADS ===
threading.Thread(target=monitoring_loop).start()
threading.Thread(target=run_server).start()
