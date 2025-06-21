import requests
import json
import datetime
import os

CONFIG_FILE = "config.json"
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "prices.log")

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def get_crypto_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    resp = requests.get(url)
    data = resp.json()
    return data[symbol]["usd"]

def check_alert(price, min_val, max_val):
    if price < min_val:
        return f"🔻 {price} below {min_val}"
    if price > max_val:
        return f"🔺 {price} above {max_val}"
    return None

def log_price(asset, price, alert_msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"{timestamp} | {asset['symbol']} | ${price} | {alert_msg or '✅ OK'}"
    print(log)
    with open(LOG_FILE, "a") as f:
        f.write(log + "\n")

def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    config = load_config()
    for asset in config["assets"]:
        try:
            price = get_crypto_price(asset["name"])
            alert = check_alert(price, asset["min"], asset["max"])
            log_price(asset, price, alert)
        except Exception as e:
            print(f"Error fetching {asset['symbol']}: {e}")

if __name__ == "__main__":
    main()