# dashboard.py

import streamlit as st
import json
import os
from datetime import datetime

SIGNAL_FILE = "signals.json"
TIMEFRAMES = ["1m", "3m", "5m", "10m"]

# Helper to load signals
def load_signals():
    if os.path.exists(SIGNAL_FILE):
        with open(SIGNAL_FILE, "r") as f:
            return json.load(f)
    return []

# Performance tracker
def compute_performance(signals):
    stats = {tf: {"total": 0, "correct": 0, "wrong": 0} for tf in TIMEFRAMES}
    for s in signals:
        tf = s["timeframe"]
        if tf in stats:
            stats[tf]["total"] += 1
            if s.get("result") == "correct":
                stats[tf]["correct"] += 1
            elif s.get("result") == "wrong":
                stats[tf]["wrong"] += 1
    return stats

# UI
def run_dashboard():
    st.set_page_config(page_title="📈 Pocket Option Realtime Signals", layout="wide")
    st.title("📡 Pocket Option Realtime Signals & Performance")

    menu = st.sidebar.radio("📊 Select View", ["Live Signals", "Performance"])

    signals = load_signals()

    if menu == "Live Signals":
        tabs = st.tabs(TIMEFRAMES)
        for i, tf in enumerate(TIMEFRAMES):
            with tabs[i]:
                st.subheader(f"⚡ {tf} Signals")
                tf_signals = [s for s in signals if s["timeframe"] == tf]
                tf_signals.reverse()
                for s in tf_signals[:20]:
                    st.markdown(f"""
                        - 🕒 **{s['start']} - {s['end']}**
                        - 💹 **Asset:** `{s['symbol']}`
                        - 📈 **Action:** `{s['signal']}`  
                        - 🎯 **Confidence:** `{s['confidence']}%`  
                        - 🧾 **Generated:** `{s['timestamp']}`  
                        - ✅ **Result:** `{s.get('result', 'pending')}`
                        ---
                    """)

    elif menu == "Performance":
        st.subheader("📊 Signal Accuracy by Timeframe")
        stats = compute_performance(signals)
        for tf, stat in stats.items():
            total = stat["total"]
            correct = stat["correct"]
            wrong = stat["wrong"]
            accuracy = round((correct / total) * 100, 2) if total > 0 else 0
            st.markdown(f"""
                ### ⏱️ {tf} Timeframe
                - Total Signals: **{total}**
                - ✅ Correct: **{correct}**
                - ❌ Wrong: **{wrong}**
                - 🎯 Accuracy: **{accuracy}%**
                ---
            """)
