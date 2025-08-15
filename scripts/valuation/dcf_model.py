import sys
from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from utils.query_utils import get_sql_data

def calculate_dcf(symbol: str, growth_rate: float, perpetual_rate: float, discount_rate: float, projection_years=5):
    """
    Calculates a simplified intrinsic value using data from the database.
    """
    df = get_sql_data(symbol)
    if df.empty:
        print(f"❌ Could not retrieve data for {symbol}. Cannot calculate DCF.")
        return 0.0

    latest = df.sort_values(by='date', ascending=False).iloc[0]

    last_fcf = latest.get('freeCashFlow')
    shares_out = latest.get('sharesOutstanding')
    total_debt = latest.get('totalDebt', 0)
    cash = latest.get('cashAndCashEquivalents', 0)

    if pd.isna(last_fcf) or pd.isna(shares_out) or shares_out == 0:
        print(f"⚠️ Warning: Missing FCF or shares outstanding for {symbol}. Cannot calculate DCF.")
        return 0.0

    fcf_projections = [last_fcf * (1 + growth_rate) ** year for year in range(1, projection_years + 1)]
    pv_fcf = [fcf / (1 + discount_rate) ** (i + 1) for i, fcf in enumerate(fcf_projections)]

    terminal_value = (fcf_projections[-1] * (1 + perpetual_rate)) / (discount_rate - perpetual_rate)
    pv_terminal_value = terminal_value / (1 + discount_rate) ** projection_years

    enterprise_value = sum(pv_fcf) + pv_terminal_value
    equity_value = enterprise_value - total_debt + cash

    intrinsic_value = equity_value / shares_out
    return intrinsic_value

# Example Test Run.
if __name__ == '__main__':
    symbol = 'AAPL'

    g_rate = 0.06      # Assumed 5-year FCF growth rate
    p_rate = 0.025     # Assumed perpetual growth rate
    wacc = 0.09        # Discount rate (WACC)

    value = calculate_dcf(symbol, g_rate, p_rate, wacc)

    if value > 0:
        print(f"DCF Intrinsic Value for {symbol}: ${value:.2f}")