import sys
import os
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "startup_valuation_db"
COLLECTION_NAME = "sec_filings"
RAW_DIR = Path("data_sources/raw/sec_edgar")

def push_sec_to_mongo():
    print("🚀 Starting MongoDB push process for SEC filings...")
    
    # TEMPORARY DEBUGGING CODE.
    print("\n--- DEBUGGING ---")
    print(f"Script is using this MONGO_URI: {MONGO_URI}")
    print("--- END DEBUGGING ---\n")
    # ---

    if not MONGO_URI:
        print("❌ MONGO_URI not found in .env file. Please add it.")
        return

    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        print(f"Connected to MongoDB. Pushing to '{DB_NAME}.{COLLECTION_NAME}'...")
    except Exception as e:
        print(f"❌ Could not connect to MongoDB. Check your connection string. Error: {e}")
        return

    # ... (rest of the script is the same) ...
    txt_files = list(RAW_DIR.glob("*/*_10k_latest.txt"))
    if not txt_files:
        print("⚠️ No 10-K .txt files found to process.")
        client.close()
        return

    pushed_count = 0
    for file_path in txt_files:
        try:
            symbol = file_path.parent.name
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            document = {"symbol": symbol, "filing_type": "10-K", "content": content}
            
            collection.update_one(
                {'symbol': symbol, 'filing_type': '10-K'},
                {'$set': document},
                upsert=True
            )
            print(f"  ✔ Upserted 10-K for {symbol}")
            pushed_count += 1
        except Exception as e:
            print(f"  ❌ Error processing file {file_path.name}: {e}")

    client.close()
    print(f"\n✅ MongoDB push complete. {pushed_count} documents were pushed.")

if __name__ == "__main__":
    push_sec_to_mongo()