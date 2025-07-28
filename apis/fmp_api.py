import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"
SAVE_DIR = "data_sources/raw/fmp"

def fetch_fmp_data(symbol):  
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    filename = f"{SAVE_DIR}/{symbol}_fmp_raw.csv"
    if os.path.exists(filename):
        print(f" Skipping FMP: {filename} already exists.")
        return

    print(f" Fetching FMP data for {symbol}...")

    endpoints = {
        "ratios-ttm": f"{BASE_URL}/ratios-ttm/{symbol}?apikey={FMP_API_KEY}",
        "key_metrics-ttm": f"{BASE_URL}/key-metrics-ttm/{symbol}?apikey={FMP_API_KEY}",
        "profile": f"{BASE_URL}/profile/{symbol}?apikey={FMP_API_KEY}"
    }

    merged_data = {}
    for label, url in endpoints.items():
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.json():
                merged_data.update(response.json()[0])
            else:
                print(f" Failed to fetch {label} for {symbol} (Status: {response.status_code})")
        except Exception as e:
            print(f" Error fetching {label} for {symbol}: {e}")

    if merged_data:
        df = pd.DataFrame([merged_data])
        df.to_csv(filename, index=False)
        print(f" FMP data saved to {filename}")
    else:
        print(f" FMP failed: No valid data for {symbol}")
        raise Exception(f"No valid FMP data retrieved for {symbol}")

if __name__ == "__main__":
    symbols = ["META", "AMZN", "TSLA", "MSFT", "AAPL", "NVDA", "GOOGL", "NFLX"]
    for symbol in symbols:
        fetch_fmp_data(symbol)