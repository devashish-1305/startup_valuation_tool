import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/stable"
SAVE_DIR = "data_sources/raw/fmp"


def fetch_and_save_json(url: str, file_path: str, force: bool = True):
    """Fetch JSON from FMP and save as CSV. Overwrites by default so ETL refreshes."""
    if (not force) and os.path.exists(file_path):
        print(f"  Skipping: {os.path.basename(file_path)} already exists.")
        return

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and data.get("Error Message"):
            print(f"  ❌ API error for {os.path.basename(file_path)}: {data['Error Message']}")
            return

        if data:
            df = pd.DataFrame(data if isinstance(data, list) else [data])
            df.to_csv(file_path, index=False)
            print(f"  ✔ Success: Saved data to {os.path.basename(file_path)}")
        else:
            print(f"  ⚠️ Warning: No data returned from {url.split('apikey=')[0]}apikey=***")

    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error fetching {os.path.basename(file_path)}: {e}")
    except Exception as e:
        print(f"  ❌ An unexpected error occurred: {e}")


def fetch_fmp_data(symbol: str):
    """
    Fetches key financial statements and metrics for a given symbol from FMP stable API.
    """
    print(f"\n🚀 Fetching FMP data for {symbol}...")
    os.makedirs(SAVE_DIR, exist_ok=True)

    endpoints = {
        "cash_flow_statement": f"{BASE_URL}/cash-flow-statement?symbol={symbol}&period=annual&apikey={FMP_API_KEY}",
        "balance_sheet_statement": f"{BASE_URL}/balance-sheet-statement?symbol={symbol}&period=annual&apikey={FMP_API_KEY}",
        "income_statement": f"{BASE_URL}/income-statement?symbol={symbol}&period=annual&apikey={FMP_API_KEY}",
        "key_metrics_ttm": f"{BASE_URL}/key-metrics-ttm?symbol={symbol}&apikey={FMP_API_KEY}",
    }

    for label, url in endpoints.items():
        filename = f"{SAVE_DIR}/{symbol}_{label}.csv"
        fetch_and_save_json(url, filename)


if __name__ == "__main__":
    symbols = ["META", "AMZN", "TSLA", "MSFT", "AAPL", "NVDA", "GOOGL", "NFLX"]
    for symbol in symbols:
        fetch_fmp_data(symbol)
    print("\n✅ All FMP data fetching complete.")
