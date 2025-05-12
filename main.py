import requests
import time
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = "https://store.fcbarcelona.com/fr/products/fc-barcelona-ldts-away-shirt-24-25?country=FR"
CHECK_INTERVAL = 3  # en secondes
PRODUCT_ID = "fc-barcelona-ldts-away-shirt-24-25"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Pragma": "no-cache",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.8"
}

notified_sizes = set()

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

print("🟢 Bot Travis Scott lancé...")

while True:
    check_stock()
    time.sleep(CHECK_INTERVAL)
