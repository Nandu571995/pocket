import time
import json
from datetime import datetime, timedelta
from pocket_option_scraper import fetch_candles_for_all_assets
from strategy import check_trade_signal
from telegram_bot import send_signal_telegram
from utils import log_signal, validate_previous_signals

TIMEFRAMES = {
    '1m': 1,
    '3m': 3,
    '5m': 5,
    '10m': 10,
}

DELAY_BEFORE_CANDLE = 60  # seconds before next candle

def get_current_utc_time():
    return datetime.utcnow()

def should_send_signal(current_time, interval_minutes):
    """Check if it's time to send signal ~1 minute before next candle."""
    return current_time.second == (60 - DELAY_BEFORE_CANDLE) % 60 and current_time.minute % interval_minutes == (interval_minutes - 1) % interval_minutes

def start_pocket_bot():
    print("✅ Pocket bot started.")
    while True:
        try:
            current_time = get_current_utc_time()
            for tf_name, tf_minutes in TIMEFRAMES.items():
                if should_send_signal(current_time, tf_minutes):
                    print(f"📊 Scanning {tf_name} signals at {current_time}")
                    asset_candle_data = fetch_candles_for_all_assets(tf_minutes)

                    for asset_name, candles in asset_candle_data.items():
                        signal_data = check_trade_signal(candles)
                        if signal_data:
                            direction = signal_data['direction']
                            reason = signal_data['reason']
                            confidence = signal_data['confidence']
                            signal_time = current_time.strftime("%H:%M")
                            next_time = (current_time + timedelta(minutes=1)).strftime("%H:%M")

                            signal_msg = (
                                f"📢 Signal ({tf_name})\n"
                                f"Asset: {asset_name}\n"
                                f"Time: {signal_time}–{next_time}\n"
                                f"Direction: {direction}\n"
                                f"Reason: {reason}\n"
                                f"Confidence: {confidence}%"
                            )

                            # Send to Telegram
                            send_signal_telegram(signal_msg)

                            # Log the signal
                            log_signal({
                                "timestamp": current_time.isoformat(),
                                "timeframe": tf_name,
                                "asset": asset_name,
                                "direction": direction,
                                "reason": reason,
                                "confidence": confidence,
                                "start_time": signal_time,
                                "end_time": next_time,
                                "status": "pending"
                            })
            # Validate previous signals after every loop
            validate_previous_signals()

            time.sleep(1)

        except Exception as e:
            print(f"⚠️ Error in bot loop: {e}")
            time.sleep(5)
