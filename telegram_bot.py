from telegram import Bot, ParseMode
from telegram.ext import Updater, CommandHandler
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="🤖 Pocket Option Bot is Active!")

def send_signal_to_telegram(message: str):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)
        print(f"📩 Sent to Telegram: {message}")
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")

def start_telegram_bot():
    try:
        updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        print("📡 Telegram Bot started polling...")
        updater.start_polling()
    except Exception as e:
        print(f"❌ Telegram polling error: {e}")
