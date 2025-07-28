# dashboard.py

import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="📊 Pocket Option Signal Dashboard", layout="wide")

SIGNALS_FILE = "signals.json"

def load_signals():
    if not os.path.exists(SIGNALS_FILE):
        return {}
    with open(SIGNALS_FILE, "r") as f:
        return json.load(f)

def display_signal(signal):
    st.markdown(f"""
    #### 🕒 {signal['timeframe'].upper()} | `{signal['symbol']}` | {signal['direction'].upper()}
    - **Confidence:** {signal['confidence']}%
    - **Reason:** {signal['reason']}
    - **Signal Time:** {signal['signal_time']} → {signal['expiry_time']}
    - **Status:** {'✅ Correct' if signal['status'] == 'correct' else '❌ Wrong' if signal['status'] == 'wrong' else '🕒 Pending'}
    ---
    """)

def show_signals_tab(signals, timeframe):
    st.header(f"{timeframe.upper()} Signals")
    filtered = [s for s in signals.get(timeframe, [])][::-1]
    if not filtered:
        st.warning(f"No {timeframe} signals yet.")
    for s in filtered:
        display_signal(s)

def show_performance(signals):
    st.header("📈 Performance")
    for tf in signals:
        all_signals = signals[tf]
        correct = sum(1 for s in all_signals if s['status'] == 'correct')
        wrong = sum(1 for s in all_signals if s['status'] == 'wrong')
        pending = sum(1 for s in all_signals if s['status'] == 'pending')
        total = len(all_signals)
        accuracy = (correct / total) * 100 if total else 0
        st.subheader(f"{tf.upper()} Timeframe")
        st.text(f"✅ Correct: {correct}")
        st.text(f"❌ Wrong: {wrong}")
        st.text(f"🕒 Pending: {pending}")
        st.text(f"📊 Accuracy: {accuracy:.2f}%")
        st.markdown("---")

def run_dashboard():
    st.title("📡 Pocket Option Trading Bot Dashboard")
    st.markdown("Real-time signals from all OTC and currency pairs across 1m, 3m, 5m, 10m timeframes.")
    signals = load_signals()

    tabs = st.tabs(["1m", "3m", "5m", "10m", "Performance"])
    timeframes = ["1m", "3m", "5m", "10m"]

    for i, tf in enumerate(timeframes):
        with tabs[i]:
            show_signals_tab(signals, tf)

    with tabs[-1]:
        show_performance(signals)

if __name__ == "__main__":
    run_dashboard()
