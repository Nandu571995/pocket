from pocket_option_scraper import get_candle_data  # Or your custom scraper function

def get_latest_candle(pair, time_str):
    """
    Find the 1-minute candle for a given pair and HH:MM time.
    """
    candles = get_candle_data(pair, interval="1m", limit=10)

    for candle in candles:
        candle_time = candle["time"][-5:]  # Extract HH:MM from timestamp
        if candle_time == time_str:
            return candle
    return None
