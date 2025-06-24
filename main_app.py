import streamlit as st
import pandas as pd
from wallet_tracker import get_wallet_balances, get_historical_balances

st.set_page_config(page_title="Crypto Wallet Tracker", layout="wide")

st.title("🪙 Crypto Wallet Tracker")

st.subheader("✅ Current Wallet Balances (Live)")
live_data = get_wallet_balances()
live_df = pd.DataFrame(live_data)
live_df["Price (USD)"] = 2000.0  # Placeholder
live_df["Value (USD)"] = live_df["Balance"] * live_df["Price (USD)"]
st.dataframe(live_df.style.format({
    "Balance": "{:.4f}",
    "Price (USD)": "${:,.2f}",
    "Value (USD)": "${:,.2f}"
}))

st.subheader("📈 Historical Balances (Past 7 Days)")
hist_data = get_historical_balances()
hist_df = pd.DataFrame(hist_data)
pivot_df = hist_df.pivot(index="Date", columns="Wallet", values="Balance")
st.line_chart(pivot_df)
