import os
import sys
from pathlib import Path
import pandas as pd
import sqlite3
from pymongo import MongoClient
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

load_dotenv(project_root / '.env')

SQLITE_DB_PATH = project_root / 'financials.db'
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = "startup_valuation_db"
MONGO_COLLECTION_NAME = "sec_filings"

def get_sql_data(symbol: str) -> pd.DataFrame:
    print(f"Querying SQLite for {symbol}...")
    try:
        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            query = f"SELECT * FROM '{symbol}'"
            df = pd.read_sql_query(query, conn)
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            return df
    except Exception as e:
        print(f"❌ Error fetching data from SQLite for {symbol}: {e}")
        return pd.DataFrame()

def get_all_sql_data() -> pd.DataFrame:
    print("Querying SQLite for all company data...")
    try:
        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_names = [table[0] for table in cursor.fetchall()]
            
            all_dfs = [pd.read_sql_query(f"SELECT * FROM '{table}'", conn) for table in table_names]
            
            if not all_dfs:
                return pd.DataFrame()
            
            combined_df = pd.concat(all_dfs, ignore_index=True)
            if 'date' in combined_df.columns:
                combined_df['date'] = pd.to_datetime(combined_df['date'])
            return combined_df
    except Exception as e:
        print(f"❌ Error fetching all data from SQLite: {e}")
        return pd.DataFrame()

def get_mongo_document(symbol: str) -> dict:
    print(f"Querying MongoDB for {symbol}...")
    if not MONGO_URI:
        return {}
    try:
        with MongoClient(MONGO_URI) as client:
            db = client[MONGO_DB_NAME]
            collection = db[MONGO_COLLECTION_NAME]
            document = collection.find_one({'symbol': symbol, 'filing_type': '10-K'})

            # The '_id' is a non-serializable ObjectId, so we drop it for portability.
            if document and '_id' in document:
                del document['_id']
            return document if document else {}
    except Exception as e:
        print(f"❌ Error fetching data from MongoDB for {symbol}: {e}")
        return {}

def get_all_mongo_documents() -> list:
    print("Querying MongoDB for all 10-K documents...")
    if not MONGO_URI:
        return []
    try:
        with MongoClient(MONGO_URI) as client:
            db = client[MONGO_DB_NAME]
            collection = db[MONGO_COLLECTION_NAME]
            documents = list(collection.find({'filing_type': '10-K'}))
            for doc in documents:
                if '_id' in doc:
                    del doc['_id']
            return documents
    except Exception as e:
        print(f"❌ Error fetching all documents from MongoDB: {e}")
        return []