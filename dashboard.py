import streamlit as st
import json
import os
from datetime import datetime
from collections import defaultdict

SIGNALS_FILE = "signals.json"

def load_signals():
    if not os.path.exists(SIGNALS_FILE):
        return []

    try:
        with open(SIGNALS_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list) and all(isinstance(s, dict) for s in data):
                return data
            else:
                return []
    except Exception as e:
        print("Error loading signals.json:", e)
        return []


def filter_signals_by_tf(signals, tf):
    return [s for s in signals if s.get("timeframe") == tf]

def calculate_performance(signals):
    performance = defaultdict(lambda: {"total": 0, "correct": 0})
    for sig in signals:
        tf = sig.get("timeframe")
        if tf:
            performance[tf]["total"] += 1
            if sig.get("validated") is True:
                performance[tf]["correct"] += 1
    return performance

def format_signal(sig):
    time_range = sig.get("time_range", "")
    pair = sig.get("pair", "N/A")
    direction = sig.get("direction", "?")
    confidence = sig.get("confidence", "?")
    reason = sig.get("reason", "")
    return f"🕒 *{time_range}* | 💱 `{pair}` | 📊 *{direction.upper()}* | 🎯 Confidence: *{confidence}%*\n🧠 *Reason:* {reason}"

def display_signals(signals, timeframe):
    tf_signals = filter_signals_by_tf(signals, timeframe)
    if not tf_signals:
        st.info("No signals yet.")
        return
    for sig in reversed(tf_signals[-10:]):  # show last 10
        st.markdown(format_signal(sig), unsafe_allow_html=True)
        st.divider()

def display_performance(performance):
    st.markdown("### ✅ Signal Accuracy by Timeframe")
    for tf, stats in performance.items():
        total = stats["total"]
        correct = stats["correct"]
        if total > 0:
            accuracy = round((correct / total) * 100, 2)
            st.success(f"🕒 {tf} | ✅ {correct}/{total} | 🎯 *{accuracy}%*")
        else:
            st.warning(f"🕒 {tf} | No signals yet.")

def main():
    st.set_page_config(layout="wide", page_title="📊 Pocket Option Dashboard")
    st.title("📊 Pocket Option Trading Dashboard")

    tab1, tab2, tab3, tab4, perf_tab = st.tabs(["1-Min", "3-Min", "5-Min", "10-Min", "📈 Performance"])

    signals = load_signals()
    performance = calculate_performance(signals)

    with tab1:
        display_signals(signals, "1m")
    with tab2:
        display_signals(signals, "3m")
    with tab3:
        display_signals(signals, "5m")
    with tab4:
        display_signals(signals, "10m")
    with perf_tab:
        display_performance(performance)

# ✅ Required by Render to import
def run_dashboard():
    main()

# Run directly if executed standalone
if __name__ == "__main__":
    main()
