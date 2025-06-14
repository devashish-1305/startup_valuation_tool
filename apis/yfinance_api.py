import yfinance as yf

def get_stock_data_yf(symbol):
    """
    Fetch historical stock data using Yahoo Finance (yfinance).
    """
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y") 
    return hist

# Quick local test
if __name__ == "__main__":
    data = get_stock_data_yf("AAPL")
    print(data.head())
