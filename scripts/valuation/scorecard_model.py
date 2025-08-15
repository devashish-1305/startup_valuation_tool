import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

def calculate_scorecard(avg_pre_money_valuation: float, factors: dict) -> float:
    sum_of_factors = 0.0
    for weight, rating in factors.values():
        sum_of_factors += weight * rating

    valuation = avg_pre_money_valuation * sum_of_factors
    return valuation

# Example Test Run.
if __name__ == '__main__':
    #We will take Average valuation for similar startups in the same market.
    average_valuation = 2_000_000

    # Weights for each factor and the rating vs. an average company (1.0 = avg)
    scorecard_factors = {
        'management_team':       (0.30, 1.25),
        'size_of_opportunity':   (0.25, 1.50),
        'product_technology':    (0.15, 1.00),
        'competitive_environment': (0.10, 0.75),
        'marketing_sales':       (0.10, 1.00),
        'need_for_funding':      (0.05, 0.50),
        'other':                 (0.05, 1.00)
    }

    final_valuation = calculate_scorecard(average_valuation, scorecard_factors)

    print("--- Scorecard Valuation Method Test ---")
    print(f"Calculated Valuation: ${final_valuation:,.0f}")