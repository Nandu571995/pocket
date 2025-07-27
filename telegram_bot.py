import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))
is_running = {"status": False}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_running["status"] = True
    await context.bot.send_message(chat_id=CHAT_ID, text="✅ Trading bot started.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_running["status"] = False
    await context.bot.send_message(chat_id=CHAT_ID, text="⛔ Trading bot stopped.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🟢 Running" if is_running["status"] else "🔴 Stopped"
    await context.bot.send_message(chat_id=CHAT_ID, text=f"Bot status: {msg}")

def start_telegram_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("status", status))
    app.run_polling()
