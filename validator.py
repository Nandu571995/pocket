import json
from datetime import datetime, timedelta
from utils import get_latest_candle  # You'll create this function if not present

def validate_signals():
    with open("signals.json", "r+") as file:
        data = json.load(file)

        for tf in ["1m", "3m", "5m", "10m"]:
            for signal in data[tf]:
                if signal["result"] != "pending":
                    continue  # Already validated

                # Check if candle has closed
                current_time = datetime.utcnow()
                end_time = datetime.strptime(signal["end"], "%H:%M")
                now = current_time.replace(second=0, microsecond=0)

                if now >= end_time:
                    # Get actual candle close price
                    pair = signal["pair"]
                    direction = signal["direction"]
                    start_time = signal["start"]

                    # 🕯️ Fetch that specific candle using your data source
                    candle = get_latest_candle(pair, start_time)

                    if not candle:
                        continue  # Wait for correct candle

                    result = "win" if (
                        (direction == "BUY" and candle["close"] > candle["open"]) or
                        (direction == "SELL" and candle["close"] < candle["open"])
                    ) else "lose"

                    signal["result"] = result

        # Save updated JSON
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
