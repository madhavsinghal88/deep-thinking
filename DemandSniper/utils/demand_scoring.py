from typing import Dict, Any
from config.loader import load_scoring_config


def calculate_demand_score(
    times_posted: int,
    days_open: int,
    number_of_openings: int
) -> float:
    """
    Calculate demand score based on configurable formula.
    
    Default formula: (times_posted * 2) + (days_open / 10) + (number_of_openings * 3)
    """
    config = load_scoring_config()
    formula = config.get("demand_score_formula", {})
    
    times_posted_weight = formula.get("times_posted_weight", 2)
    days_open_divisor = formula.get("days_open_divisor", 10)
    openings_weight = formula.get("openings_weight", 3)
    
    # Avoid division by zero
    if days_open_divisor == 0:
        days_open_divisor = 10
    
    score = (
        (times_posted * times_posted_weight) +
        (days_open / days_open_divisor) +
        (number_of_openings * openings_weight)
    )
    
    return round(score, 2)


def get_priority_tag(demand_score: float) -> str:
    """
    Assign priority tag based on demand score thresholds.
    
    Default:
    - > 25: High Priority
    - 10-25: Medium Priority
    - < 10: Low Priority
    """
    config = load_scoring_config()
    thresholds = config.get("priority_thresholds", {})
    
    high_threshold = thresholds.get("high", 25)
    medium_threshold = thresholds.get("medium", 10)
    
    if demand_score >= high_threshold:
        return "High"
    elif demand_score >= medium_threshold:
        return "Medium"
    else:
        return "Low"


def get_demand_score_breakdown(
    times_posted: int,
    days_open: int,
    number_of_openings: int
) -> Dict[str, Any]:
    """Get detailed breakdown of demand score calculation."""
    config = load_scoring_config()
    formula = config.get("demand_score_formula", {})
    
    times_posted_weight = formula.get("times_posted_weight", 2)
    days_open_divisor = formula.get("days_open_divisor", 10)
    openings_weight = formula.get("openings_weight", 3)
    
    times_posted_contribution = times_posted * times_posted_weight
    days_open_contribution = days_open / days_open_divisor
    openings_contribution = number_of_openings * openings_weight
    total_score = times_posted_contribution + days_open_contribution + openings_contribution
    
    return {
        "total_score": round(total_score, 2),
        "priority": get_priority_tag(total_score),
        "components": {
            "times_posted": {
                "value": times_posted,
                "weight": times_posted_weight,
                "contribution": round(times_posted_contribution, 2)
            },
            "days_open": {
                "value": days_open,
                "divisor": days_open_divisor,
                "contribution": round(days_open_contribution, 2)
            },
            "number_of_openings": {
                "value": number_of_openings,
                "weight": openings_weight,
                "contribution": round(openings_contribution, 2)
            }
        }
    }
