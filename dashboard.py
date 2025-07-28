# dashboard.py
import streamlit as st
import json
import pandas as pd
from datetime import datetime

SIGNALS_FILE = "signals.json"

def load_signals():
    try:
        with open(SIGNALS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"1m": [], "3m": [], "5m": [], "10m": []}

def calculate_stats(tf_data):
    total = len(tf_data)
    wins = sum(1 for s in tf_data if s["result"] == "WIN")
    losses = sum(1 for s in tf_data if s["result"] == "LOSS")
    pending = total - wins - losses
    accuracy = (wins / total * 100) if total else 0
    return total, wins, losses, pending, round(accuracy, 2)

def display_tf_tab(tf, tf_data):
    st.subheader(f"🕒 {tf} Signals")

    if not tf_data:
        st.info("No signals yet.")
        return

    df = pd.DataFrame(tf_data)
    df["Timestamp"] = df["time"]
    df["Pair"] = df["pair"]
    df["Signal"] = df["direction"]
    df["Confidence"] = df["confidence"]
    df["Result"] = df["result"]
    df = df[["Timestamp", "Pair", "Signal", "Confidence", "Result"]]

    st.dataframe(df, use_container_width=True)

    total, wins, losses, pending, accuracy = calculate_stats(tf_data)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📈 Total", total)
    col2.metric("✅ Win", wins)
    col3.metric("❌ Loss", losses)
    col4.metric("⏳ Pending", pending)
    col5.metric("🎯 Accuracy", f"{accuracy:.2f}%")

def main():
    st.set_page_config(page_title="Pocket Option Signal Dashboard", layout="wide")
    st.title("📊 Real-Time Pocket Option Signal Dashboard")
    st.caption("Live auto-updating signals for OTC & Currency Pairs - Timeframes: 1m, 3m, 5m, 10m")

    signals = load_signals()

    tabs = st.tabs(["1m", "3m", "5m", "10m"])
    for i, tf in enumerate(["1m", "3m", "5m", "10m"]):
        with tabs[i]:
            display_tf_tab(tf, signals.get(tf, []))

if __name__ == "__main__":
    main()
