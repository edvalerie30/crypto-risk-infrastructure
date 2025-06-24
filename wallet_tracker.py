import requests
import time
from datetime import datetime, timedelta
import pandas as pd

ETHERSCAN_API_KEY = "T7GD3KIYX7I4UEDCUSX5XR17K8JJAFMQR3"
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"

WALLETS = [
    {"label": "XRP_1", "address": "rLj64jUj7Y4G4W2QuCEESyh3wLT8n9r6qL", "token": "XRP"},
    {"label": "XRP_2", "address": "rNCvpUp1vJjvK5dt7PqSAuhRq5sEiTcZRX", "token": "XRP"},
    {"label": "BTC", "address": "bc1q8j79ls5vj2vn8gqxlsmw4mv9ag5c3w2ws577rg", "token": "BTC"},
    {"label": "ETH", "address": "0xEEebb89716DDE1b3A17732CFC1A6dDEF75F8c87e", "token": "ETH"},
    {"label": "AERO", "address": "0x1B4A3D3d0cC2C517B088E0E84FbF3Bb40BB5030B", "token": "AERO"},
    {"label": "SUI", "address": "0x9e549e0b5df5e250b1c1f497e5b75f5e86d7c08cd2d72c5ff8cdc28d9b116b35", "token": "SUI"},
    {"label": "BASE", "address": "0xEEebb89716DDE1b3A17732CFC1A6dDEF75F8c87e", "token": "BASE"},
]

def get_eth_balance(address):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&apikey={ETHERSCAN_API_KEY}"
    r = requests.get(url).json()
    return int(r.get("result", 0)) / 1e18

def get_token_prices():
    symbols = ["bitcoin", "ethereum", "ripple", "aerodrome-finance", "sui"]
    ids = "%2C".join(symbols)
    r = requests.get(f"{COINGECKO_API}?ids={ids}&vs_currencies=usd").json()
    return {
        "BTC": r.get("bitcoin", {}).get("usd", 0),
        "ETH": r.get("ethereum", {}).get("usd", 0),
        "XRP": r.get("ripple", {}).get("usd", 0),
        "AERO": r.get("aerodrome-finance", {}).get("usd", 0),
        "SUI": r.get("sui", {}).get("usd", 0),
        "BASE": r.get("ethereum", {}).get("usd", 0),
    }

def get_wallet_balances():
    prices = get_token_prices()
    rows = []
    for wallet in WALLETS:
        token = wallet["token"]
        label = wallet["label"]
        address = wallet["address"]

        if token == "ETH" or token == "BASE":
            bal = get_eth_balance(address)
        else:
            bal = 0.0  # Extend for other blockchains

        price = prices.get(token, 0)
        value = bal * price

        rows.append({
            "Wallet": label,
            "Address": address,
            "Balance": round(bal, 4),
            "Token": token,
            "Price (USD)": f"${price:,.2f}",
            "Value (USD)": f"${value:,.2f}",
        })
    return pd.DataFrame(rows)

def get_historical_balances():
    today = datetime.now()
    return pd.DataFrame({
        "Timestamp": [today - timedelta(days=i) for i in range(7)][::-1],
        "BASE": [0.0367 for _ in range(7)],
        "ETH": [0.0367 for _ in range(7)],
        "BTC": [0.0 for _ in range(7)],
        "XRP_1": [0.0 for _ in range(7)],
        "XRP_2": [0.0 for _ in range(7)],
        "AERO": [0.0 for _ in range(7)],
        "SUI": [0.0 for _ in range(7)]
    })
