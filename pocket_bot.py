# File: pocket_bot.py
import time
import json
from datetime import datetime, timedelta
from strategy import check_trade_signal
from telegram_bot import send_signal
from pocket_option_scraper import get_active_assets, get_candles

TIMEFRAMES = ['1m', '3m', '5m', '10m']

def start_pocket_bot():
    print("📊 Starting real-time Pocket Option bot...")
    while True:
        try:
            assets = get_active_assets()
            print(f"🔍 Scanning {len(assets)} assets...")

            for asset in assets:
                for tf in TIMEFRAMES:
                    candles = get_candles(asset, tf)
                    if not candles or len(candles) < 5:
                        continue

                    signal_data = check_trade_signal(candles)
                    if signal_data:
                        direction, confidence, reason = signal_data["signal"], signal_data["confidence"], signal_data["reason"]

                        next_start = (datetime.utcnow() + timedelta(seconds=30)).strftime('%H:%M')
                        next_end = (datetime.utcnow() + timedelta(minutes=int(tf.replace('m', '')))).strftime('%H:%M')

                        send_signal(asset, tf, direction, confidence, reason, next_start, next_end)
                        log_signal(asset, tf, direction, confidence, reason, next_start, next_end)

            time.sleep(30)
        except Exception as e:
            print(f"[ERROR] Bot loop: {e}")
            time.sleep(10)

def log_signal(asset, tf, direction, confidence, reason, start, end):
    try:
        with open("signals.json", "r") as f:
            data = json.load(f)
    except:
        data = {}

    if tf not in data:
        data[tf] = []

    signal_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "asset": asset,
        "direction": direction,
        "confidence": confidence,
        "reason": reason,
        "range": f"{start}-{end}",
        "result": "PENDING"
    }

    data[tf].append(signal_entry)

    with open("signals.json", "w") as f:
        json.dump(data, f, indent=4)
