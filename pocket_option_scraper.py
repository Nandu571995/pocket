import requests
import time

BASE_URL = "https://api.pocketoption.com/chart/history/candles"

ASSETS = [
    "EURUSD_OTC", "GBPUSD_OTC", "USDJPY_OTC", "AUDUSD_OTC", "USDCHF_OTC", "NZDUSD_OTC",
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF", "NZDUSD"
]

def fetch_candles(asset, tf, limit=20):
    tf_map = {"1m": "60", "3m": "180", "5m": "300", "10m": "600"}
    resolution = tf_map[tf]
    url = f"{BASE_URL}?asset={asset}&resolution={resolution}&limit={limit}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [
                {
                    "timestamp": item[0],
                    "open": item[1],
                    "high": item[2],
                    "low": item[3],
                    "close": item[4]
                }
                for item in data["candles"]
            ]
    except Exception as e:
        print(f"Error fetching {asset} {tf} data: {e}")
    return []

def fetch_candles_for_all_assets(timeframes):
    result = {}
    for asset in ASSETS:
        result[asset] = {}
        for tf in timeframes:
            candles = fetch_candles(asset, tf)
            if candles:
                result[asset][tf] = candles
            time.sleep(0.3)  # To avoid hitting rate limits
    return result
