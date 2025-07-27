import pandas as pd
import ta

def default_strategy(df):
    if df.shape[0] < 20:
        return None
    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=5).ema_indicator()
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=13).ema_indicator()
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    latest = df.iloc[-1]
    if latest['rsi'] < 30 and latest['ema_fast'] > latest['ema_slow']:
        return "BUY"
    elif latest['rsi'] > 70 and latest['ema_fast'] < latest['ema_slow']:
        return "SELL"
    return None