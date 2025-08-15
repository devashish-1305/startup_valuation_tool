import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

def calculate_vc_method(
    projected_revenue: float, 
    industry_multiple: float, 
    required_roi: float, 
    investment_amount: float
) -> dict:
    exit_value = projected_revenue * industry_multiple
    post_money_valuation = exit_value / required_roi
    pre_money_valuation = post_money_valuation - investment_amount
    
    return {
        'exit_value': exit_value,
        'post_money_valuation': post_money_valuation,
        'pre_money_valuation': pre_money_valuation
    }

# Example Test Run.
if __name__ == '__main__':
    # Assumptions about the company's future and the investment
    projected_revenue_at_exit = 50_000_000
    industry_ps_multiple = 4.0
    target_roi_multiple = 20.0
    current_investment = 2_000_000

    valuations = calculate_vc_method(
        projected_revenue_at_exit,
        industry_ps_multiple,
        target_roi_multiple,
        current_investment
    )

    print("--- Venture Capital (VC) Method Test ---")
    print(f"Implied Pre-Money Valuation Today: ${valuations['pre_money_valuation']:,.0f}")