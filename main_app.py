import streamlit as st
import pandas as pd
from wallet_tracker import get_all_balances, update_historical_log

st.set_page_config(page_title="Crypto Risk Dashboard", layout="wide")

st.title("📡 Crypto Wallet Tracker")

# Live wallet snapshot
st.subheader("🟢 Current Wallet Balances (Live)")
live_df = get_all_balances()
st.dataframe(live_df.style.format({
    "Balance": "{:,.4f}",
    "Price (USD)": "${:,.2f}",
    "Value (USD)": "${:,.2f}"
}))

st.metric("📈 Total Portfolio Value", f"${live_df['Value (USD)'].sum():,.2f}")

# Historical trend chart
st.subheader("📊 Historical Balance Trend")
hist_df = update_historical_log()
hist_df["Timestamp"] = pd.to_datetime(hist_df["Timestamp"])

chart_df = hist_df.set_index("Timestamp").drop(columns=["Asset"])
st.line_chart(chart_df)
