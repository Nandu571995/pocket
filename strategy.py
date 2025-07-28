# strategy.py

import ta
import numpy as np

def compute_indicators(df):
    df["ema_9"] = ta.trend.ema_indicator(df["close"], window=9)
    df["ema_21"] = ta.trend.ema_indicator(df["close"], window=21)
    df["macd"] = ta.trend.macd_diff(df["close"])
    df["rsi"] = ta.momentum.rsi(df["close"], window=14)
    bb = ta.volatility.BollingerBands(df["close"], window=20, window_dev=2)
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_lower"] = bb.bollinger_lband()
    df["bb_mid"] = bb.bollinger_mavg()
    return df

def check_trade_signal(df):
    df = compute_indicators(df)
    last = df.iloc[-1]

    signals = []

    # EMA Crossover
    if last["ema_9"] > last["ema_21"]:
        signals.append("EMA_BULLISH")
    elif last["ema_9"] < last["ema_21"]:
        signals.append("EMA_BEARISH")

    # MACD
    if last["macd"] > 0:
        signals.append("MACD_BULLISH")
    elif last["macd"] < 0:
        signals.append("MACD_BEARISH")

    # RSI
    if last["rsi"] < 30:
        signals.append("RSI_OVERSOLD")
    elif last["rsi"] > 70:
        signals.append("RSI_OVERBOUGHT")

    # Bollinger Bands
    if last["close"] < last["bb_lower"]:
        signals.append("BB_LOWER_BREAK")
    elif last["close"] > last["bb_upper"]:
        signals.append("BB_UPPER_BREAK")

    # Aggregate signal
    bullish_count = sum(1 for s in signals if "BULLISH" in s or "OVERSOLD" in s or "LOWER" in s)
    bearish_count = sum(1 for s in signals if "BEARISH" in s or "OVERBOUGHT" in s or "UPPER" in s)

    if bullish_count > bearish_count:
        direction = "GREEN"
        confidence = round((bullish_count / (bullish_count + bearish_count)) * 100, 2)
    elif bearish_count > bullish_count:
        direction = "RED"
        confidence = round((bearish_count / (bullish_count + bearish_count)) * 100, 2)
    else:
        direction = None
        confidence = 0.0

    return {
        "direction": direction,
        "confidence": confidence,
        "reasons": signals
    }
