# pocket_option_scraper.py

import requests
import datetime
import time

# Sample asset list (can be dynamically fetched too)
ASSETS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD",
    "USDCHF", "USDCAD", "BTCUSD", "ETHUSD", "XAUUSD",
    "XAGUSD", "LTCUSD", "OTC_EURUSD", "OTC_GBPUSD", "OTC_USDJPY"
]

BASE_URL = "https://api-pocketoption.com/indicators/candles"

def get_candle_data(asset: str, timeframe: int = 60, count: int = 10):
    """
    Fetch recent candle data for a given asset and timeframe.
    :param asset: str (e.g., "EURUSD", "BTCUSD", etc.)
    :param timeframe: int (candle duration in seconds, e.g., 60 for 1 min)
    :param count: int (number of candles to fetch)
    :return: List of candle dicts
    """
    now = int(time.time())
    end_time = now
    start_time = end_time - timeframe * count

    params = {
        "asset": asset,
        "from": start_time,
        "to": end_time,
        "interval": timeframe
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            candles = data.get("data", [])
            return candles
        else:
            print(f"Failed to fetch candle data for {asset}. Status: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching candle data for {asset}: {e}")
        return []
