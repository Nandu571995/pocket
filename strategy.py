# strategy.py

import pandas as pd
import ta

def analyze_signal(df):
    try:
        df = df.copy()
        df['close'] = df['close'].astype(float)

        # Indicators
        df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=9).fillna(0)
        df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=21).fillna(0)
        macd = ta.trend.MACD(df['close'])
        df['macd'] = macd.macd().fillna(0)
        df['macd_signal'] = macd.macd_signal().fillna(0)
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi().fillna(0)
        bb = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2)
        df['bb_upper'] = bb.bollinger_hband().fillna(0)
        df['bb_lower'] = bb.bollinger_lband().fillna(0)

        latest = df.iloc[-1]

        reasons = []
        confidence = 0
        signal = "NO_SIGNAL"

        # EMA crossover
        if latest['ema_fast'] > latest['ema_slow']:
            reasons.append("EMA Bullish Crossover")
            confidence += 20
        elif latest['ema_fast'] < latest['ema_slow']:
            reasons.append("EMA Bearish Crossover")
            confidence += 20

        # MACD crossover
        if latest['macd'] > latest['macd_signal']:
            reasons.append("MACD Bullish Crossover")
            confidence += 25
        elif latest['macd'] < latest['macd_signal']:
            reasons.append("MACD Bearish Crossover")
            confidence += 25

        # RSI filter
        if latest['rsi'] < 30:
            reasons.append("RSI Oversold")
            confidence += 15
        elif latest['rsi'] > 70:
            reasons.append("RSI Overbought")
            confidence += 15

        # Bollinger Band check
        if latest['close'] < latest['bb_lower']:
            reasons.append("Price Below Bollinger Band")
            confidence += 15
        elif latest['close'] > latest['bb_upper']:
            reasons.append("Price Above Bollinger Band")
            confidence += 15

        # Final signal decision
        if confidence >= 50:
            signal = "BUY" if "Bullish" in " ".join(reasons) or "Oversold" in " ".join(reasons) else "SELL"

        return {
            "signal": signal,
            "reason": ", ".join(reasons) if reasons else "No strong signal",
            "confidence": confidence
        }

    except Exception as e:
        print(f"Error in analyze_signal: {e}")
        return {"signal": "NO_SIGNAL", "reason": "Error", "confidence": 0}
