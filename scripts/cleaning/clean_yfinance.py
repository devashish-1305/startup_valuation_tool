import os
import pandas as pd

RAW_DIR = "data_sources/raw/yfinance/"
CLEANED_DIR = "data_sources/cleaned/yfinance/"

os.makedirs(CLEANED_DIR, exist_ok=True)

symbols = ["META", "AMZN", "TSLA", "MSFT", "AAPL", "NVDA", "GOOGL", "NFLX"]

def clean_yfinance_symbol(symbol):
    raw_file = os.path.join(RAW_DIR, f"{symbol}_yfinance_raw.csv")
    cleaned_file = os.path.join(CLEANED_DIR, f"{symbol}_yfinance_cleaned.csv")

    df = pd.read_csv(raw_file)

    df.dropna(subset=['close'], inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    df.reset_index(drop=True, inplace=True)


    df = df[df['close'] > 0]

    df.to_csv(cleaned_file, index=False)
    print(f" Cleaned file saved for {symbol}: {cleaned_file}")

if __name__ == "__main__":
    for symbol in symbols:
        try:
            clean_yfinance_symbol(symbol)
        except Exception as e:
            print(f"Failed for {symbol}: {e}")
