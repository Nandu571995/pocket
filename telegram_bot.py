from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

# Config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "YOUR_REAL_TOKEN"
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "YOUR_REAL_CHAT_ID"

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
    update.message.reply_text("✅ Trading Bot is live and running!")

def run_telegram_bot_background():
    """
    For Render or background thread: polling without idle() to prevent blocking or error
    """
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    print("✅ Telegram bot is listening...")
    updater.start_polling()  # No .idle()

# For manual local testing
if __name__ == "__main__":
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()
