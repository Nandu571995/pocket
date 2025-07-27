import time
import json
import logging
import os
import random
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from strategy import check_trade_signal
from telegram_bot import send_signal

# Assets
OTC_ASSETS = ["EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "AUDCAD_otc"]
FX_ASSETS = ["EURUSD", "GBPUSD", "USDJPY", "AUDCAD"]
ASSETS = OTC_ASSETS + FX_ASSETS

# Timeframes
TIMEFRAMES = ["1m", "3m", "5m", "10m"]

# Signal log file
SIGNAL_LOG = "signals.json"

def start_pocket_bot():
    logging.basicConfig(level=logging.INFO)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    logging.info("🟢 Browser initialized")

    while True:
        for asset in ASSETS:
            for tf in TIMEFRAMES:
                try:
                    candles = get_candle_data(driver, asset, tf)
                    df = pd.DataFrame(candles)
                    signal = check_trade_signal(df)

                    if signal:
                        send_signal(asset, tf, signal)
                        save_signal_result(asset, tf, signal, df)

                except Exception as e:
                    logging.error(f"❌ Error for {asset} {tf}: {e}")
        time.sleep(60)

# Simulated candle data (replace with real scraping logic)
def get_candle_data(driver, asset, timeframe):
    candles = []
    for _ in range(100):
        open_price = random.uniform(1.0, 1.1)
        close_price = open_price + random.uniform(-0.005, 0.005)
        high = max(open_price, close_price) + random.uniform(0.001, 0.003)
        low = min(open_price, close_price) - random.uniform(0.001, 0.003)
        candles.append({
            'timestamp': datetime.now().timestamp(),
            'open': round(open_price, 5),
            'high': round(high, 5),
            'low': round(low, 5),
            'close': round(close_price, 5)
        })
    return candles

# Store signal and later track accuracy
def save_signal_result(asset, tf, signal, df):
    now = datetime.now()
    next_open = df.iloc[-1]['close']
    entry = {
        "asset": asset,
        "timeframe": tf,
        "signal": signal,
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "open": round(next_open, 5),
        "checked": False,
        "result": None  # To be validated after candle closes
    }

    if os.path.exists(SIGNAL_LOG):
        with open(SIGNAL_LOG, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(SIGNAL_LOG, "w") as f:
        json.dump(data, f, indent=2)
