# pocket_bot.py

import threading
import time
from datetime import datetime, timedelta
from pocket_option_scraper import get_all_assets, get_candles
from strategy import analyze_signal
from telegram_bot import send_signal_telegram
import json
import os

SIGNALS_FILE = "signals.json"
TIMEFRAMES = [1, 3, 5, 10]

# Ensure signals.json exists
if not os.path.exists(SIGNALS_FILE):
    with open(SIGNALS_FILE, "w") as f:
        json.dump([], f)

def log_signal(signal):
    with open(SIGNALS_FILE, "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
        data.append(signal)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

def process_asset(asset):
    for tf in TIMEFRAMES:
        candles = get_candles(asset, interval=tf, limit=30)
        if len(candles) < 20:
            return
        signal_info = analyze_signal(candles)
        if signal_info:
            now = datetime.utcnow()
            signal_time = now + timedelta(minutes=1)
            signal = {
                "id": f"{asset}_{tf}_{signal_time.strftime('%Y%m%d%H%M')}",
                "asset": asset,
                "timeframe": tf,
                "signal_time": f"{(signal_time).strftime('%H:%M')}–{(signal_time + timedelta(minutes=tf)).strftime('%H:%M')}",
                "direction": signal_info["direction"],
                "confidence": signal_info["confidence"],
                "reason": signal_info["reason"],
                "generated_at": now.strftime('%Y-%m-%d %H:%M:%S'),
                "status": "pending"
            }
            log_signal(signal)
            send_signal_telegram(signal)

def start_pocket_bot():
    print("✅ Pocket bot started.")
    def run_loop():
        while True:
            try:
                all_assets = get_all_assets()
                for asset in all_assets:
                    process_asset(asset)
                time.sleep(60)
            except Exception as e:
                print(f"Error in bot loop: {e}")
                time.sleep(10)

    threading.Thread(target=run_loop).start()
