# pocket_bot.py
import time
import json
import random
import threading
from datetime import datetime, timedelta
from strategy import generate_signal
from telegram_bot import send_telegram_signal

SIGNALS_FILE = "signals.json"
TIMEFRAMES = ["1m", "3m", "5m", "10m"]

# Simulated list of OTC and FX assets for Pocket Option
ASSETS = [
    "EUR/USD", "GBP/USD", "AUD/USD", "USD/JPY", "USD/CHF", "USD/CAD",
    "EUR/GBP", "EUR/JPY", "BTC/USD", "ETH/USD",
    "OTC EUR/USD", "OTC GBP/JPY", "OTC AUD/CAD", "OTC USD/CHF", "OTC NZD/JPY"
]

def load_existing_signals():
    try:
        with open(SIGNALS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_signal(signal):
    signals = load_existing_signals()
    signals.append(signal)
    with open(SIGNALS_FILE, "w") as f:
        json.dump(signals, f, indent=2)

def signal_loop(asset, tf):
    while True:
        now = datetime.utcnow()
        current_minute = now.minute
        current_second = now.second

        # Calculate when to send the signal (30–60 seconds before next candle)
        delay = 60 - current_second - 30
        if delay > 0:
            time.sleep(delay)

        signal_data = generate_signal(asset, tf)

        if signal_data and signal_data["confidence"] >= 60:
            signal = {
                "timestamp": int(time.time()),
                "pair": asset,
                "timeframe": tf,
                "signal": signal_data["direction"],
                "confidence": signal_data["confidence"],
                "result": "pending"
            }
            save_signal(signal)

            formatted_time = (datetime.utcnow() + timedelta(minutes=1)).strftime("%H:%M")
            message = (
                f"📡 *Next Candle {tf.upper()}*\n"
                f"*{signal['signal'].upper()}* | `{asset}` | ⏰ {formatted_time}\n"
                f"🎯 Confidence: *{signal['confidence']}%*"
            )
            send_telegram_signal(message)

        time.sleep(30)

def start_pocket_bot():
    for asset in ASSETS:
        for tf in TIMEFRAMES:
            threading.Thread(target=signal_loop, args=(asset, tf), daemon=True).start()
