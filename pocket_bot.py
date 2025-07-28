# pocket_bot.py

import requests
import pandas as pd
import time
import json
from datetime import datetime, timedelta
from strategy import evaluate_signal

# Assets to scan (OTC + Forex Pairs)
ASSETS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF", "NZDUSD",
    "EURJPY", "GBPJPY", "EURGBP", "USDCAD",
    "OTC_EURUSD", "OTC_GBPUSD", "OTC_USDJPY", "OTC_AUDUSD"
]

TIMEFRAMES = {
    "1m": 1,
    "3m": 3,
    "5m": 5,
    "10m": 10
}

SIGNAL_FILE = "signals.json"

# Pocket Option candle data URL (replace this with actual URL or scraping logic)
def get_candle_data(symbol, minutes=50, timeframe="1m"):
    url = f"https://pocketapi.in/get_candles?pair={symbol}&interval={timeframe}&limit={minutes}"
    try:
        res = requests.get(url)
        data = res.json()
        candles = pd.DataFrame(data)
        candles.columns = ['timestamp', 'open', 'high', 'low', 'close']
        candles['timestamp'] = pd.to_datetime(candles['timestamp'], unit='s')
        return candles
    except Exception as e:
        print(f"Error fetching data for {symbol} - {e}")
        return None

def generate_and_save_signal(symbol, tf_name):
    df = get_candle_data(symbol, minutes=50, timeframe=tf_name)
    if df is None or len(df) < 30:
        return None

    signal, confidence = evaluate_signal(df)
    if signal:
        now = datetime.utcnow() + timedelta(minutes=5.5*60)  # convert to IST
        start_time = (now + timedelta(minutes=1)).strftime("%H:%M")
        end_time = (now + timedelta(minutes=1+TIMEFRAMES[tf_name])).strftime("%H:%M")
        msg = f"""
📡 Signal #{tf_name}
Asset: {symbol}
🕒 Time: {start_time}–{end_time}
📊 Action: {signal}
✅ Confidence: {confidence}%
        """.strip()

        log = {
            "symbol": symbol,
            "timeframe": tf_name,
            "start": start_time,
            "end": end_time,
            "signal": signal,
            "confidence": confidence,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            with open(SIGNAL_FILE, 'r') as f:
                old_data = json.load(f)
        except:
            old_data = []

        old_data.append(log)
        with open(SIGNAL_FILE, 'w') as f:
            json.dump(old_data, f, indent=2)

        print(msg)
        return msg
    return None

def start_pocket_bot():
    print("🔁 Pocket Option bot started...")
    while True:
        for tf_name in TIMEFRAMES:
            for symbol in ASSETS:
                signal = generate_and_save_signal(symbol, tf_name)
                time.sleep(1)  # avoid rate limits
        time.sleep(30)
