import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_daily_prices(symbol):
    """
    Fetch daily adjusted stock prices using Alpha Vantage.
    """
    API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
    
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Alpha Vantage API error: {response.status_code}")

    return response.json()

# Quick local test
if __name__ == "__main__":
    data = get_daily_prices("AAPL")
    print(list(data.keys()))
