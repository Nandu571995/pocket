# File: strategy.py
import pandas as pd
import ta

def get_indicators(df):
    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=5)
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=20)
    df['macd'] = ta.trend.macd_diff(df['close'])
    df['rsi'] = ta.momentum.rsi(df['close'])
    return df

def check_trade_signal(candles):
    # Ensure input is a DataFrame
    if not isinstance(candles, pd.DataFrame):
        df = pd.DataFrame(candles)
    else:
        df = candles

    if df.empty or len(df) < 25:
        return None

    df = get_indicators(df)
    latest = df.iloc[-1]

    if (latest['ema_fast'] > latest['ema_slow'] and 
        latest['macd'] > 0 and 
        latest['rsi'] > 55):
        return {
            "direction": "BUY",
            "reason": "EMA fast > slow, MACD > 0, RSI > 55"
        }

    elif (latest['ema_fast'] < latest['ema_slow'] and 
          latest['macd'] < 0 and 
          latest['rsi'] < 45):
        return {
            "direction": "SELL",
            "reason": "EMA fast < slow, MACD < 0, RSI < 45"
        }

    return None
