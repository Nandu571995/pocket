from datetime import datetime, timedelta
from telegram import Bot
import asyncio
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_signal(asset, tf, signal):
    now = datetime.now()
    start_time = now.strftime("%H:%M")
    end_time = (now + timedelta(minutes=1)).strftime("%H:%M")
    
    signal_emoji = "🔴 RED (SELL)" if signal == "SELL" else "🟢 GREEN (BUY)"
    
    message = (
        f"📢 OTC Signal\n"
        f"Pair: {asset}\n"
        f"Time: {start_time} - {end_time}\n"
        f"Next Candle 1 min: {signal_emoji}"
    )

    bot = Bot(token=BOT_TOKEN)
    asyncio.run(bot.send_message(chat_id=CHAT_ID, text=message))

# ✅ Dummy function to avoid import error
def start_telegram_bot():
    print("Telegram bot is a utility, no need to run separately.")
