import requests
import time
import threading
from flask import Flask

# === CONFIGURATION FIXE ===
TELEGRAM_TOKEN = "7955874330:AAGMas9suuaSvlfMO63H3peuav8s_heyB7Q"
TELEGRAM_CHAT_ID = "-4603633681"

PRODUCT_URL = "https://store.fcbarcelona.com/fr/products/fc-barcelona-ldts-away-shirt-24-25?country=FR"
PRODUCT_ID = "fc-barcelona-ldts-away-shirt-24-25"
CHECK_INTERVAL = 2  # en secondes

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Pragma": "no-cache",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.8"
}

notified_sizes = set()

# === ENVOI DE NOTIF TELEGRAM ===
def send_telegram_message(size):
    message = (
        f"🔥 Maillot *Travis Scott* dispo en taille *{size}* !\n\n"
        f"🛒 [Clique ici pour acheter]({PRODUCT_URL})"
    )
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        res = requests.post(telegram_url, data=data)
        if res.status_code == 200:
            print(f"✅ Alerte envoyée pour la taille {size}")
        else:
            print(f"❌ Erreur Telegram : {res.status_code} - {res.text}")
    except Exception as e:
        print("[Erreur Telegram]", e)

# === CHECK STOCK SHOPIFY ===
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
                send_telegram_message(size)
                notified_sizes.add(size)
                print(f"[🟢 ALERTE] {size} dispo")
            else:
                print(f"🔍 Taille {size} : {'✅' if available else '❌'}")
    except Exception as e:
        print("[Erreur lors du check]", e)

# === THREAD DU BOT ===
def monitor_loop():
    print("🟢 Bot Travis Scott actif")
    while True:
        check_stock()
        time.sleep(CHECK_INTERVAL)

# === SERVEUR FLASK POUR GARDER EN LIGNE SUR RAILWAY ===
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Bot Travis Scott en ligne ✅"

def run_server():
    app.run(host="0.0.0.0", port=8080)

# === LANCEMENT DES 2 THREADS (bot + serveur Flask) ===
threading.Thread(target=monitor_loop).start()
threading.Thread(target=run_server).start()
