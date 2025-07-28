import os
import threading
from pocket_bot import start_pocket_bot
from telegram_bot import run_telegram_bot_background
import subprocess

def run_dashboard():
    subprocess.run([
        "streamlit", "run", "dashboard.py",
        "--server.port", "10000",
        "--server.address", "0.0.0.0"
    ])

if __name__ == "__main__":
    print("📦 Starting Pocket Option Bot System...")

    # ✅ Start pocket bot in background
    threading.Thread(target=start_pocket_bot, daemon=True).start()

    # ✅ Start telegram bot in background WITHOUT updater.idle()
    threading.Thread(target=run_telegram_bot_background, daemon=True).start()

    # ✅ Start Streamlit dashboard in main thread
    run_dashboard()
