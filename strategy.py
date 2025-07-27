import pandas as pd
import ta

def check_trade_signal(candles):
    df = pd.DataFrame(candles)
    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=5)
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=20)
    df['macd'] = ta.trend.macd_diff(df['close'])

    if df['ema_fast'].iloc[-1] > df['ema_slow'].iloc[-1] and df['macd'].iloc[-1] > 0:
        return "BUY"
    elif df['ema_fast'].iloc[-1] < df['ema_slow'].iloc[-1] and df['macd'].iloc[-1] < 0:
        return "SELL"
    return None
