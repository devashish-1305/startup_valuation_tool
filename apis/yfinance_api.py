import os
import yfinance as yf
import pandas as pd
from datetime import datetime

SAVE_DIR = "data_sources/raw/yfinance"

def fetch_yfinance_data(symbol):
    # Create directory if it doesn't exist
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    filename = f"{SAVE_DIR}/{symbol}_yfinance_raw.csv"
    if os.path.exists(filename):
        print(f" Skipping yFinance: {filename} already exists.")
        return

    print(f" Fetching yFinance data for {symbol}...")
    
    try:
        # Create ticker object
        ticker = yf.Ticker(symbol)
        
        # Fetch various data
        info = ticker.info
        
        # Extract key metrics
        data = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'marketCap': info.get('marketCap'),
            'enterpriseValue': info.get('enterpriseValue'),
            'trailingPE': info.get('trailingPE'),
            'forwardPE': info.get('forwardPE'),
            'pegRatio': info.get('pegRatio'),
            'priceToSalesTrailing12Months': info.get('priceToSalesTrailing12Months'),
            'priceToBook': info.get('priceToBook'),
            'enterpriseToRevenue': info.get('enterpriseToRevenue'),
            'enterpriseToEbitda': info.get('enterpriseToEbitda'),
            'beta': info.get('beta'),
            'profitMargins': info.get('profitMargins'),
            'grossMargins': info.get('grossMargins'),
            'operatingMargins': info.get('operatingMargins'),
            'returnOnAssets': info.get('returnOnAssets'),
            'returnOnEquity': info.get('returnOnEquity'),
            'revenue': info.get('totalRevenue'),
            'revenuePerShare': info.get('revenuePerShare'),
            'quarterlyRevenueGrowth': info.get('quarterlyRevenueGrowth'),
            'grossProfit': info.get('grossProfit'),
            'ebitda': info.get('ebitda'),
            'netIncomeToCommon': info.get('netIncomeToCommon'),
            'trailingEps': info.get('trailingEps'),
            'forwardEps': info.get('forwardEps'),
            'totalCash': info.get('totalCash'),
            'totalCashPerShare': info.get('totalCashPerShare'),
            'totalDebt': info.get('totalDebt'),
            'debtToEquity': info.get('debtToEquity'),
            'currentRatio': info.get('currentRatio'),
            'bookValue': info.get('bookValue'),
            'operatingCashflow': info.get('operatingCashflow'),
            'freeCashflow': info.get('freeCashflow'),
            'sharesOutstanding': info.get('sharesOutstanding'),
            'floatShares': info.get('floatShares'),
            'avgVolume': info.get('averageVolume'),
            'avgVolume10days': info.get('averageVolume10days'),
            'bid': info.get('bid'),
            'ask': info.get('ask'),
            'bidSize': info.get('bidSize'),
            'askSize': info.get('askSize'),
            'previousClose': info.get('previousClose'),
            'open': info.get('open'),
            'dayLow': info.get('dayLow'),
            'dayHigh': info.get('dayHigh'),
            'regularMarketPreviousClose': info.get('regularMarketPreviousClose'),
            'regularMarketOpen': info.get('regularMarketOpen'),
            'regularMarketDayLow': info.get('regularMarketDayLow'),
            'regularMarketDayHigh': info.get('regularMarketDayHigh'),
            'dividendRate': info.get('dividendRate'),
            'dividendYield': info.get('dividendYield'),
            'exDividendDate': info.get('exDividendDate'),
            'payoutRatio': info.get('payoutRatio'),
            'fiveYearAvgDividendYield': info.get('fiveYearAvgDividendYield'),
            'lastSplitFactor': info.get('lastSplitFactor'),
            'lastSplitDate': info.get('lastSplitDate'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'fullTimeEmployees': info.get('fullTimeEmployees'),
            'website': info.get('website'),
            'country': info.get('country'),
            'currency': info.get('currency')
        }
        
        df = pd.DataFrame([data])
        df.to_csv(filename, index=False)
        print(f" yFinance data saved to {filename}")
        
    except Exception as e:
        print(f" yFinance failed: Error fetching data for {symbol}: {e}")
        raise

if __name__ == "__main__":
    symbols = ["META", "AMZN", "TSLA", "MSFT", "AAPL", "NVDA", "GOOGL", "NFLX"]
    for symbol in symbols:
        fetch_yfinance_data(symbol)