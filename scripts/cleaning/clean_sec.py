import os
import shutil
import pandas as pd

RAW_DIR     = "data_sources/raw/sec_edgar"
CLEANED_DIR = "data_sources/cleaned/sec_edgar"
os.makedirs(CLEANED_DIR, exist_ok=True)

symbols   = ["AAPL", "AMZN", "GOOGL", "META",
             "MSFT", "NFLX", "NVDA", "TSLA"]

meta_keep = ["filing_date", "form_type", "report_period_end_date",
             "accession_number", "file_url", "extraction_date"]


def clean_metadata(sym: str):
    src = os.path.join(RAW_DIR, sym, f"{sym}_metadata.csv")
    dst = os.path.join(CLEANED_DIR,  f"{sym}_metadata_cleaned.csv")
    if not os.path.isfile(src):
        print(f" metadata missing for {sym}")
        return

    df = pd.read_csv(src)
    df.columns = [c.strip() for c in df.columns]

    for c in df.columns:
        if "date" in c.lower():
            df[c] = pd.to_datetime(df[c], errors="coerce")

    if "filing_date" in df.columns:
        df.sort_values("filing_date", inplace=True)
    df.drop_duplicates(inplace=True)

    df = df[[c for c in meta_keep if c in df.columns]]
    df.to_csv(dst, index=False)
    print(f" metadata cleaned for {sym}")


def clean_10k(sym: str):
    src = os.path.join(RAW_DIR, sym, f"{sym}_10k_latest.txt")
    dst = os.path.join(CLEANED_DIR,  f"{sym}_10k_latest.html")
    if not os.path.isfile(src):
        print(f"⚠️  10-K file missing for {sym}")
        return

    shutil.copyfile(src, dst)
    print(f"10-K copied → {dst}")


if __name__ == "__main__":
    for s in symbols:
        try:
            clean_metadata(s)
            clean_10k(s)
        except Exception as e:
            print(f"SEC cleaning failed for {s}: {e}")