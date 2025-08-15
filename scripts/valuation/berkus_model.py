import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

def calculate_berkus(scores: dict) -> float:
    valuation = sum(scores.values())
    return valuation

# Example Test Run.
if __name__ == '__main__':
    # Assign a dollar value (up to $500k) for each of the five factors.
    berkus_scores = {
        'sound_idea': 400000,
        'prototype': 300000,
        'management_team': 500000,
        'strategic_relationships': 250000,
        'product_rollout': 150000
    }

    total_valuation = calculate_berkus(berkus_scores)
    
    print("--- Berkus Method Valuation Test ---")
    print(f"Calculated Valuation: ${total_valuation:,.0f}")