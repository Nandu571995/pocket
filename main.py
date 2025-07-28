# File: main.py
import threading
from pocket_bot import start_pocket_bot
from telegram_bot import start_telegram_bot
from dashboard import run_dashboard

if __name__ == "__main__":
    threading.Thread(target=start_telegram_bot, daemon=True).start()
    threading.Thread(target=start_pocket_bot, daemon=True).start()
    run_dashboard()
