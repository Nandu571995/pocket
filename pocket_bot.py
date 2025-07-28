# pocket_bot.py

import json
import time
import pytz
import threading
import datetime
import requests
from strategy import check_trade_signal
from telegram_bot import send_signal_message

TIMEFRAMES = {
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "10m": 600
}

PAIRS = [
    "EURUSD-OTC", "GBPUSD-OTC", "USDJPY-OTC", "AUDUSD-OTC", "EURJPY-OTC",
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "EURJPY"
]

def fetch_candles(pair, interval, limit=100):
    try:
        url = f"https://api.pocketoption.com/api/v1/candles/{pair}?interval={interval}&limit={limit}"
        response = requests.get(url)
        data = response.json()
        candles = [{"time": c["timestamp"], "open": c["open"], "high": c["high"],
                    "low": c["low"], "close": c["close"], "volume": c["volume"]}
                   for c in data["data"]]
        return candles
    except Exception as e:
        print(f"Error fetching candles for {pair} [{interval}]:", e)
        return []

def load_signal_log():
    try:
        with open("signals.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_signal_log(signals):
    with open("signals.json", "w") as f:
        json.dump(signals, f, indent=2)

def should_generate(pair, tf, log):
    now = datetime.datetime.utcnow().replace(second=0, microsecond=0)
    next_candle = now + datetime.timedelta(seconds=TIMEFRAMES[tf])
    timestamp = next_candle.strftime("%Y-%m-%d %H:%M:%S")
    for s in log:
        if s["pair"] == pair and s["timeframe"] == tf and s["next_candle"] == timestamp:
            return False
    return True

def analyze_and_signal(pair, tf):
    interval = tf.replace("m", "")
    candles = fetch_candles(pair, interval)
    if len(candles) < 30:
        return

    signal = check_trade_signal(candles)
    if signal["direction"] is None or signal["confidence"] < 60:
        return

    log = load_signal_log()
    if not should_generate(pair, tf, log):
        return

    next_candle_time = datetime.datetime.utcnow().replace(second=0, microsecond=0) + datetime.timedelta(seconds=TIMEFRAMES[tf])
    next_str = next_candle_time.strftime("%H:%M") + "–" + (next_candle_time + datetime.timedelta(minutes=1)).strftime("%H:%M")

    signal_data = {
        "pair": pair,
        "timeframe": tf,
        "direction": signal["direction"],
        "confidence": signal["confidence"],
        "reasons": signal["reasons"],
        "next_candle": next_candle_time.strftime("%Y-%m-%d %H:%M:%S"),
        "time_generated": datetime.datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")
    }

    log.append(signal_data)
    save_signal_log(log)

    msg = f"""📊 *Signal Alert*
Asset: `{pair}`
Timeframe: `{tf}`
🕰 Time: `{next_str}`
📈 Direction: *{signal['direction']}*
✅ Confidence: *{signal['confidence']}%*
📚 Reason: `{', '.join(signal['reasons'])}`"""
    send_signal_message(msg)

def scan_all():
    while True:
        print("⏳ Scanning...")
        for tf in TIMEFRAMES:
            for pair in PAIRS:
                threading.Thread(target=analyze_and_signal, args=(pair, tf)).start()
        time.sleep(30)

def start_pocket_bot():
    t = threading.Thread(target=scan_all)
    t.start()
