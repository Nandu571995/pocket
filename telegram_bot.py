from telegram import Bot
import os

# Load from environment variables or directly assign
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "8062898551:AAFp6Mzz3TU2Ngeqf4gL4KL55S1guuRwcnA"
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "1014815784"

bot = Bot(token=TELEGRAM_TOKEN)

def send_signal_telegram(signal):
    """
    Send a trading signal to Telegram in formatted style.
    """
    message = (
        f"📢 *{signal['timeframe']} Signal Alert!*\n"
        f"🪙 *Asset:* `{signal['asset']}`\n"
        f"🎯 *Direction:* {signal['direction']}\n"
        f"🧠 *Confidence:* {signal['confidence']}%\n"
        f"📊 *Reason:* {signal['reason']}\n"
        f"🕒 *Time:* {signal['timestamp']}"
    )
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

# Optional: Telegram test
if __name__ == "__main__":
    send_signal_telegram({
        "asset": "BTC/USD",
        "direction": "BUY",
        "confidence": 87,
        "reason": "MACD + EMA",
        "timestamp": "2025-07-28 21:18",
        "timeframe": "1m"
    })
