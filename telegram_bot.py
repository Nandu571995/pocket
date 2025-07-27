from datetime import datetime, timedelta
from telegram import Bot
import asyncio
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def send_signal(asset, tf, direction, reason="Strategy Confirmed"):
    now = datetime.now()
    duration = int(tf.replace('m', ''))

    start_time = now.strftime("%H:%M")
    end_time = (now + timedelta(minutes=duration)).strftime("%H:%M")

    emoji = "🔴 RED (SELL)" if direction == "SELL" else "🟢 GREEN (BUY)"

    message = (
        f"📢 OTC Signal ({tf})\n"
        f"Pair: {asset}\n"
        f"Time: {start_time} - {end_time}\n"
        f"Direction: {emoji}\n"
        f"Reason: {reason}"
    )

    asyncio.run(bot.send_message(chat_id=CHAT_ID, text=message))

# Utility for thread-safe embedding
def start_telegram_bot():
    print("Telegram bot is embedded into signal system.")
