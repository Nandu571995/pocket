# File: strategy.py
import pandas as pd
import ta

def get_indicators(df):
    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=5)
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=20)
    df['macd'] = ta.trend.macd_diff(df['close'])
    df['rsi'] = ta.momentum.rsi(df['close'])
    return df

def check_trade_signal(df):
    df = get_indicators(df)

    latest = df.iloc[-1]

    # Strategy: EMA crossover + MACD + RSI confirmation
    if (latest['ema_fast'] > latest['ema_slow'] and 
        latest['macd'] > 0 and 
        latest['rsi'] > 55):
        return "BUY"
    elif (latest['ema_fast'] < latest['ema_slow'] and 
          latest['macd'] < 0 and 
          latest['rsi'] < 45):
        return "SELL"
    return None
