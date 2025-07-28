import os
import sys
import pandas as pd

DIR_FMP = "data_sources/cleaned/fmp/"
DIR_YF  = "data_sources/cleaned/yfinance/"
DIR_SEC = "data_sources/cleaned/sec_edgar/"
OUT_DIR = "data_sources/integrated/"
os.makedirs(OUT_DIR, exist_ok=True)

symbols = (
    [s.strip().upper() for s in sys.argv[1].split(",")]
    if len(sys.argv) > 1
    else ["AAPL", "AMZN", "GOOGL", "META", "MSFT", "NFLX", "NVDA", "TSLA"]
)


def _detect_date_column(df):
    """Return the first column that looks like a date, or None."""
    for col in df.columns:
        low = col.lower()
        if low in {"date", "filing_date", "timestamp"} or low.endswith("_date"):
            return col
    return None


def _load_normalise(path):
    if not os.path.isfile(path):
        return pd.DataFrame()

    df = pd.read_csv(path)
    date_col = _detect_date_column(df)
    if date_col is None:
        return pd.DataFrame()

    df[date_col] = (
        pd.to_datetime(df[date_col], errors="coerce", utc=True)
        .dt.tz_localize(None)
    )
    df.dropna(subset=[date_col], inplace=True)
    df.rename(columns={date_col: "date"}, inplace=True)
    return df


def merge(symbol: str):
    fmp = _load_normalise(os.path.join(DIR_FMP, f"{symbol}_fmp_cleaned.csv"))
    yf  = _load_normalise(os.path.join(DIR_YF,  f"{symbol}_yfinance_cleaned.csv"))
    sec = _load_normalise(os.path.join(DIR_SEC, f"{symbol}_metadata_cleaned.csv"))

    if fmp.empty and yf.empty:
        print(f"No FMP/YF data for {symbol}")
        return

    frames = [df for df in (fmp, yf) if not df.empty]
    df = frames[0] if len(frames) == 1 else pd.merge(
        frames[0], frames[1], on="date", how="outer", suffixes=("_fmp", "_yf")
    )

    if not sec.empty:
        df = pd.merge(df, sec, on="date", how="left")

    df.sort_values("date", inplace=True, ignore_index=True)
    out_path = os.path.join(OUT_DIR, f"{symbol}_merged.csv")
    df.to_csv(out_path, index=False)
    print(f"Integrated saved: {out_path}")


if __name__ == "__main__":
    for sym in symbols:
        try:
            merge(sym)
        except Exception as err:
            print(f"Merge failed for {sym}: {err}")