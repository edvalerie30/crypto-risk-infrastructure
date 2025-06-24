# wallet_tracker.py

import requests
import pandas as pd

def get_xrp_balance(address):
    url = f"https://api.xrpscan.com/api/v1/account/{address}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data.get("balance", 0)) / 1_000_000
    except Exception:
        return None

def get_btc_balance(address):
    url = f"https://blockstream.info/api/address/{address}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data["chain_stats"]["funded_txo_sum"] / 1e8 - data["chain_stats"]["spent_txo_sum"] / 1e8
    except Exception:
        return None

def get_eth_balance(address):
    url = f"https://api.ethplorer.io/getAddressInfo/{address}?apiKey=freekey"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data.get("ETH", {}).get("balance", 0))
    except Exception:
        return None

def get_erc20_balance(address, token_symbol):
    url = f"https://api.ethplorer.io/getAddressInfo/{address}?apiKey=freekey"
    try:
        response = requests.get(url, timeout=10)
        tokens = response.json().get("tokens", [])
        for token in tokens:
            if token["tokenInfo"]["symbol"].upper() == token_symbol.upper():
                return float(token["balance"]) / (10 ** int(token["tokenInfo"]["decimals"]))
        return 0
    except Exception:
        return None

def get_sui_balance(address):
    # Placeholder - replace with real Sui API integration if needed
    return None

def get_wallet_balances():
    wallets = {
        "XRP Wallet 1": ("XRP", "rLj64jUj7Y4G4W2QuCEESyh3wLT8n9r6qL"),
        "XRP Wallet 2": ("XRP", "rNCvpUp1iYJXk5dt7PqSAuhRq5xEiTcZRX"),
        "BTC Wallet": ("BTC", "bc1q8j79ls5vj2vn8gxqlsmw4mv9ag5c3w2ws577rg"),
        "ETH Wallet": ("ETH", "0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e"),
        "AERO (ERC-20)": ("ERC20", ("0x1B4A3D3d0cC2C517B088E0E84FbF3Bb40BB5030B", "AERO")),
        "SUI Wallet": ("SUI", "0x9e549e0b5df5e250b1c1f497e5b75f5e86d7c08cd2d72c5ff8cdc28d9b116b35"),
        "BASE (ETH)": ("ETH", "0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e"),
    }

    results = []
    for label, (chain, data) in wallets.items():
        if chain == "XRP":
            balance = get_xrp_balance(data)
        elif chain == "BTC":
            balance = get_btc_balance(data)
        elif chain == "ETH":
            balance = get_eth_balance(data)
        elif chain == "ERC20":
            address, token = data
            balance = get_erc20_balance(address, token)
        elif chain == "SUI":
            balance = get_sui_balance(data)
        else:
            balance = None

        results.append({
            "Wallet": label,
            "Chain": chain,
            "Balance": balance
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    print(get_wallet_balances())
