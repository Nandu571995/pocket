import threading
import subprocess
from telegram_bot import start_telegram_bot
from pocket_bot import start_pocket_bot

def start_streamlit_dashboard():
    subprocess.Popen(["streamlit", "run", "dashboard.py", "--server.port", "10000"])  # use a non-conflicting port

if __name__ == "__main__":
    # ✅ Don't start keep_alive (conflict with streamlit)
    threading.Thread(target=start_telegram_bot).start()
    threading.Thread(target=start_pocket_bot).start()

    # ✅ Launch Streamlit
    start_streamlit_dashboard()
