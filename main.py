# main.py

import time
import threading
from pocket_bot import PocketBot
from telegram_bot import TelegramBot
from dashboard import run_dashboard
from signals_utils import validate_signals_loop

if __name__ == "__main__":
    # Initialize components
    bot = PocketBot()
    telegram = TelegramBot()

    def signal_loop():
        while True:
            signals = bot.generate_signals()
            if signals:
                for signal in signals:
                    telegram.send_signal(signal)
            time.sleep(60)  # Run every minute

    # Run signal loop in background
    signal_thread = threading.Thread(target=signal_loop, daemon=True)
    signal_thread.start()

    # Run validation loop (for signal performance)
    validation_thread = threading.Thread(target=validate_signals_loop, daemon=True)
    validation_thread.start()

    # Run Streamlit dashboard
    run_dashboard()
