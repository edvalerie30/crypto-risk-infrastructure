import streamlit as st
from wallet_tracker import get_wallet_balances, get_historical_balances
import pandas as pd

st.set_page_config(page_title="Crypto Wallet Tracker", layout="wide")
st.title("🪙 Crypto Wallet Tracker")

# Live wallet balances
st.subheader("✅ Current Wallet Balances (Live)")
live_df = get_wallet_balances()
st.dataframe(live_df)

# Historical balances
st.subheader("📉 Historical Balances (Past 7 Days)")

try:
    hist_df = get_historical_balances()
    if "Wallet" in hist_df.columns and "Date" in hist_df.columns and "Balance" in hist_df.columns:
        pivot_df = hist_df.pivot(index="Date", columns="Wallet", values="Balance")
        st.line_chart(pivot_df)
    else:
        st.warning("Historical data missing expected columns.")
except Exception as e:
    st.error(f"Error displaying historical balances: {e}")
