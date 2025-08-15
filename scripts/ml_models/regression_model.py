import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import numpy as np

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from utils.query_utils import get_all_sql_data

def train_valuation_model():
    data = get_all_sql_data()

    if data.empty:
        print("No data found. Halting model training.")
        return None, None, None

    data['marketCap'] = data['close'] * data['sharesOutstanding']

    features = ['freeCashFlow', 'totalDebt', 'cashAndCashEquivalents', 'volume']
    target = 'marketCap'
    
    required_columns = features + [target]
    data = data.dropna(subset=required_columns)
    data = data[data[target] > 0]

    X = data[features]
    y = data[target]

    if len(data) < 10:
        print("Not enough data to train the model after cleaning.")
        return None, None, None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)

    return model, rmse, features

# Example Test Run
if __name__ == '__main__':
    print("--- Training Valuation Regression Model (XGBoost) ---")
    trained_model, model_rmse, model_features = train_valuation_model()
    
    if trained_model:
        print(f"\n✔ Model training complete.")
        print(f"  - Root Mean Squared Error (RMSE): ${model_rmse:,.0f}")
        print(f"  - Model Features: {model_features}")
        
        print("\n--- Example Prediction ---")
        sample_company = pd.DataFrame([{
            'freeCashFlow': 6.0e10,
            'totalDebt': 1.0e11,
            'cashAndCashEquivalents': 4.0e10,
            'volume': 1.5e8
        }])
        
        predicted_market_cap = trained_model.predict(sample_company)
        print(f"Predicted Market Cap for sample company: ${predicted_market_cap[0]:,.0f}")