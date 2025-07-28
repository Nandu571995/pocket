# pocket_option_scraper.py

import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz

def get_all_assets():
    url = "https://api.pocketoption.com/en/api/v1/assets/all"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [a['symbol'] for a in data if a['is_otc'] or a['type'] == 'forex']
    except Exception as e:
        print(f"Error fetching assets: {e}")
        return []

def get_candles(symbol, interval='60', limit=100):
    end = int(datetime.utcnow().timestamp())
    url = f"https://api.pocketoption.com/en/api/v1/candles/{symbol}?interval={interval}&limit={limit}&end_time={end}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        candles = [
            {
                'time': datetime.utcfromtimestamp(c['timestamp']).replace(tzinfo=pytz.utc),
                'open': c['open'],
                'high': c['high'],
                'low': c['low'],
                'close': c['close'],
                'volume': c['volume']
            }
            for c in data
        ]
        return pd.DataFrame(candles)
    except Exception as e:
        print(f"Error fetching candles for {symbol}: {e}")
        return pd.DataFrame()
