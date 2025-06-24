import requests
import time
from datetime import datetime
import pandas as pd

wallets = {
    "XRP 1": "rLj64jUj7Y4G4W2QuCEESyh3wLT8n9r6qL",
    "BTC": "bc1q8j79ls5vj2vn8gxqlsmw4mv9ag5c3w2ws577rg",
    "ETH": "0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e",
    "XRP 2": "rNCvpUp1iYJXk5dt7PqSAuhRq5xEiTcZRX",
    "AERO": "0x1B4A3D3d0cC2C517B088E0E84FbF3Bb40BB5030B",
    "SUI": "0x9e549e0b5df5e250b1c1f497e5b75f5e86d7c08cd2d72c5ff8cdc28d9b116b35",
    "BASE": "0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e"
}

def get_wallet_balances():
    results = []
    prices = get_prices()

    for label, address in wallets.items():
        chain = detect_chain(address)

        if chain == "BTC":
            bal = get_btc_balance(address)
        elif chain == "ETH":
            bal = get_eth_balance(address)
        elif chain == "XRP":
            bal = get_xrp_balance(address)
        elif chain == "SUI":
            bal = get_sui_balance(address)
        else:
            bal = 0

        price = prices.get(chain, 0)
        value = bal * price
        results.append({
            "Label": label,
            "Chain": chain,
            "Address": address,
            "Balance": round(bal, 4),
            "Price (USD)": round(price, 2),
            "Value (USD)": round(value, 2)
        })

    return results

def get_prices():
    ids = "bitcoin,ethereum,ripple,sui,base"
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    r = requests.get(url).json()
    return {
        "BTC": r["bitcoin"]["usd"],
        "ETH": r["ethereum"]["usd"],
        "XRP": r["ripple"]["usd"],
        "SUI": r["sui"]["usd"],
        "BASE": r["base"]["usd"] if "base" in r else 0
    }

def detect_chain(address):
    if address.startswith("r"):
        return "XRP"
    if address.startswith("bc1"):
        return "BTC"
    if address.startswith("0x") and len(address) == 42:
        return "ETH"  # Could be ETH, AERO, BASE
    if address.startswith("0x") and len(address) > 42:
        return "SUI"
    return "UNKNOWN"

def get_btc_balance(address):
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
    r = requests.get(url).json()
    return r.get("final_balance", 0) / 1e8

def get_eth_balance(address):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey=YourApiKeyToken"
    r = requests.get(url).json()
    return int(r.get("result", 0)) / 1e18

def get_xrp_balance(address):
    url = f"https://api.xrpscan.com/api/v1/account/{address}/balances"
    r = requests.get(url).json()
    return float(r[0]["value"]) if r else 0

def get_sui_balance(address):
    return 0  # Placeholder unless you use Sui API

def get_historical_balances():
    data = []
    for _ in range(7):
        snapshot = get_wallet_balances()
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        for entry in snapshot:
            entry["Timestamp"] = timestamp
            data.append(entry)
        time.sleep(1)
    return pd.DataFrame(data)
