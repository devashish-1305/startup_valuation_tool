import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_income_statement(symbol):
    """
    Fetch income statement data using Financial Modeling Prep API.
    """
    API_KEY = os.getenv("FMP_API_KEY")
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?apikey={API_KEY}&limit=1"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"FMP API error: {response.status_code}")

    return response.json()

# Quick local test
if __name__ == "__main__":
    data = get_income_statement("AAPL")
    print(data[0].keys())  # Print keys of the latest income statement
