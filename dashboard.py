# File: dashboard.py
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

SIGNAL_LOG = "signals.json"

def load_signals():
    if not os.path.exists(SIGNAL_LOG):
        return []
    with open(SIGNAL_LOG, "r") as f:
        return json.load(f)

def display_signal_table(signals, timeframe):
    tf_signals = [s for s in signals if s["timeframe"] == timeframe]
    if not tf_signals:
        st.warning(f"No signals for {timeframe}")
        return

    df = pd.DataFrame(tf_signals)
    df["time"] = pd.to_datetime(df["timestamp"], unit="s").dt.strftime("%Y-%m-%d %H:%M:%S")
    df = df[["time", "asset", "signal", "result"]]
    df = df.rename(columns={
        "time": "Timestamp",
        "asset": "Pair",
        "signal": "Signal",
        "result": "Outcome"
    })

    st.dataframe(df, use_container_width=True)

    total = len(df)
    correct = df["Outcome"].str.lower().eq("correct").sum()
    incorrect = df["Outcome"].str.lower().eq("wrong").sum()
    accuracy = (correct / total) * 100 if total else 0

    st.metric(label="📈 Total Signals", value=total)
    st.metric(label="✅ Correct", value=correct)
    st.metric(label="❌ Wrong", value=incorrect)
    st.metric(label="🎯 Accuracy", value=f"{accuracy:.2f} %")

def run_dashboard():
    st.set_page_config(page_title="Pocket Option Dashboard", layout="wide")
    st.title("📊 Pocket Option Signal Dashboard")
    st.caption("🔄 Live auto-updating signals and accuracy stats for OTC & FX pairs")

    signals = load_signals()

    tabs = st.tabs(["1m", "3m", "5m", "10m"])
    timeframes = ["1m", "3m", "5m", "10m"]

    for i, tf in enumerate(timeframes):
        with tabs[i]:
            display_signal_table(signals, tf)

if __name__ == "__main__":
    run_dashboard()
