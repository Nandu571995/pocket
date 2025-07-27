import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from strategy import check_trade_signal
from telegram_bot import send_signal
import logging

OTC_ASSETS = ["EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "AUDCAD_otc"]
TIMEFRAMES = ["1m", "5m"]

def start_pocket_bot():
    logging.basicConfig(level=logging.INFO)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    logging.info("🟢 Browser initialized")

    while True:
        for asset in OTC_ASSETS:
            for tf in TIMEFRAMES:
                try:
                    candles = get_candle_data(driver, asset, tf)
                    signal = check_trade_signal(candles)
                    if signal:
                        send_signal(asset, tf, signal)
                except Exception as e:
                    logging.error(f"❌ Error for {asset} {tf}: {e}")
        time.sleep(60)

def get_candle_data(driver, asset, timeframe):
    # Simulate candle scraping from Pocket Option chart or use dummy test
    # Replace below mock with real scraping if needed
    import random
    from datetime import datetime
    candles = []
    for _ in range(100):
        candles.append({
            'timestamp': datetime.now().timestamp(),
            'open': random.uniform(1.0, 1.1),
            'high': random.uniform(1.1, 1.2),
            'low': random.uniform(0.9, 1.0),
            'close': random.uniform(1.0, 1.1)
        })
    return candles
