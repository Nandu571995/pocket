import threading
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram_bot import start_telegram_bot
from pocket_bot import start_pocket_bot
from dashboard import run_dashboard

# Dummy keep-alive server for Render
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is running.")

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), KeepAliveHandler)
    print(f"🟢 Keep-alive server running on port {port}")
    server.serve_forever()

def run_all():
    threading.Thread(target=start_telegram_bot, name="TelegramBot").start()
    threading.Thread(target=start_pocket_bot, name="PocketBot").start()
    threading.Thread(target=run_dashboard, name="Dashboard").start()

if __name__ == "__main__":
    print("🚀 Starting Pocket Option Trading Bot System...")
    threading.Thread(target=keep_alive, name="KeepAlive").start()
    run_all()
