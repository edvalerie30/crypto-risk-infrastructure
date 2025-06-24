import requests
import time
import datetime
import pandas as pd

ETHERSCAN_API_KEY = "T7GD3KIYX7I4UEDCUSX5XR17K8JJAFMQR3"

WALLETS = [
    {"label": "XRP_1", "address": "rLj64jUj7Y4G4W2QuCEESyh3wLT8n9r6qL", "token": "XRP"},
    {"label": "XRP_2", "address": "rNCvpUp1iYJXk5dt7PqSAuhRq5xEiTcZRX", "token": "XRP"},
    {"label": "BTC", "address": "bc1q8j79ls5vj2vn8gxqlsmw4mv9ag5c3w2ws577rg", "token": "BTC"},
    {"label": "ETH", "address": "0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e", "token": "ETH"},
    {"label": "AERO", "address": "0x1B4A3D3d0cC2C517B088E0E84FbF3Bb40BB5030B", "token": "AERO"},
    {"label": "SUI", "address": "0x9e549e0b5df5e250b1c1f497e5b75f5e86d7c08cd2d72c5ff8cdc28d9b116b35", "token": "SUI"},
    {"label": "BASE", "address": "0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e", "token": "BASE"}
]

def get_eth_balance(address):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    r = requests.get(url)
    result = r.json().get("result", "0")
    return int(result) / 1e18

def get_token_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,ripple,sui,aerodrome-finance,base",
        "vs_currencies": "usd"
    }
    r = requests.get(url, params=params)
    data = r.json()
    return {
        "BTC": data.get("bitcoin", {}).get("usd", 0),
        "ETH": data.get("ethereum", {}).get("usd", 0),
        "XRP": data.get("ripple", {}).get("usd", 0),
        "SUI": data.get("sui", {}).get("usd", 0),
        "AERO": data.get("aerodrome-finance", {}).get("usd", 0),
        "BASE": data.get("base", {}).get("usd", 0)
    }

def get_wallet_balances():
    balances = []
    prices = get_token_prices()

    for wallet in WALLETS:
        token = wallet["token"]
        label = wallet["label"]
        address = wallet["address"]

        if token == "ETH" or token == "BASE":
            bal = get_eth_balance(address)
        else:
            bal = 0.0  # For now placeholder, other APIs needed for XRP, BTC, SUI

        price = prices.get(token, 0)
        balances.append({
            "Wallet": label,
            "Address": address,
            "Balance": bal,
            "Token": token,
            "Price (USD)": price,
            "Value (USD)": bal * price
        })
    return pd.DataFrame(balances)

def get_historical_balances():
    today = datetime.date.today()
    data = []
    for i in range(7):
        fake_balances = get_wallet_balances()
        fake_balances["Date"] = today - datetime.timedelta(days=i)
        data.append(fake_balances)
        time.sleep(1)
    df = pd.concat(data)
    return df
