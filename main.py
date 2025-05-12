import requests

# ✅ Renseigne tes infos ici en dur pour le test
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message():
    message = (
        "✅ *Test réussi !*\n"
        "Le bot est bien connecté à Telegram.\n\n"
        "🔥 Prêt à traquer le maillot Travis Scott."
    )
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(telegram_url, data=data)
    if response.status_code == 200:
        print("📨 Message envoyé avec succès ✅")
    else:
        print(f"❌ Erreur lors de l'envoi : {response.status_code}")
        print(response.text)

# 🔁 Test d’envoi immédiat
send_telegram_message()
