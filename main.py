import threading
import time
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from telegram_bot import start_telegram_bot
from pocket_bot import start_pocket_bot

# Dummy HTTP server to prevent Render from sleeping
def keep_alive():
    port = 8080
    handler = SimpleHTTPRequestHandler
    with TCPServer(("0.0.0.0", port), handler) as httpd:
        print(f"🟢 Dummy server running at http://0.0.0.0:{port}")
        httpd.serve_forever()

# Telegram bot thread
def run_telegram():
    start_telegram_bot()

# Pocket Option bot (main loop)
def run_pocket():
    start_pocket_bot()

# Run everything
if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()
    threading.Thread(target=run_telegram).start()
    run_pocket()

