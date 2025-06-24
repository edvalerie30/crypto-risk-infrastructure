import requests
import datetime

ETHERSCAN_API_KEY = "T7GD3KIYX7I4UEDCUSX5XR17K8JJAFMQR3"

WALLETS = {
    "XRP_1": "rLj64jUj7Y4G4W2QuCEESyh3wLT8n9r6qL",
    "XRP_2": "rNCvpUp1iYJXk5dt7PqSAuhRq5xEiTcZRX",
    "BTC": "bc1q8j79ls5vj2vn8gxqlsmw4mv9ag5c3w2ws577rg",
    "ETH": "0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e",
    "AERO": "0x1B4A3D3d0cC2C517B088E0E84FbF3Bb40BB5030B",
    "SUI": "0x9e549e0b5df5e250b1c1f497e5b75f5e86d7c08cd2d72c5ff8cdc28d9b116b35",
    "BASE": "0xEEebb89716DDE1b3A17732CFc1A6dDEF75F8c87e",
}

def get_eth_balance(address):
    url = (
        f"https://api.etherscan.io/api?module=account&action=balance"
        f"&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    )
    try:
        response = requests.get(url).json()
        wei = int(response.get("result", 0))
        return wei / 1e18  # Convert from Wei to ETH
    except Exception as e:
        print(f"[ETH] Error fetching balance: {e}")
        return 0.0

def get_wallet_balances():
    results = []
    for name, address in WALLETS.items():
        if name.startswith("ETH") or name.startswith("BASE") or name.startswith("AERO"):
            balance = get_eth_balance(address)
        else:
            balance = 0.0  # placeholder for XRP, BTC, SUI
        results.append({
            "Wallet": name,
            "Address": address,
            "Balance": balance,
            "Token": name.split("_")[0]
        })
    return results

def get_historical_balances():
    today = datetime.date.today()
    history = []
    for i in range(7):
        date = today - datetime.timedelta(days=i)
        for name, address in WALLETS.items():
            balance = get_eth_balance(address) if "ETH" in name or "BASE" in name or "AERO" in name else 0.0
            history.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Wallet": name,
                "Balance": balance
            })
    return history
