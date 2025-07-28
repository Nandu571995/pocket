import requests
from datetime import datetime, timedelta
import pytz
import time

# Timezone for Pocket Option UTC server
tz = pytz.UTC

def get_all_assets():
    try:
        response = requests.get("https://pocketoption.com/api/v1/assets/all")
        assets = response.json().get("data", [])
        filtered = []
        for asset in assets:
            if asset.get("isOTC") or asset.get("category") == "currency":
                filtered.append(asset["symbol"])
        return list(set(filtered))
    except Exception as e:
        print("Error fetching asset list:", e)
        return []

def fetch_candles(asset, timeframe):
    try:
        now = datetime.utcnow().replace(second=0, microsecond=0)
        if timeframe == "1m":
            delta = timedelta(minutes=2)
            interval = 60
        elif timeframe == "3m":
            delta = timedelta(minutes=6)
            interval = 180
        elif timeframe == "5m":
            delta = timedelta(minutes=10)
            interval = 300
        elif timeframe == "10m":
            delta = timedelta(minutes=20)
            interval = 600
        else:
            return []

        end_time = int(now.timestamp())
        start_time = int((now - delta).timestamp())

        url = f"https://pocketoption.com/chart/history/candles/{asset}?from={start_time}&to={end_time}&interval={interval}"
        res = requests.get(url)
        candles = res.json().get("data", [])
        return candles[-2:] if len(candles) >= 2 else []
    except Exception as e:
        print(f"Error fetching candles for {asset} ({timeframe}):", e)
        return []

def fetch_candles_for_all_assets(timeframes):
    all_data = {}
    assets = get_all_assets()
    for asset in assets:
        all_data[asset] = {}
        for tf in timeframes:
            candles = fetch_candles(asset, tf)
            all_data[asset][tf] = candles
            time.sleep(0.1)  # Avoid hammering server
    return all_data
