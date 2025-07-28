from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

# Config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "8062898551:AAFp6Mzz3TU2Ngeqf4gL4KL55S1guuRwcnA"
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "1014815784"

bot = Bot(token=TELEGRAM_TOKEN)

def send_signal_telegram(signal):
    """
    Send a trading signal to Telegram in formatted style.
    """
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
    Starts the Telegram bot in background thread for Render-safe execution.
    """
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    print("✅ Telegram bot is listening...")
    updater.start_polling()  # Do NOT call idle() in threads

# Test locally
if __name__ == "__main__":
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    print("✅ Telegram bot is running locally...")
    updater.start_polling()
    updater.idle()
