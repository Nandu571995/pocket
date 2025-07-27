from datetime import datetime, timedelta
from telegram import Bot
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=BOT_TOKEN)

def send_signal(asset, tf, signal):
    now = datetime.now()
    duration = int(tf.replace('m', ''))

    start_time = now.strftime("%H:%M")
    end_time = (now + timedelta(minutes=duration)).strftime("%H:%M")
    signal_emoji = "🔴 RED (SELL)" if signal == "SELL" else "🟢 GREEN (BUY)"

    message = (
        f"📢 OTC Signal ({tf})\n"
        f"Pair: {asset}\n"
        f"Time: {start_time} - {end_time}\n"
        f"Next Candle {tf}: {signal_emoji}"
    )

    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"❌ Telegram error: {e}")

def start_telegram_bot():
    print("Telegram bot is embedded into signal system.")
