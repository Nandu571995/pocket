# pocket_option_scraper.py

import requests
import random
import time
import json
from datetime import datetime, timedelta

BASE_URL = "https://api.pocketoption.com"

# Static fallback list of OTC and currency pairs
FALLBACK_ASSETS = [
    "EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "AUDUSD_otc", "NZDUSD_otc",
    "EURJPY_otc", "GBPJPY_otc", "EURGBP_otc", "USDCHF_otc", "EURUSD",
    "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD", "EURJPY", "GBPJPY", "EURGBP", "USDCHF"
]

def get_all_assets():
    """Return a static or scraped list of all tradable assets."""
    # In production, this should scrape from real-time Pocket Option data.
    # For now, we use a static list of OTC + Currency pairs
    return FALLBACK_ASSETS

def get_candles(asset, interval, limit=5):
    """
    Mock candle data generator for demo/testing.

    Replace with real-time candle scraping from Pocket Option WebSocket or API.
    """
    now = datetime.utcnow()
    candles = []

    for i in range(limit):
        open_price = round(random.uniform(1.0, 1.2), 5)
        close_price = open_price + round(random.uniform(-0.001, 0.001), 5)
        high_price = max(open_price, close_price) + 0.0005
        low_price = min(open_price, close_price) - 0.0005
        candle_time = now - timedelta(minutes=i * interval)

        candles.append({
            "time": candle_time.strftime('%Y-%m-%d %H:%M:%S'),
            "open": open_price,
            "close": close_price,
            "high": high_price,
            "low": low_price,
        })

    return list(reversed(candles))
