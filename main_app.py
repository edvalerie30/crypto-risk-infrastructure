import streamlit as st
import pandas as pd
from wallet_tracker import get_wallet_data

st.set_page_config(page_title="Crypto Risk Dashboard", layout="wide")

st.title("🧠 Crypto Wallet Tracker")
st.subheader("💹 Current Wallet Balances (Live)")

# Retrieve wallet data
wallets = [
    {
        "asset": "XRP",
        "type": "xrp",
        "address": "rLj64jUj7Y4G4W2QuCEESyh3wLT8n9r6qL"
    },
    {
        "asset": "BTC",
        "type": "btc",
        "address": "bc1q8j79ls5vj2vn8gxqlsmw4mv9ag5c3w2ws577rg"
    },
    {
        "asset": "ETH",
        "type": "eth",
        "address": "0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e"
    },
    {
        "asset": "XRP",
        "type": "xrp",
        "address": "rNCvpUp1iYJXk5dt7PqSAuhRq5xEiTcZRX"
    },
    {
        "asset": "AERO",
        "type": "eth",
        "address": "0x1B4A3D3d0cC2C517B088E0E84FbF3Bb40BB5030B"
    },
    {
        "asset": "SUI",
        "type": "sui",
        "address": "0x9e549e0b5df5e250b1c1f497e5b75f5e86d7c08cd2d72c5ff8cdc28d9b116b35"
    },
    {
        "asset": "BASE",
        "type": "eth",
        "address": "0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e"
    },
]

# Fetch live data
live_df = get_wallet_data(wallets)

if live_df.empty:
    st.warning("No data available. Please check wallet connectivity or API keys.")
else:
    live_df["Balance"] = live_df["Balance"].astype(float)
    live_df["Price (USD)"] = live_df["Price (USD)"].astype(float)
    live_df["Value (USD)"] = live_df["Value (USD)"].astype(float)

    # Format
    styled_df = live_df.style.format({
        "Balance": "{:,.4f}",
        "Price (USD)": "${:,.2f}",
        "Value (USD)": "${:,.2f}"
    })

    # Display
    st.dataframe(styled_df, use_container_width=True)

    # Historical trend placeholder
    st.subheader("📈 Historical Portfolio Balance (24h)")
    chart_data = live_df.copy()
    chart_data["Time"] = pd.Timestamp.now()
    chart_data = chart_data.groupby("Asset")[["Value (USD)"]].sum()
    st.bar_chart(chart_data)

    # Balance alerts (change threshold)
    st.subheader("🔔 Balance Change Alerts")
    threshold = 0.01  # 1%
    for idx, row in live_df.iterrows():
        if abs(row.get("Change", 0)) > threshold:
            st.error(f"{row['Asset']} changed by {row['Change']*100:.2f}%!")

st.caption("Last updated: {}".format(pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")))
