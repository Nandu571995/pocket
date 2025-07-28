import ta
import pandas as pd

def calculate_indicators(df):
    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=5).fillna(0)
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=20).fillna(0)
    macd = ta.trend.macd_diff(df['close']).fillna(0)
    df['macd'] = macd
    df['rsi'] = ta.momentum.rsi(df['close'], window=14).fillna(0)
    bb = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband().fillna(0)
    df['bb_lower'] = bb.bollinger_lband().fillna(0)
    return df

def check_trade_signal(candles):
    try:
        df = pd.DataFrame(candles)
        df.columns = ['timestamp', 'open', 'high', 'low', 'close']
        df = df.astype(float)
        df = calculate_indicators(df)

        last = df.iloc[-1]
        previous = df.iloc[-2]

        signal = None
        reason = []
        confidence = 50

        # EMA Crossover
        if previous['ema_fast'] < previous['ema_slow'] and last['ema_fast'] > last['ema_slow']:
            signal = 'buy'
            reason.append('EMA crossover')
            confidence += 10
        elif previous['ema_fast'] > previous['ema_slow'] and last['ema_fast'] < last['ema_slow']:
            signal = 'sell'
            reason.append('EMA crossover')
            confidence += 10

        # MACD Confirmation
        if last['macd'] > 0 and signal == 'buy':
            reason.append('MACD > 0')
            confidence += 10
        elif last['macd'] < 0 and signal == 'sell':
            reason.append('MACD < 0')
            confidence += 10

        # RSI Filter
        if last['rsi'] < 30 and signal == 'buy':
            reason.append('RSI < 30')
            confidence += 10
        elif last['rsi'] > 70 and signal == 'sell':
            reason.append('RSI > 70')
            confidence += 10

        # Bollinger Bounce
        if last['close'] <= last['bb_lower']:
            reason.append('Close at lower BB')
            if signal != 'sell':
                signal = 'buy'
                confidence += 5
        elif last['close'] >= last['bb_upper']:
            reason.append('Close at upper BB')
            if signal != 'buy':
                signal = 'sell'
                confidence += 5

        if signal:
            return {
                'direction': 'GREEN' if signal == 'buy' else 'RED',
                'reason': ', '.join(reason),
                'confidence': min(confidence, 100)
            }
        return None

    except Exception as e:
        print(f"⚠️ Error in analyze_signal: {e}")
        return None
