import pandas as pd
from pathlib import Path

RAW_DIR = Path("data_sources/raw/fmp")
CLEANED_DIR = Path("data_sources/cleaned/fmp")
SYMBOLS = ["META", "AMZN", "TSLA", "MSFT", "AAPL", "NVDA", "GOOGL", "NFLX"]

COLUMN_MAP = {
    'date': ['date'],
    'symbol': ['symbol'],
    'freeCashFlow': ['freeCashFlow'],
    'totalDebt': ['totalDebt'],
    'cashAndCashEquivalents': ['cashAndCashEquivalents'],
    'sharesOutstanding': ['sharesOutstanding', 'weightedAverageShsOut', 'weightedAverageShsOutDil']
}


def clean_file(raw_path: Path, cleaned_path: Path):
    """
    Reads a raw file, finds and standardizes columns based on COLUMN_MAP,
    and saves a cleaned version containing only the desired columns.
    """
    if not raw_path.exists():
        return

    df = pd.read_csv(raw_path)
    df_cleaned = pd.DataFrame()

    # Find and copy each required column using its standard name
    for standard_name, possible_names in COLUMN_MAP.items():
        for raw_name in possible_names:
            if raw_name in df.columns:
                df_cleaned[standard_name] = df[raw_name]
                break 
    # Format date column if it was found
    if 'date' in df_cleaned.columns:
        df_cleaned['date'] = pd.to_datetime(df_cleaned['date'])
        df_cleaned.sort_values('date', ascending=False, inplace=True)

    if not df_cleaned.empty:
        # Save only the columns that were actually found
        df_cleaned.to_csv(cleaned_path, index=False)
        print(f"  ✔ Cleaned and saved: {cleaned_path.name}")

def clean_fmp_data():
    """Main function to orchestrate the cleaning of all FMP files."""
    print("🚀 Starting FMP data cleaning process...")
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)

    # List all the file types we fetched
    file_types = ["cash_flow_statement", "balance_sheet_statement", "income_statement", "key_metrics_ttm"]

    for symbol in SYMBOLS:
        print(f"\nProcessing symbol: {symbol}")
        for file_type in file_types:
            raw_file = RAW_DIR / f"{symbol}_{file_type}.csv"
            cleaned_file = CLEANED_DIR / f"{symbol}_{file_type}_clean.csv"
            clean_file(raw_file, cleaned_file)

    print("\n All FMP data cleaning complete.")


if __name__ == "__main__":
    clean_fmp_data()