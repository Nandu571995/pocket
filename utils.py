from pocket_option_scraper import fetch_candles_for_all_assets

def get_latest_candle(pair, time_str):
    """
    Find the 1-minute candle for a given pair and HH:MM time.
    """
    # Fetch data for just this asset and 1m timeframe
    candles_data = fetch_candles_for_all_assets([1])  # 1 = 1m
    candles = candles_data.get(pair, {}).get(1, [])  # 1 = 1m

    for candle in candles:
        candle_time = candle["time"][-5:]  # Extract HH:MM from timestamp
        if candle_time == time_str:
            return candle
    return None
