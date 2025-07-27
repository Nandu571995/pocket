import os
import asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def telegram_polling():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

def start_telegram_bot():
    asyncio.run(telegram_polling())

def send_signal(asset, tf, signal):
    text = f"📢 OTC Signal\nAsset: {asset}\nTF: {tf}\nAction: {signal}"
    bot = Bot(token=BOT_TOKEN)
    asyncio.run(bot.send_message(chat_id=CHAT_ID, text=text))
