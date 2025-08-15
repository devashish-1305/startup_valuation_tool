import sys
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from xgboost import XGBRegressor
import joblib

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from utils.query_utils import get_all_sql_data

def prepare_and_save_models():
   
    data = get_all_sql_data()
    if data.empty:
        print("No data found. Halting.")
        return

    # 1. Train and Save Clustering Model.
    features_cluster = ['freeCashFlow', 'totalDebt', 'cashAndCashEquivalents', 'volume']
    data_cluster = data.dropna(subset=features_cluster).copy()
    
    if len(data_cluster) > 3:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(data_cluster[features_cluster])
        kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
        kmeans.fit(X_scaled)
        
        joblib.dump(kmeans, 'clustering_model.joblib')
        joblib.dump(scaler, 'clustering_scaler.joblib')
        print("✔ Clustering model and scaler saved.")

    # 2. Train and Save Regression Model.
    data_reg = data.copy()
    data_reg['marketCap'] = data_reg['close'] * data_reg['sharesOutstanding']
    features_reg = ['freeCashFlow', 'totalDebt', 'cashAndCashEquivalents', 'volume']
    target_reg = 'marketCap'
    
    required_cols_reg = features_reg + [target_reg]
    data_reg = data_reg.dropna(subset=required_cols_reg)
    data_reg = data_reg[data_reg[target_reg] > 0]
    
    if len(data_reg) > 10:
        X_reg = data_reg[features_reg]
        y_reg = data_reg[target_reg]
        
        xgb_model = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
        xgb_model.fit(X_reg, y_reg)
        
        joblib.dump(xgb_model, 'regression_model.joblib')
        print("✔ Regression model saved.")

# --- Example Test Run ---
if __name__ == '__main__':
    print("--- Training and Saving All Production ML Models ---")
    prepare_and_save_models()
    print("\nAll models have been trained and saved to files.")