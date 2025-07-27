# File: telegram_bot.py
from datetime import datetime, timedelta
from telegram import Bot
import asyncio
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def send_signal(asset, tf, signal, reason="Strategy Triggered"):
    now = datetime.now()
    duration = int(tf.replace('m', ''))

    start_time = now.strftime("%H:%M")
    end_time = (now + timedelta(minutes=duration)).strftime("%H:%M")
    signal_emoji = "🔴 RED (SELL)" if signal == "SELL" else "🟢 GREEN (BUY)"

    message = (
        f"📢 OTC Signal ({tf})\n"
        f"Pair: {asset}\n"
        f"Time: {start_time} - {end_time}\n"
        f"Next Candle {tf}: {signal_emoji}\n"
        f"Reason: {reason}"
    )

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        asyncio.ensure_future(bot.send_message(chat_id=CHAT_ID, text=message))
    else:
        loop.run_until_complete(bot.send_message(chat_id=CHAT_ID, text=message))

def start_telegram_bot():
    print("Telegram bot is embedded into signal system.")
