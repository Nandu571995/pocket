# telegram_bot.py

from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

# Environment variables or fallback
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "8062898551:AAFp6Mzz3TU2Ngeqf4gL4KL55S1guuRwcnA"
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "1014815784"

bot = Bot(token=TELEGRAM_TOKEN)

def send_signal_telegram(signal):
    message = (
        f"📢 *{signal['timeframe']} Signal Alert!*\n"
        f"🪙 *Asset:* `{signal['asset']}`\n"
        f"🎯 *Direction:* {signal['direction']}\n"
        f"🧠 *Confidence:* {signal['confidence']}%\n"
        f"📊 *Reason:* {signal['reason']}\n"
        f"🕒 *Time:* {signal['timestamp']}"
    )
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Trading Bot is live!")

def run_telegram_bot_background():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    print("✅ Telegram listener started in background...")
    updater.start_polling()
    # DO NOT CALL `updater.idle()` here or it will block everything
