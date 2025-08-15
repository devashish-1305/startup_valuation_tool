import os
import yfinance as yf
import pandas as pd

SAVE_DIR = "data_sources/raw/yfinance"

def fetch_yfinance_data(symbol: str):
    """
    Fetches 10 years of historical daily stock data for a given symbol
    and overwrites the existing file.
    """
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    filename = f"{SAVE_DIR}/{symbol}_yfinance_historical.csv"
    
    try:
        ticker = yf.Ticker(symbol)
        
        hist_df = ticker.history(period="10y")
        
        if hist_df.empty:
            print(f"  ⚠️ Warning: No historical data found for {symbol}.")
            return
            
        hist_df.reset_index(inplace=True)
        hist_df['date'] = pd.to_datetime(hist_df['Date']).dt.date
        
        hist_df = hist_df[['date', 'Close', 'Volume']].rename(columns={
            'Close': 'close',
            'Volume': 'volume'
        })
        
        hist_df.to_csv(filename, index=False)
        print(f"  ✔ Success: Saved latest yFinance data to {os.path.basename(filename)}")
        
    except Exception as e:
        print(f"  ❌ yFinance failed for {symbol}: {e}")

if __name__ == "__main__":
    symbols = ["META", "AMZN", "TSLA", "MSFT", "AAPL", "NVDA", "GOOGL", "NFLX"]
    for symbol in symbols:
        fetch_yfinance_data(symbol)