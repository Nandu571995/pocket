import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from telegram_bot import start_telegram_bot
from pocket_bot import start_pocket_bot
from dashboard import run_dashboard

def keep_alive():
    port = 8080
    handler = SimpleHTTPRequestHandler
    with TCPServer(("0.0.0.0", port), handler) as httpd:
        print(f"🟢 Dummy server running at http://0.0.0.0:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()
    threading.Thread(target=start_telegram_bot, daemon=True).start()
    threading.Thread(target=start_pocket_bot, daemon=True).start()
    run_dashboard()  # runs Streamlit in the main thread
