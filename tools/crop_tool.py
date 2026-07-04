"""
Crop Recommendation Tool – AgriSense AI
─────────────────────────────────────────
Placeholder for AI/ML-based crop recommendation engine.

Future integration:
  - Connect to a trained ML model (Random Forest / SVM) using soil + weather data
  - ICAR crop suitability database
  - Season-based recommendation with expected yield estimates
"""


def get_crop_recommendation(
    soil_type: str,
    season: str,
    state: str,
    rainfall_mm: float = 500,
    temperature_c: float = 28,
    ph: float = 6.5,
) -> dict:
    """
    Recommend suitable crops based on soil, season, location, and climate.

    Args:
        soil_type (str): e.g., "black", "alluvial", "red", "laterite"
        season (str): "kharif", "rabi", or "zaid"
        state (str): Indian state name
        rainfall_mm (float): Annual rainfall in mm
        temperature_c (float): Average temperature in °C
        ph (float): Soil pH value

    Returns:
        dict: Top crop recommendations with suitability scores and tips.

    TODO: Replace stub with real ML model inference or API call.
    """
    # ── STUB DATA ─────────────────────────────────────────────────
    recommendations = {
        ("black", "kharif"): [
            {"crop": "Cotton", "suitability": 95, "expected_yield": "15–20 quintals/acre", "water_need": "Medium"},
            {"crop": "Soybean", "suitability": 88, "expected_yield": "8–12 quintals/acre", "water_need": "Low"},
            {"crop": "Sorghum (Jowar)", "suitability": 82, "expected_yield": "12–15 quintals/acre", "water_need": "Low"},
        ],
        ("alluvial", "rabi"): [
            {"crop": "Wheat", "suitability": 96, "expected_yield": "18–22 quintals/acre", "water_need": "Medium"},
            {"crop": "Mustard", "suitability": 90, "expected_yield": "6–9 quintals/acre", "water_need": "Low"},
            {"crop": "Chickpea (Chana)", "suitability": 85, "expected_yield": "7–10 quintals/acre", "water_need": "Low"},
        ],
        ("red", "kharif"): [
            {"crop": "Groundnut", "suitability": 92, "expected_yield": "10–14 quintals/acre", "water_need": "Low"},
            {"crop": "Pearl Millet (Bajra)", "suitability": 88, "expected_yield": "10–13 quintals/acre", "water_need": "Low"},
            {"crop": "Maize", "suitability": 80, "expected_yield": "14–18 quintals/acre", "water_need": "Medium"},
        ],
    }

    key = (soil_type.lower(), season.lower())
    crops = recommendations.get(
        key,
        [
            {"crop": "Rice", "suitability": 78, "expected_yield": "16–20 quintals/acre", "water_need": "High"},
            {"crop": "Maize", "suitability": 75, "expected_yield": "14–18 quintals/acre", "water_need": "Medium"},
            {"crop": "Vegetables (Mixed)", "suitability": 72, "expected_yield": "Varies", "water_need": "Medium"},
        ],
    )

    return {
        "input": {"soil_type": soil_type, "season": season, "state": state, "ph": ph},
        "recommendations": crops,
        "top_pick": crops[0]["crop"] if crops else "Rice",
        "advisory": f"Based on {soil_type} soil in {state} during {season} season.",
        "source": "stub",
    }
