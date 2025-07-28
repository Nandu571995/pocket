# telegram_bot.py

import os
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Load from environment or fallback
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8330981377:AAH3GUheRzKgpd4NDx0cIIGo4FVs1PDMyTA")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1014815784")

bot = Bot(token=TELEGRAM_TOKEN)

def send_signal_telegram(signal: dict):
    """
    Send a formatted trading signal to Telegram.
    """
    message = (
        f"📢 *{signal['timeframe']} Signal Alert!*\n"
        f"🪙 *Asset:* `{signal['asset']}`\n"
        f"🎯 *Direction:* {signal['direction']}\n"
        f"🧠 *Confidence:* {signal['confidence']}%\n"
        f"📊 *Reason:* {signal['reason']}\n"
        f"🕒 *Time:* {signal['timestamp']}`"
    )
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Trading Bot is live and running!")

def start_telegram_bot():
    """
    Run in foreground (for dev).
    """
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    print("✅ Telegram bot is listening...")
    updater.start_polling()
    updater.idle()

def run_telegram_bot_background():
    """
    Run in background (for deployment).
    """
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()  # No idle() here

