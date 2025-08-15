import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

def calculate_risk_factor(avg_valuation: float, risk_scores: dict) -> float:
    risk_adjustment = sum(risk_scores.values())
    adjusted_valuation = avg_valuation + risk_adjustment
    return adjusted_valuation

# --- Example Test Run ---
if __name__ == '__main__':
    #Let's Start with an average valuation for a comparable business
    average_company_valuation = 1_500_000

    # Assign a monetary value (+ or -) to each key risk factor.
    # +$250k for very low risk, -$250k for very high risk.
    risk_factor_scores = {
        'management_risk': 250_000,     # Strong, experienced team
        'stage_of_business': 125_000,   # Post-revenue, early traction
        'political_risk': 0,            # Neutral political climate
        'manufacturing_risk': -125_000, # Some supply chain uncertainties
        'sales_and_marketing_risk': 0,  # Standard go-to-market plan
        'funding_risk': 250_000,        # Well-capitalized, long runway
        'competition_risk': -250_000,   # Highly competitive market
        'technology_risk': 250_000,     # Proven, stable technology
        'litigation_risk': 0,           # No pending lawsuits
        'international_risk': 0,        # Domestic-only for now
        'reputation_risk': 125_000,     # Positive early press
        'potential_lucrative_exit': 250_000 # Attractive to large acquirers
    }

    final_valuation = calculate_risk_factor(average_company_valuation, risk_factor_scores)

    print("--- Risk Factor Summation Method Test ---")
    print(f"Average Valuation Start Point: ${average_company_valuation:,.0f}")
    print(f"Total Risk Adjustment: ${sum(risk_factor_scores.values()):,.0f}")
    print(f"\nFinal Adjusted Valuation: ${final_valuation:,.0f}")