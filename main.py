# main.py

import os
import threading
import subprocess

from pocket_bot import start_pocket_bot
from telegram_bot import run_telegram_bot_background

def run_dashboard():
    subprocess.run([
        "streamlit", "run", "dashboard.py",
        "--server.port", "10000",
        "--server.address", "0.0.0.0"
    ])

if __name__ == "__main__":
    print("📦 Starting Pocket Option Bot System...")

    threading.Thread(target=start_pocket_bot, daemon=True).start()
    threading.Thread(target=run_telegram_bot_background, daemon=True).start()

    # Dashboard stays in foreground
    run_dashboard()
