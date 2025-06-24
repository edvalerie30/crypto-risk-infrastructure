# wallet_tracker_advanced.py
import requests
import pandas as pd
from datetime import datetime

COINGECKO_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "XRP": "ripple",
    "AERO": "aerodrome-finance",
    "SUI": "sui",
    "BASE": "base"
}

WALLET_ADDRESSES = {
    "BTC": ["bc1q8j79ls5vj2vn8gxqlsmw4mv9ag5c3w2ws577rg"],
    "ETH": ["0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e"],
    "XRP": [
        "rLj64jUj7Y4G4W2QuCEESyh3wLT8n9r6qL",
        "rNCvpUp1iYJXk5dt7PqSAuhRq5xEiTcZRX"
    ],
    "SUI": ["0x9e549e0b5df5e250b1c1f497e5b75f5e86d7c08cd2d72c5ff8cdc28d9b116b35"],
    "AERO": ["0x1B4A3D3d0cC2C517B088E0E84FbF3Bb40BB5030B"]
}

HISTORICAL_BALANCE_LOG = "balance_log.csv"


def fetch_price_usd(token_symbol):
    token_id = COINGECKO_IDS.get(token_symbol.upper())
    if not token_id:
        return None
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd"
        response = requests.get(url, timeout=10).json()
        return response[token_id]["usd"]
    except Exception:
        return None


def fetch_sample_balance(chain, address):
    # Placeholder function – replace with actual API integration
    if chain == "BTC":
        return 0.23
    elif chain == "ETH":
        return 2.1
    elif chain == "XRP":
        return 3400
    elif chain == "SUI":
        return 800
    elif chain == "AERO":
        return 2500
    return 0


def get_all_balances():
    rows = []
    for chain, addresses in WALLET_ADDRESSES.items():
        total = 0
        for addr in addresses:
            balance = fetch_sample_balance(chain, addr)
            total += balance
        price = fetch_price_usd(chain)
        value = total * price if price is not None else None
        rows.append({
            "Asset": chain,
            "Balance": total,
            "Price (USD)": price,
            "Value (USD)": value
        })
    return pd.DataFrame(rows)


def update_historical_log():
    df = get_all_balances()
    df["Timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    df.set_index("Timestamp", inplace=True)
    df = df.T  # transpose so assets are columns

    try:
        existing = pd.read_csv(HISTORICAL_BALANCE_LOG, index_col=0)
        merged = pd.concat([existing, df])
    except FileNotFoundError:
        merged = df

    merged.to_csv(HISTORICAL_BALANCE_LOG)
    return merged.T.reset_index().rename(columns={"index": "Timestamp"})


if __name__ == "__main__":
    latest = get_all_balances()
    print("Current Portfolio:")
    print(latest)

    print("\nUpdated Balance History:")
    history = update_historical_log()
    print(history.tail())
