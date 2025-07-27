import threading
from telegram_bot import start_telegram_bot
from pocket_bot import start_pocket_bot

def run_telegram():
    start_telegram_bot()

def run_pocket():
    start_pocket_bot()

if __name__ == "__main__":
    threading.Thread(target=run_telegram).start()
    run_pocket()
