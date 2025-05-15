import discord
import asyncio
import os
import threading
from flask import Flask

# === CONFIG ===
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SOURCE_CHANNEL_ID_STR = os.getenv("SOURCE_CHANNEL_ID")
ALERT_CHANNEL_ID_STR = os.getenv("ALERT_CHANNEL_ID")

print("DEBUG TOKEN:", DISCORD_TOKEN)
print("DEBUG SOURCE_CHANNEL_ID:", SOURCE_CHANNEL_ID_STR)
print("DEBUG ALERT_CHANNEL_ID:", ALERT_CHANNEL_ID_STR)

# ✅ Conversion après vérification
if not SOURCE_CHANNEL_ID_STR or not ALERT_CHANNEL_ID_STR:
    raise ValueError("❌ Les variables SOURCE_CHANNEL_ID ou ALERT_CHANNEL_ID sont manquantes.")

SOURCE_CHANNEL_ID = int(SOURCE_CHANNEL_ID_STR)
ALERT_CHANNEL_ID = int(ALERT_CHANNEL_ID_STR)
