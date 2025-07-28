import ta
import pandas as pd

def analyze_signal(candles):
    df = pd.DataFrame(candles)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('timestamp', inplace=True)

    df['ema_5'] = ta.trend.ema_indicator(df['close'], window=5).ema_indicator()
    df['ema_20'] = ta.trend.ema_indicator(df['close'], window=20).ema_indicator()
    macd = ta.trend.macd(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    bb = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    reasons = []
    confidence = 0

    # EMA crossover
    if prev['ema_5'] < prev['ema_20'] and latest['ema_5'] > latest['ema_20']:
        reasons.append("EMA Bullish Crossover")
        confidence += 25
    elif prev['ema_5'] > prev['ema_20'] and latest['ema_5'] < latest['ema_20']:
        reasons.append("EMA Bearish Crossover")
        confidence += 25

    # MACD crossover
    if prev['macd'] < prev['macd_signal'] and latest['macd'] > latest['macd_signal']:
        reasons.append("MACD Bullish Crossover")
        confidence += 25
    elif prev['macd'] > prev['macd_signal'] and latest['macd'] < latest['macd_signal']:
        reasons.append("MACD Bearish Crossover")
        confidence += 25

    # RSI
    if latest['rsi'] < 30:
        reasons.append("RSI Oversold")
        confidence += 15
    elif latest['rsi'] > 70:
        reasons.append("RSI Overbought")
        confidence += 15

    # Bollinger Band bounce
    if latest['close'] < latest['bb_lower']:
        reasons.append("Bollinger Lower Band Bounce")
        confidence += 10
    elif latest['close'] > latest['bb_upper']:
        reasons.append("Bollinger Upper Band Rejection")
        confidence += 10

    direction = None
    if "Bullish" in " ".join(reasons) or "Oversold" in " ".join(reasons) or "Lower Band" in " ".join(reasons):
        direction = "GREEN"
    elif "Bearish" in " ".join(reasons) or "Overbought" in " ".join(reasons) or "Upper Band" in " ".join(reasons):
        direction = "RED"

    return direction, confidence, reasons
