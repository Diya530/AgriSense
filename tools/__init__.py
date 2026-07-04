# AgriSense AI – Tool registry
# Import all placeholder tools here for easy registration
from .weather_tool import get_weather_data
from .crop_tool import get_crop_recommendation
from .market_tool import get_market_prices
from .scheme_tool import get_government_schemes
from .soil_tool import get_soil_information
from .pest_tool import get_pest_management

__all__ = [
    "get_weather_data",
    "get_crop_recommendation",
    "get_market_prices",
    "get_government_schemes",
    "get_soil_information",
    "get_pest_management",
]
