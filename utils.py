import json
from datetime import datetime
from pocket_option_scraper import fetch_candles_for_all_assets

def get_latest_candle(pair, time_str):
    """
    Find the 1-minute candle for a given pair and HH:MM time.
    """
    candles_data = fetch_candles_for_all_assets([1])  # 1m timeframe
    candles = candles_data.get(pair, {}).get(1, [])

    for candle in candles:
        candle_time = candle["time"][-5:]  # Get HH:MM
        if candle_time == time_str:
            return candle
    return None

def save_signal(signal_data, filename="signals.json"):
    """
    Save a signal to signals.json
    """
    try:
        with open(filename, "r") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    tf = signal_data["timeframe"]
    if tf not in existing_data:
        existing_data[tf] = []

    existing_data[tf].append(signal_data)

    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=2)

def validate_signals(filename="signals.json"):
    """
    Validate past signals by checking if their prediction was correct.
    """
    try:
        with open(filename, "r") as file:
            signals = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No signals to validate.")
        return

    updated = False
    for tf, tf_signals in signals.items():
        for signal in tf_signals:
            if "validated" in signal:
                continue  # Already validated

            now = datetime.utcnow()
            signal_time = datetime.strptime(signal["timestamp"], "%Y-%m-%d %H:%M:%S")
            wait_minutes = int(tf.replace("m", ""))
            if (now - signal_time).total_seconds() < wait_minutes * 60 + 60:
                continue  # Skip if timeframe not yet complete

            # Fetch latest candle
            target_time = (signal_time + timedelta(minutes=wait_minutes)).strftime("%H:%M")
            latest_candle = get_latest_candle(signal["pair"], target_time)

            if latest_candle:
                open_price = latest_candle["open"]
                close_price = latest_candle["close"]
                if signal["direction"].upper() == "GREEN":
                    signal["validated"] = close_price > open_price
                else:
                    signal["validated"] = close_price < open_price
                updated = True

    if updated:
        with open(filename, "w") as file:
            json.dump(signals, file, indent=2)
