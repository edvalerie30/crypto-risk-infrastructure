import streamlit as st
import pandas as pd
from wallet_tracker import get_wallet_balances, get_historical_balances

st.set_page_config(page_title="Crypto Wallet Tracker", layout="wide")

st.title("🪙 Crypto Wallet Tracker")
st.subheader("✅ Current Wallet Balances (Live)")

# Fetch current wallet balances
live_df = get_wallet_balances()

# Display live balances
st.dataframe(live_df.style.format({
    "Balance": "{:,.4f}",
    "Price (USD)": "${:,.2f}",
    "Value (USD)": "${:,.2f}"
}))

# Display line chart for balance history
st.markdown("---")
st.subheader("📈 Historical Balance Trends")

history_df = get_historical_balances()

if not history_df.empty:
    for symbol in history_df["Symbol"].unique():
        token_df = history_df[history_df["Symbol"] == symbol]
        st.line_chart(
            token_df.set_index("Timestamp")[["Balance"]],
            height=250,
            use_container_width=True
        )
else:
    st.info("No historical data available yet. Please wait for balance polling to accumulate over time.")

# Show alert section
st.markdown("---")
st.subheader("🔔 Balance Alerts")

if "alerts" in st.session_state and st.session_state["alerts"]:
    for alert in st.session_state["alerts"]:
        st.warning(alert)
else:
    st.success("No alerts triggered.")
