import os
from telegram import Bot, ParseMode, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Set your bot token and chat ID
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8062898551:AAFp6Mzz3TU2Ngeqf4gL4KL55S1guuRwcnA")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1014815784")

# Initialize bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_signal_telegram(message: str):
    """Send a message to the Telegram bot."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode=ParseMode.MARKDOWN)
        print("✅ Telegram alert sent.")
    except Exception as e:
        print(f"⚠️ Telegram send error: {e}")

# Optional: command to test bot or extend with more controls
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="🤖 Pocket Bot is running!")

def start_telegram_bot():
    try:
        updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        updater.start_polling()
        print("📲 Telegram bot started...")
    except Exception as e:
        print(f"⚠️ Telegram Monitoring Error: {e}")
