# File: pocket_option_scraper.py
import requests
from datetime import datetime, timedelta

def get_active_assets():
    try:
        url = "https://pocketoption.com/en/api/v1/assets/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        active_assets = []
        for asset in data.get("assets", []):
            if asset.get("asset_type") == "currency" or asset.get("asset_type") == "otc":
                if asset.get("is_trading_enabled", False):
                    active_assets.append(asset["name"])
        return list(set(active_assets))
    except Exception as e:
        print(f"[ERROR] Failed to fetch assets: {e}")
        return []

def get_candles(asset, tf='1m', count=10):
    try:
        end = int(datetime.utcnow().timestamp())
        start = end - count * int(tf.replace('m', '')) * 60

        url = f"https://pocketoption.com/en/api/v1/candles/{asset}?from={start}&to={end}&interval={tf}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        candles = [{
            "timestamp": c["timestamp"],
            "open": c["open"],
            "high": c["high"],
            "low": c["low"],
            "close": c["close"],
            "volume": c.get("volume", 0)
        } for c in data.get("candles", [])]
        return candles
    except Exception as e:
        print(f"[ERROR] Candle fetch failed for {asset}: {e}")
        return []
