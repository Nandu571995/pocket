# pocket_bot.py

import time
import json
import threading
from datetime import datetime, timedelta
from pocket_option_scraper import get_all_assets, get_candles
from strategy import analyze_signal
from telegram_bot import send_signal_alert

SIGNALS_FILE = "signals.json"
TIMEFRAMES = {
    '1m': 60,
    '3m': 180,
    '5m': 300,
    '10m': 600
}

def load_existing_signals():
    try:
        with open(SIGNALS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_signal(signal):
    all_signals = load_existing_signals()
    all_signals.append(signal)
    with open(SIGNALS_FILE, "w") as f:
        json.dump(all_signals[-500:], f, indent=2, default=str)  # keep last 500 only

def process_asset(symbol, timeframe, interval):
    candles = get_candles(symbol, str(interval), limit=100)
    if candles.empty or len(candles) < 50:
        return

    signal_data = analyze_signal(candles)
    if signal_data["signal"] == "NO_SIGNAL":
        return

    # Set signal timing
    now = datetime.utcnow()
    next_candle_time = (now + timedelta(seconds=interval)).replace(second=0, microsecond=0)
    alert_time = next_candle_time - timedelta(seconds=60)

    # Prepare signal
    signal = {
        "pair": symbol,
        "timeframe": timeframe,
        "signal": signal_data["signal"],
        "reason": signal_data["reason"],
        "confidence": signal_data["confidence"],
        "timestamp": datetime.utcnow().isoformat(),
        "for_candle": f"{next_candle_time.strftime('%H:%M')}–{(next_candle_time + timedelta(seconds=interval)).strftime('%H:%M')}"
    }

    print(f"[{timeframe}] Signal for {symbol}: {signal['signal']} @ {signal['for_candle']} | {signal['confidence']}%")

    # Save and send signal
    save_signal(signal)
    send_signal_alert(signal)

def scan_market():
    assets = get_all_assets()
    for symbol in assets:
        for tf, interval in TIMEFRAMES.items():
            try:
                process_asset(symbol, tf, interval)
            except Exception as e:
                print(f"Error on {symbol}-{tf}: {e}")

def start_pocket_bot():
    print("✅ Pocket Option Bot Started.")
    while True:
        now = datetime.utcnow()
        if now.second == 0:
            threading.Thread(target=scan_market).start()
            time.sleep(55)
        time.sleep(1)
