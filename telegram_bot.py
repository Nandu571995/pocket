# telegram_bot.py

import os
import requests
from datetime import datetime, timedelta

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token_here")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "your_chat_id_here")

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload)
        if not response.ok:
            print("Telegram send error:", response.text)
    except Exception as e:
        print(f"Telegram Exception: {e}")

def format_signal_message(asset, timeframe, signal, reason, confidence):
    now = datetime.utcnow() + timedelta(minutes=1)  # 1 min ahead to give user time
    start = now.strftime('%H:%M')
    end = (now + timedelta(minutes=1)).strftime('%H:%M') if timeframe == 1 else (now + timedelta(minutes=timeframe)).strftime('%H:%M')

    color = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "⚪"
    
    message = (
        f"📡 *Pocket Option Signal*\n"
        f"{color} *{signal}* | `{asset}` | *{timeframe} min*\n"
        f"🕒 *Next Candle*: `{start}–{end}`\n"
        f"📊 *Confidence*: `{confidence}%`\n"
        f"🔍 *Reason*: _{reason}_"
    )
    return message
