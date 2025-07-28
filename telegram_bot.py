# telegram_bot.py
from telegram import Bot, ParseMode
from telegram.ext import Updater, CommandHandler
import logging
import os

# Replace with your actual values
TELEGRAM_TOKEN = "8062898551:AAFp6Mzz3TU2Ngeqf4gL4KL55S1guuRwcnA"
CHAT_ID = "1014815784"

# Init bot
bot = Bot(token=TELEGRAM_TOKEN)

def send_telegram_signal(message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print("❌ Telegram Error:", e)

def start(update, context):
    update.message.reply_text("🤖 Pocket Option Signal Bot is Active!")

def start_telegram_bot():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    print("✅ Telegram bot started")
    updater.idle()
