# telegram_bot.py

import requests

TELEGRAM_BOT_TOKEN = "8062898551:AAFp6Mzz3TU2Ngeqf4gL4KL55S1guuRwcnA"
TELEGRAM_CHAT_ID = "1014815784"

def send_signal_message(message: str):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("❌ Telegram send error:", response.text)
        else:
            print("✅ Signal sent to Telegram.")
    except Exception as e:
        print("⚠️ Telegram send exception:", e)
