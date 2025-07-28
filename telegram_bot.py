# telegram_bot.py

from telegram import Bot
import threading
import json
import time
from datetime import datetime

TELEGRAM_TOKEN = "8062898551:AAFp6Mzz3TU2Ngeqf4gL4KL55S1guuRwcnA"
CHAT_ID = "1014815784"

bot = Bot(token=TELEGRAM_TOKEN)

def send_signal_telegram(signal):
    msg = (
        f"📊 Signal #{signal.get('id', 'N/A')}\n"
        f"📌 Asset: {signal.get('pair')}\n"
        f"🕒 Timeframe: {signal.get('timeframe')} min\n"
        f"📈 Direction: {signal.get('direction', '').upper()}\n"
        f"✅ Confidence: {signal.get('confidence', 0)}%\n"
        f"📅 Time: {signal.get('timestamp')}\n"
        f"🧠 Reason: {signal.get('reason')}"
    )
    try:
        bot.send_message(chat_id=CHAT_ID, text=msg)
        print(f"✅ Sent to Telegram: {msg}")
