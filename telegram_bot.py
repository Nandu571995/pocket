from telegram.ext import Updater, CommandHandler
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your-token-here")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "your-chat-id")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot is active!")

def start_telegram_bot():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    # Webhook URL
    APP_NAME = "pocket-c948"  # Your Render subdomain
    PORT = int(os.environ.get('PORT', '8080'))
    WEBHOOK_URL = f"https://{APP_NAME}.onrender.com/{TELEGRAM_BOT_TOKEN}"

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_BOT_TOKEN,
        webhook_url=WEBHOOK_URL
    )

    print("✅ Telegram bot webhook started...")
    updater.idle()
