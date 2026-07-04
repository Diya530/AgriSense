"""
Soil Information Tool – AgriSense AI
──────────────────────────────────────
Placeholder for soil health database integration.

Future integration:
  - ICAR Soil Health Card API
  - NBSS&LUP (National Bureau of Soil Survey & Land Use Planning) database
  - Real-time soil moisture sensor data (IoT integration)
"""


def get_soil_information(location: str = None, soil_type: str = None) -> dict:
    """
    Retrieve soil health information and recommendations.

    Args:
        location (str, optional): District/state for regional soil data
        soil_type (str, optional): Type of soil to query

    Returns:
        dict: Soil properties, nutrient levels, and amendment recommendations.

    TODO: Replace stub with real soil health database query.
    """
    soil_profiles = {
        "black": {
            "type": "Black Cotton Soil (Regur)",
            "regions": "Maharashtra, Gujarat, MP, Karnataka, AP",
            "ph_range": "7.5–8.5",
            "texture": "Clay (fine-grained)",
            "water_retention": "Very High",
            "organic_matter": "Low to Medium",
            "nitrogen": "Low",
            "phosphorus": "Medium",
            "potassium": "High",
            "suitable_crops": ["Cotton", "Soybean", "Sorghum", "Wheat", "Sunflower"],
            "deficiencies": ["Nitrogen", "Zinc", "Boron"],
            "amendment": "Add organic manure, zinc sulfate; avoid waterlogging",
        },
        "alluvial": {
            "type": "Alluvial Soil",
            "regions": "Indo-Gangetic Plains (UP, Bihar, Punjab, Haryana, WB)",
            "ph_range": "6.5–7.5",
            "texture": "Sandy loam to clay loam",
            "water_retention": "Medium to High",
            "organic_matter": "Medium",
            "nitrogen": "Medium",
            "phosphorus": "Medium",
            "potassium": "High",
            "suitable_crops": ["Wheat", "Rice", "Sugarcane", "Maize", "Vegetables"],
            "deficiencies": ["Zinc", "Sulfur", "Iron (in alkaline patches)"],
            "amendment": "Balanced NPK; zinc sulfate; green manure",
        },
        "red": {
            "type": "Red and Yellow Soil",
            "regions": "Deccan Plateau, Eastern Ghats, Odisha, Jharkhand",
            "ph_range": "5.5–7.0",
            "texture": "Sandy loam",
            "water_retention": "Low to Medium",
            "organic_matter": "Low",
            "nitrogen": "Low",
            "phosphorus": "Low",
            "potassium": "Low to Medium",
            "suitable_crops": ["Groundnut", "Millets", "Pulses", "Cotton", "Tobacco"],
            "deficiencies": ["Nitrogen", "Phosphorus", "Zinc", "Boron"],
            "amendment": "Add organic matter, lime if acidic; use phosphatic fertilizers",
        },
    }

    key = (soil_type or "alluvial").lower()
    profile = soil_profiles.get(key, soil_profiles["alluvial"])

    return {
        "location": location or "General",
        "soil_profile": profile,
        "health_score": 72,  # out of 100
        "recommendations": [
            f"Apply 2–3 tonnes FYM/compost per acre before sowing.",
            f"Use soil test report to fine-tune NPK doses.",
            f"Address deficiencies: {', '.join(profile['deficiencies'])}.",
        ],
        "source": "stub",
    }
