import pandas as pd
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def check_trade_signal(candles):
    df = pd.DataFrame(candles)

    if len(df) < 30:
        return None  # Not enough data

    # Calculate indicators
    df['ema_fast'] = EMAIndicator(close=df['close'], window=5).ema_indicator()
    df['ema_slow'] = EMAIndicator(close=df['close'], window=20).ema_indicator()
    macd = MACD(close=df['close'])
    df['macd_diff'] = macd.macd_diff()
    df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()
    bb = BollingerBands(close=df['close'], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()

    df = df.dropna()
    if df.empty:
        return None

    last = df.iloc[-1]

    # Composite signal logic
    if (
        last['ema_fast'] > last['ema_slow'] and
        last['macd_diff'] > 0 and
        last['rsi'] < 70 and
        last['close'] < last['bb_upper']
    ):
        return "BUY"

    elif (
        last['ema_fast'] < last['ema_slow'] and
        last['macd_diff'] < 0 and
        last['rsi'] > 30 and
        last['close'] > last['bb_lower']
    ):
        return "SELL"

    return None
