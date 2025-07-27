import threading
import time
from telegram_bot import start_telegram_bot, is_running
from pocket_bot import run_bot

def run_telegram():
    start_telegram_bot()

def run_trader():
    is_running["status"] = True  # Auto-run bot without needing /start
    run_bot()

if __name__ == "__main__":
    print("[INFO] Starting Telegram bot and trading engine...")
    threading.Thread(target=run_telegram, daemon=True).start()
    run_trader()
