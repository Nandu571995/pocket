# strategy.py
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
import pandas as pd

def check_trade_signal(candles, timeframe):
    if len(candles) < 50:
        return None

    df = pd.DataFrame(candles)
    df.columns = ["timestamp", "open", "high", "low", "close"]
    df["close"] = df["close"].astype(float)

    macd = MACD(close=df["close"])
    ema = EMAIndicator(close=df["close"], window=21)
    rsi = RSIIndicator(close=df["close"], window=14)
    bb = BollingerBands(close=df["close"], window=20)

    df["macd"] = macd.macd()
    df["signal"] = macd.macd_signal()
    df["ema"] = ema.ema_indicator()
    df["rsi"] = rsi.rsi()
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_lower"] = bb.bollinger_lband()

    latest = df.iloc[-1]

    signal = None
    confidence = 0

    if (
        latest["macd"] > latest["signal"] and
        latest["close"] > latest["ema"] and
        latest["rsi"] > 50 and
        latest["close"] < latest["bb_upper"]
    ):
        signal = "GREEN"
        confidence += 25
    if (
        latest["macd"] < latest["signal"] and
        latest["close"] < latest["ema"] and
        latest["rsi"] < 50 and
        latest["close"] > latest["bb_lower"]
    ):
        signal = "RED"
        confidence += 25

    if signal:
        if 55 <= latest["rsi"] <= 70 or 30 <= latest["rsi"] <= 45:
            confidence += 25
        if abs(latest["macd"] - latest["signal"]) > 0.1:
            confidence += 25

        confidence = min(100, confidence)

    return {"signal": signal, "confidence": confidence} if signal else None
