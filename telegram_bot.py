# telegram_bot.py

import os
import logging
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

def send_signal_to_telegram(signal):
    try:
        timeframe = signal['timeframe']
        symbol = signal['symbol']
        direction = signal['direction']
        confidence = signal['confidence']
        reason = signal['reason']
        signal_time = signal['signal_time']
        expiry = signal['expiry_time']

        message = f"""
📡 *New Trading Signal*
───────────────
📍 *Asset:* `{symbol}`
🕒 *Timeframe:* `{timeframe}`
🟢 *Direction:* `{direction.upper()}`
📈 *Confidence:* `{confidence}%`
📚 *Reason:* {reason}
⏱ *Trade Window:* `{signal_time} – {expiry}`
───────────────
🔥 *Execute before candle starts!*
        """
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
        logging.info(f"Signal sent: {symbol} | {timeframe} | {direction}")
    except Exception as e:
        logging.error(f"Telegram send error: {e}")
