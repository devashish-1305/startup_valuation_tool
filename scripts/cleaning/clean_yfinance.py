import pandas as pd
from pathlib import Path

RAW_DIR = Path("data_sources/raw/yfinance/")
CLEANED_DIR = Path("data_sources/cleaned/yfinance/")
SYMBOLS = ["META", "AMZN", "TSLA", "MSFT", "AAPL", "NVDA", "GOOGL", "NFLX"]

def clean_yfinance_data():
    """Cleans all yfinance historical data files."""
    print("🚀 Starting yFinance data cleaning process...")
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)

    for symbol in SYMBOLS:
        try:
            raw_file = RAW_DIR / f"{symbol}_yfinance_historical.csv"
            cleaned_file = CLEANED_DIR / f"{symbol}_yfinance_clean.csv"

            if not raw_file.exists():
                print(f"  - Skipping {symbol}: Raw file not found.")
                continue

            df = pd.read_csv(raw_file)

            df.dropna(subset=['close'], inplace=True)
            df['date'] = pd.to_datetime(df['date'])
            df.sort_values('date', inplace=True)
            df.reset_index(drop=True, inplace=True)
            df = df[df['close'] > 0]

            df.to_csv(cleaned_file, index=False)
            print(f"  ✔ Cleaned and saved: {cleaned_file.name}")

        except Exception as e:
            print(f"  Failed for {symbol}: {e}")
            
    print("\n All yFinance data cleaning complete.")


if __name__ == "__main__":
    clean_yfinance_data()