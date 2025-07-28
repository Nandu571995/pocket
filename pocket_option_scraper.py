# pocket_option_scraper.py

import random
import datetime
import pandas as pd

def fetch_candles_for_all_assets(timeframes):
    # Simulated candle data generation for all assets and timeframes
    assets = [
        "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF",
        "BTC/USD", "ETH/USD", "GOLD", "CRUDE", "OTC_EURUSD",
        "OTC_GBPUSD", "OTC_USDJPY", "OTC_AUDCAD"
    ]
    
    all_data = {}
    now = datetime.datetime.utcnow().replace(second=0, microsecond=0)
    
    for asset in assets:
        all_data[asset] = {}
        for tf in timeframes:
            candles = []
            for i in range(50):  # last 50 candles
                base_time = now - datetime.timedelta(minutes=tf * i)
                open_price = round(random.uniform(1.1000, 1.3000), 5)
                close_price = open_price + round(random.uniform(-0.0010, 0.0010), 5)
                high_price = max(open_price, close_price) + round(random.uniform(0, 0.0005), 5)
                low_price = min(open_price, close_price) - round(random.uniform(0, 0.0005), 5)
                candles.append({
                    "timestamp": base_time.isoformat(),
                    "open": open_price,
                    "close": close_price,
                    "high": high_price,
                    "low": low_price,
                    "volume": random.randint(100, 1000)
                })
            df = pd.DataFrame(candles).sort_values("timestamp")
            df.reset_index(drop=True, inplace=True)
            all_data[asset][tf] = df
    
    return all_data
