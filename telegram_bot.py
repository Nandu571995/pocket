# telegram_bot.py

import json
import time
import os
from telegram import Bot
from datetime import datetime

# Set your bot token and chat ID
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8062898551:AAFp6Mzz3TU2Ngeqf4gL4KL55S1guuRwcnA")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1014815784")

SIGNAL_FILE = "signals.json"
sent_signals = set()

def send_telegram_message(message):
    try:
        bot = Bot(token=BOT_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"✅ Sent to Telegram:\n{message}")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

def format_signal(signal):
    return f"""
📡 Signal #{signal['timeframe']}
Asset: {signal['symbol']}
🕒 Time: {signal['start']}–{signal['end']}
📊 Action: {signal['signal']}
✅ Confidence: {signal['confidence']}%
📅 Generated: {signal['timestamp']}
""".strip()

def start_telegram_bot():
    print("📨 Telegram bot started...")
    while True:
        try:
            if os.path.exists(SIGNAL_FILE):
                with open(SIGNAL_FILE, "r") as f:
                    signals = json.load(f)

                for signal in signals[-20:]:
                    signal_id = f"{signal['symbol']}-{signal['start']}-{signal['timeframe']}"
                    now = datetime.now().strftime("%H:%M")

                    # Send only if not sent before and at least 30 sec to 1 min before signal time
                    if signal_id not in sent_signals:
                        scheduled_time = signal['start']
                        if now < scheduled_time:
                            message = format_signal(signal)
                            send_telegram_message(message)
                            sent_signals.add(signal_id)
            time.sleep(10)
        except Exception as e:
            print(f"Telegram bot loop error: {e}")
            time.sleep(5)
