import os
from datetime import datetime
import pandas as pd

RAW_DIR = "data_sources/raw/fmp/"
CLEANED_DIR = "data_sources/cleaned/fmp/"
os.makedirs(CLEANED_DIR, exist_ok=True)

symbols   = ["AAPL", "AMZN", "GOOGL", "META", "MSFT", "NFLX", "NVDA", "TSLA"]
keep_cols = ["date", "revenue", "netIncome", "EBITDA",
             "ROE", "P/B", "P/E"]        


def _find(df, words):
    for c in df.columns:
        cl = c.lower()
        if any(w in cl for w in words):
            return c
    return None


def clean_fmp_symbol(sym):
    raw     = os.path.join(RAW_DIR,     f"{sym}_fmp_raw.csv")
    cleaned = os.path.join(CLEANED_DIR, f"{sym}_fmp_cleaned.csv")
    df = pd.read_csv(raw)
    df.columns = [c.strip() for c in df.columns]

    rev = _find(df, ["revenue"])                   
    if rev:
        if rev != "revenue":
            df.rename(columns={rev: "revenue"}, inplace=True)
    else:
        df["revenue"] = pd.NA

    date_col = _find(df, ["date", "fiscal", "calendar", "period"])
    if date_col:
        df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    else:
        df["date"] = pd.to_datetime(datetime.today().date())

    df.dropna(subset=["revenue"], inplace=True)
    df.sort_values("date", inplace=True)
    df.drop_duplicates(subset=["date"], inplace=True)

    df = df[[c for c in keep_cols if c in df.columns]]
    df.to_csv(cleaned, index=False)
    print(f"✅ Cleaned FMP for {sym}: {cleaned}")


if __name__ == "__main__":
    for s in symbols:
        try:
            clean_fmp_symbol(s)
        except Exception as e:
            print(f"❌ FMP failed for {s}: {e}")