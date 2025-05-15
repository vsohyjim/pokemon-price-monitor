import discord
import asyncio
import os
import threading
from flask import Flask

# === CONFIG DISCORD ===
DISCORD_TOKEN = "MTM3MTU0MDMwNzE5MTEzNjQ2Ng.Gw7R7H.glajES6u9HPU0skz1MgLkMcW9RN53-HD9dY_KA"
SOURCE_CHANNEL_ID = 1332865315859726342
ALERT_CHANNEL_ID = 1371547563060232314
KEYWORDS = ["fnac", "151"]
CHECK_INTERVAL = 5  # secondes

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Pour stocker les IDs des messages déjà lus
seen_message_ids = set()

async def check_messages():
    await client.wait_until_ready()
    print("🎯 Bot connecté et prêt")
    while not client.is_closed():
        try:
            source_channel = client.get_channel(SOURCE_CHANNEL_ID)
            alert_channel = client.get_channel(ALERT_CHANNEL_ID)
            if source_channel and alert_channel:
                messages = await source_channel.history(limit=10).flatten()
                for msg in messages:
                    if msg.id not in seen_message_ids:
                        content_lower = msg.content.lower()
                        if all(k in content_lower for k in KEYWORDS):
                            await alert_channel.send("Pokemon 151 Bundle Restock ! 🔥")
                            print(f"✅ Message détecté : {msg.content}")
                        seen_message_ids.add(msg.id)
            else:
                print("⚠️ Channels non trouvés")
        except Exception as e:
            print(f"[ERREUR] {e}")
        await asyncio.sleep(CHECK_INTERVAL)

# === FLASK POUR KEEP-ALIVE RAILWAY ===
app = Flask(__name__)

@app.route("/")
def index():
    return "🟢 Bot Discord 151 actif"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# === LANCEMENT FLASK + DISCORD ===
threading.Thread(target=run_flask).start()

@client.event
async def on_ready():
    print(f"🔗 Connecté en tant que {client.user}")
    client.loop.create_task(check_messages())

client.run(DISCORD_TOKEN)
