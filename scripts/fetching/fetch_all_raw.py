import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from .sec_edgar_api   import fetch_sec_edgar_data
from .fmp_api         import fetch_fmp_data
from .yfinance_api    import fetch_yfinance_data 

symbols = ["META", "AMZN", "TSLA", "MSFT", "AAPL", "NVDA", "GOOGL", "NFLX"]

if __name__ == "__main__":
    for symbol in symbols:
        print(f"\n🚀 Fetching data for {symbol}...")

        try:
            fetch_yfinance_data(symbol)
            print(f"yFinance fetched for {symbol}")
        except Exception as e:
            print(f"yFinance failed for {symbol}: {e}")

        try:
            fetch_fmp_data(symbol)
            print(f"FMP fetched for {symbol}")
        except Exception as e:
            print(f"FMP failed for {symbol}: {e}")
        
        try:
            fetch_sec_edgar_data(symbol)
            print(f"SEC EDGAR fetched for {symbol}")
        except Exception as e:
            print(f"SEC EDGAR failed for {symbol}: {e}")