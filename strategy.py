# strategy.py

import pandas as pd
import numpy as np
import ta

def preprocess_data(df):
    df = df.copy()
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['open'] = pd.to_numeric(df['open'], errors='coerce')
    df['high'] = pd.to_numeric(df['high'], errors='coerce')
    df['low'] = pd.to_numeric(df['low'], errors='coerce')
    df.dropna(inplace=True)
    return df

def calculate_indicators(df):
    df = df.copy()
    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=9)
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=21)
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    bb = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    return df

def evaluate_signal(df):
    df = preprocess_data(df)
    df = calculate_indicators(df)

    last = df.iloc[-1]
    second_last = df.iloc[-2]

    score_buy = 0
    score_sell = 0

    # EMA crossover
    if last['ema_fast'] > last['ema_slow'] and second_last['ema_fast'] <= second_last['ema_slow']:
        score_buy += 1
    elif last['ema_fast'] < last['ema_slow'] and second_last['ema_fast'] >= second_last['ema_slow']:
        score_sell += 1

    # MACD crossover
    if last['macd'] > last['macd_signal'] and second_last['macd'] <= second_last['macd_signal']:
        score_buy += 1
    elif last['macd'] < last['macd_signal'] and second_last['macd'] >= second_last['macd_signal']:
        score_sell += 1

    # RSI zone
    if last['rsi'] < 30:
        score_buy += 1
    elif last['rsi'] > 70:
        score_sell += 1

    # Bollinger band signal
    if last['close'] < last['bb_lower']:
        score_buy += 1
    elif last['close'] > last['bb_upper']:
        score_sell += 1

    confidence_buy = int((score_buy / 4) * 100)
    confidence_sell = int((score_sell / 4) * 100)

    if score_buy > score_sell:
        return 'BUY', confidence_buy
    elif score_sell > score_buy:
        return 'SELL', confidence_sell
    else:
        return None, 0  # No clear signal

