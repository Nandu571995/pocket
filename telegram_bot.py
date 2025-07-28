# telegram_bot.py

from telegram import Bot
from telegram.ext import Updater
import threading
import json
import time
from datetime import datetime

TELEGRAM_TOKEN = "8062898551:AAFp6Mzz3TU2Ngeqf4gL4KL55S1guuRwcnA"
CHAT_ID = "1014815784"

bot = Bot(token=TELEGRAM_TOKEN)

def send_telegram_signal(signal):
    msg = (
        f"📊 Signal #{signal['id']}\n"
        f"📌 Asset: {signal['pair']}\n"
        f"🕒 Timeframe: {signal['timeframe']} min\n"
        f"📈 Direction: {signal['direction'].upper()}\n"
        f"✅ Confidence: {signal['confidence']}%\n"
        f"📅 Time: {signal['timestamp']}\n"
        f"🧠 Reason: {signal['reason']}"
    )
    bot.send_message(chat_id=CHAT_ID, text=msg)

def monitor_signals():
    last_sent = set()
    while True:
        try:
            with open("signals.json", "r") as f:
                data = json.load(f)
                for signal in data:
                    signal_id = signal.get("id")
                    if signal_id not in last_sent:
                        send_telegram_signal(signal)
                        last_sent.add(signal_id)
        except Exception as e:
            print("❌ Telegram error:", e)
        time.sleep(10)

def start_telegram_bot():
    print("✅ Telegram bot is running...")
    monitor_signals()
