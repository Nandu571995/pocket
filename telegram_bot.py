# telegram_bot.py

import os
import logging
from telegram import Bot

# Telegram bot credentials
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8062898551:AAFp6Mzz3TU2Ngeqf4gL4KL55S1guuRwcnA")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1014815784")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN)

def send_signal_telegram(signal):
    try:
        message = (
            f"📡 *Signal {signal['timeframe']}m | {signal['asset']}*\n"
            f"🕒 *Time:* {signal['signal_time']}\n"
            f"🎯 *Direction:* `{signal['direction'].upper()}`\n"
            f"📊 *Confidence:* {signal['confidence']}%\n"
            f"📌 *Reason:* {signal['reason']}\n"
            f"📅 *Generated at:* {signal['generated_at']}\n"
            f"#PocketOption #SignalBot"
        )
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
        logger.info(f"Sent signal to Telegram: {message}")
    except Exception as e:
        logger.error(f"Error sending Telegram message: {e}")
