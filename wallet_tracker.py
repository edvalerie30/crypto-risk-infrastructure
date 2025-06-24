import pandas as pd
import requests
import time

# Define wallet addresses
wallets = {
    "XRP 1": ("XRP", "rLj64jUj7Y4G4W2QuCEESyh3wLT8n9r6qL"),
    "BTC": ("BTC", "bc1q8j79ls5vj2vn8gxqlsmw4mv9ag5c3w2ws577rg"),
    "ETH": ("ETH", "0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e"),
    "XRP 2": ("XRP", "rNCvpUp1iYJXk5dt7PqSAuhRq5xEiTcZRX"),
    "AERO": ("AERO", "0x1B4A3D3d0cC2C517B088E0E84FbF3Bb40BB5030B"),
    "SUI": ("SUI", "0x9e549e0b5df5e250b1c1f497e5b75f5e86d7c08cd2d72c5ff8cdc28d9b116b35"),
    "BASE": ("ETH", "0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e")
}

# Get USD prices from CoinGecko
def get_usd_price(symbol):
    ids = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "XRP": "ripple",
        "AERO": "aerodrome-finance",
        "SUI": "sui"
    }
    try:
        if symbol not in ids: return None
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids[symbol]}&vs_currencies=usd"
        return requests.get(url).json()[ids[symbol]]["usd"]
    except:
        return None

# Fetch balance per wallet
def get_balance(symbol, address):
    try:
        if symbol == "BTC":
            url = f"https://blockchain.info/q/addressbalance/{address}"
            return int(requests.get(url).text) / 1e8
        elif symbol == "ETH":
            url = f"https://api.blockchair.com/ethereum/dashboards/address/{address}"
            data = requests.get(url).json()
            return int(data["data"][address]["address"]["balance"]) / 1e18
        elif symbol == "XRP":
            url = f"https://data.ripple.com/v2/accounts/{address}/balances"
            balances = requests.get(url).json()["balances"]
            for b in balances:
                if b["currency"] == "XRP":
                    return float(b["value"])
        elif symbol == "AERO":
            return 0.0  # Placeholder
        elif symbol == "SUI":
            return 0.0  # Placeholder
    except:
        return None

# Live tracker
def get_live_wallet_data():
    data = []
    for label, (symbol, addr) in wallets.items():
        balance = get_balance(symbol, addr)
        price = get_usd_price(symbol)
        value = balance * price if balance and price else None
        data.append({
            "Wallet": label,
            "Symbol": symbol,
            "Address": addr,
            "Balance": balance,
            "Price (USD)": price,
            "Value (USD)": value
        })
        time.sleep(1.2)
    df = pd.DataFrame(data)
    df["Balance"] = pd.to_numeric(df["Balance"], errors="coerce")
    df["Price (USD)"] = pd.to_numeric(df["Price (USD)"], errors="coerce")
    df["Value (USD)"] = pd.to_numeric(df["Value (USD)"], errors="coerce")
    return df
