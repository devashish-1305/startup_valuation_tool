import sqlite3
import pandas as pd
from pathlib import Path

INTEGRATED_DIR = Path("data_sources/integrated")
DB_PATH = Path("financials.db")

def push_to_db():
    print("🚀 Starting database push process...")
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        csv_files = list(INTEGRATED_DIR.glob("*_merged.csv"))

        if not csv_files:
            print(f"❌ No merged CSV files found in {INTEGRATED_DIR}. Halting.")
            return

        print(f"Found {len(csv_files)} CSV files to process.")

        for file_path in csv_files:
            try:
                table_name = file_path.stem.split('_')[0]
                print(f"  - Processing {file_path.name} -> Pushing to table '{table_name}'...")
                df = pd.read_csv(file_path)
                df.to_sql(
                    name=table_name,
                    con=conn,
                    if_exists="replace",
                    index=False
                )
                print(f"  ✔ Success: Table '{table_name}' created/replaced.")
            except Exception as e:
                print(f"  ❌ Error processing {file_path.name}: {e}")

    print(f"\n✅ Database push complete. All data saved to '{DB_PATH}'.")

if __name__ == "__main__":
    push_to_db()