import time
import json
from datetime import datetime, timedelta
from pocket_option_scraper import fetch_candles_for_all_assets
from strategy import analyze_signal
from telegram_bot import send_signal_telegram
from utils import save_signal, validate_signals

TIMEFRAMES = ["1m", "3m", "5m", "10m"]

def start_pocket_bot():
    print("✅ Pocket bot started.")
    while True:
        try:
            now = datetime.utcnow()
            if now.second in range(0, 2):  # Run at start of minute
                all_candle_data = fetch_candles_for_all_assets(TIMEFRAMES)

                for asset, tf_data in all_candle_data.items():
                    for tf, candles in tf_data.items():
                        if len(candles) < 2:
                            continue

                        signal = analyze_signal(candles)
                        if signal:
                            direction = signal["direction"]
                            confidence = signal["confidence"]
                            reason = signal["reason"]

                            next_start = now + timedelta(minutes=1)
                            start_str = next_start.strftime("%H:%M")
                            end_str = (next_start + timedelta(minutes=1)).strftime("%H:%M")

                            signal_data = {
                                "asset": asset,
                                "timeframe": tf,
                                "start": start_str,
                                "end": end_str,
                                "direction": direction,
                                "confidence": confidence,
                                "reason": reason,
                                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                                "validated": False,
                                "result": None
                            }

                            save_signal(signal_data)
                            send_signal_telegram(signal_data)

                validate_signals()  # Auto validation after timeframe ends
                time.sleep(60)
            else:
                time.sleep(1)
        except Exception as e:
            print("Error in bot loop:", e)
            time.sleep(5)
