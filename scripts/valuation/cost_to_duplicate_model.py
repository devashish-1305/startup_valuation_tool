import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

def calculate_cost_to_duplicate(costs: dict) -> float:
    return sum(costs.values())

# .Example Test Run.
if __name__ == '__main__':
    # Estimate the costs to rebuild the company's assets from scratch
    cost_items = {
        'research_and_development': 150_000,
        'software_development_salaries': 250_000,
        'patents_and_trademarks': 25_000,
        'physical_assets_computers': 20_000,
        'marketing_brand_setup': 50_000
    }

    total_valuation = calculate_cost_to_duplicate(cost_items)

    print("--- Cost-to-Duplicate Method Test ---")
    print(f"Calculated Valuation: ${total_valuation:,.0f}")