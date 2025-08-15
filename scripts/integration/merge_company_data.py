import os
import pandas as pd

DIR_FMP = "data_sources/cleaned/fmp/"
DIR_YF  = "data_sources/cleaned/yfinance/"
DIR_SEC = "data_sources/cleaned/sec_edgar/" 
OUT_DIR = "data_sources/integrated/"
os.makedirs(OUT_DIR, exist_ok=True)
SYMBOLS = ["AAPL", "AMZN", "GOOGL", "META", "MSFT", "NFLX", "NVDA", "TSLA"]


def _load_and_prep(path):
    """Loads a CSV, converts date column, and sorts."""
    if not os.path.isfile(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    for col in df.columns:
        if 'date' in col.lower():
            df.rename(columns={col: 'date'}, inplace=True)
            break
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    return df

def merge(symbol: str):
    """
    Loads all cleaned files for a symbol and merges them using a time-series approach.
    """
  
    yf_df = _load_and_prep(os.path.join(DIR_YF,  f"{symbol}_yfinance_clean.csv"))
    cf_df = _load_and_prep(os.path.join(DIR_FMP, f"{symbol}_cash_flow_statement_clean.csv"))
    bs_df = _load_and_prep(os.path.join(DIR_FMP, f"{symbol}_balance_sheet_statement_clean.csv"))
    ic_df = _load_and_prep(os.path.join(DIR_FMP, f"{symbol}_income_statement_clean.csv"))
    
    if yf_df.empty:
        print(f"No daily yFinance data for {symbol}, cannot merge.")
        return

  
    merged_df = yf_df

   
    for fin_df in [ic_df, cf_df, bs_df]:
        if not fin_df.empty:
        
            fin_df_no_symbol = fin_df.drop(columns=['symbol'], errors='ignore')
            merged_df = pd.merge_asof(merged_df, fin_df_no_symbol, on='date', direction='backward')


    merged_df['symbol'] = symbol
    merged_df.fillna(method='ffill', inplace=True)
    merged_df.dropna(inplace=True)

    out_path = os.path.join(OUT_DIR, f"{symbol}_merged.csv")
    merged_df.to_csv(out_path, index=False)
    print(f"✅ Integrated data saved: {out_path}")


if __name__ == "__main__":
    for sym in SYMBOLS:
        try:
            merge(sym)
        except Exception as err:
            print(f"❌ Merge failed for {sym}: {err}")