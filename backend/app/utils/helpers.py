import uuid
import os
from typing import List, Union


def health_category(score: float) -> str:
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Moderate"
    elif score >= 20:
        return "Poor"
    else:
        return "Critical"


def generate_report_id() -> str:
    return f"RPT-{uuid.uuid4().hex[:8].upper()}"


def validate_csv(file_path: str) -> bool:
    if not os.path.exists(file_path):
        return False
    if not file_path.lower().endswith(".csv"):
        return False
    return True


def parse_forecast_years(preset: str, custom_years: Union[List[int], None] = None) -> List[int]:
    import datetime
    current_year = datetime.datetime.now().year

    if preset == "5":
        return list(range(current_year + 1, current_year + 6))
    elif preset == "10":
        return list(range(current_year + 1, current_year + 11))
    elif preset == "20":
        return list(range(current_year + 1, current_year + 21))
    elif preset == "50":
        return list(range(current_year + 1, current_year + 51))
    elif preset == "custom":
        if not custom_years:
            raise ValueError("custom_years must be provided when preset is 'custom'")
        return sorted(custom_years)
    else:
        raise ValueError(f"Unknown preset: {preset}. Use '5', '10', '20', '50', or 'custom'")
