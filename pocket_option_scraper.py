# pocket_option_scraper.py

import requests
import datetime

BASE_URL = "https://api-pocketoption.live/api/v1"

def get_assets():
    """Fetch list of available assets (OTC + currency)."""
    try:
        response = requests.get(f"{BASE_URL}/assets")
        response.raise_for_status()
        assets = response.json()
        return [a['symbol'] for a in assets if a['type'] in ['otc', 'forex']]
    except Exception as e:
        print(f"Asset fetch error: {e}")
        return []

def get_candles(symbol, timeframe, limit=10):
    """Fetch recent candles for an asset at given timeframe."""
    try:
        url = f"{BASE_URL}/candles?symbol={symbol}&interval={timeframe}&limit={limit}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        candles = []
        for c in data:
            candles.append({
                "time": datetime.datetime.utcfromtimestamp(c["timestamp"]),
                "open": c["open"],
                "close": c["close"],
                "high": c["high"],
                "low": c["low"],
                "volume": c.get("volume", 0)
            })
        return candles
    except Exception as e:
        print(f"[{symbol} {timeframe}] Candle fetch error: {e}")
        return []
