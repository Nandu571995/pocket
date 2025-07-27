import threading
import subprocess
import os

from telegram_bot import start_telegram_bot
from pocket_bot import start_pocket_bot

def start_streamlit_dashboard():
    port = os.environ.get("PORT", "10000")
    subprocess.Popen(["streamlit", "run", "dashboard.py", "--server.port", port])

if __name__ == "__main__":
    threading.Thread(target=start_telegram_bot).start()
    threading.Thread(target=start_pocket_bot).start()
    start_streamlit_dashboard()
