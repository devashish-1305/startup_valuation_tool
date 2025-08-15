import sys
from pathlib import Path
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from utils.query_utils import get_sql_data

def forecast_stock_price(symbol: str, periods=365):
    data = get_sql_data(symbol)
    if data.empty or 'date' not in data.columns or 'close' not in data.columns:
        print(f"Not enough data for {symbol} to forecast.")
        return None, None

    df_prophet = data[['date', 'close']].rename(columns={'date': 'ds', 'close': 'y'})

    model = Prophet()
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    return model, forecast

# Example Test Run 
if __name__ == '__main__':
    target_symbol = 'AAPL'
    print(f"--- Forecasting Stock Price for {target_symbol} ---")
    
    model, forecast_data = forecast_stock_price(target_symbol)
    
    if model and forecast_data is not None:
        print("\n✔ Forecast complete.")
        print("Displaying forecast plot. Close the plot window to continue.")
        
        # Prophet has a built-in plotting function
        fig = model.plot(forecast_data)
        plt.title(f'{target_symbol} Stock Price Forecast')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()

        print("\nLast 5 rows of the forecast data:")
        # Show the predicted values ('yhat')
        print(forecast_data[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())