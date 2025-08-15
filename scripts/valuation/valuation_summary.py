import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from utils.query_utils import get_sql_data
from scripts.valuation.dcf_model import calculate_dcf
from scripts.valuation.berkus_model import calculate_berkus
from scripts.valuation.scorecard_model import calculate_scorecard
from scripts.valuation.vc_method_model import calculate_vc_method
from scripts.valuation.risk_factor_model import calculate_risk_factor
from scripts.valuation.cost_to_duplicate_model import calculate_cost_to_duplicate

def generate_valuation_summary(symbol, assumptions):
    results = {}

    if symbol:
        results['DCF Model'] = calculate_dcf(
            symbol,
            assumptions['dcf']['growth_rate'],
            assumptions['dcf']['perpetual_rate'],
            assumptions['dcf']['discount_rate']
        )
    
    results['Berkus Method'] = calculate_berkus(assumptions['berkus'])
    results['Scorecard Method'] = calculate_scorecard(
        assumptions['scorecard']['avg_valuation'],
        assumptions['scorecard']['factors']
    )
    results['Risk Factor Summation'] = calculate_risk_factor(
        assumptions['risk_factor']['avg_valuation'],
        assumptions['risk_factor']['scores']
    )
    results['Cost-to-Duplicate'] = calculate_cost_to_duplicate(assumptions['cost_to_duplicate'])
    
    vc_results = calculate_vc_method(
        assumptions['vc']['projected_revenue'],
        assumptions['vc']['industry_multiple'],
        assumptions['vc']['required_roi'],
        assumptions['vc']['investment_amount']
    )
    results['VC Method (Pre-Money)'] = vc_results['pre_money_valuation']
    
    return results

def print_summary(results, symbol):
    print(f"--- Valuation Summary Report for: {symbol if symbol else 'Early-Stage Startup'} ---")
    print("-" * 50)
    for model, value in results.items():
        if value > 0:
            print(f"{model:<25}: ${value:,.0f}")
    print("-" * 50)
    
    startup_models = [
        'Berkus Method', 'Scorecard Method', 'Risk Factor Summation',
        'Cost-to-Duplicate', 'VC Method (Pre-Money)'
    ]
    startup_valuations = [v for k, v in results.items() if k in startup_models and v > 0]
    if startup_valuations:
        blended_startup_valuation = sum(startup_valuations) / len(startup_valuations)
        print(f"\n{'Blended Startup Valuation':<25}: ${blended_startup_valuation:,.0f}")

# Example Test Run.
if __name__ == '__main__':
    # Set a target symbol for DCF, or None for an early-stage startup
    target_symbol = 'AAPL'

    # A single dictionary holding all assumptions for all models
    all_assumptions = {
        'dcf': {
            'growth_rate': 0.06,
            'perpetual_rate': 0.025,
            'discount_rate': 0.09
        },
        'berkus': {
            'sound_idea': 400000,
            'prototype': 300000,
            'management_team': 500000,
            'strategic_relationships': 250000,
            'product_rollout': 150000
        },
        'scorecard': {
            'avg_valuation': 2_000_000,
            'factors': {
                'management_team': (0.30, 1.25),
                'size_of_opportunity': (0.25, 1.50),
                'product_technology': (0.15, 1.00),
                'competitive_environment': (0.10, 0.75),
                'marketing_sales': (0.10, 1.00),
                'need_for_funding': (0.05, 0.50),
                'other': (0.05, 1.00)
            }
        },
        'risk_factor': {
            'avg_valuation': 1_500_000,
            'scores': {
                'management_risk': 250_000,
                'stage_of_business': 125_000,
                'competition_risk': -250_000,
                'technology_risk': 250_000,
                'potential_lucrative_exit': 250_000
            }
        },
        'cost_to_duplicate': {
            'research_and_development': 150_000,
            'software_development_salaries': 250_000,
            'physical_assets_computers': 20_000
        },
        'vc': {
            'projected_revenue': 50_000_000,
            'industry_multiple': 4.0,
            'required_roi': 20.0,
            'investment_amount': 2_000_000
        }
    }
    
    summary_results = generate_valuation_summary(target_symbol, all_assumptions)
    print_summary(summary_results, target_symbol)