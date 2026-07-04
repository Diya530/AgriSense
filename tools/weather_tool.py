"""
Weather Tool – AgriSense AI
────────────────────────────
Placeholder for live weather data retrieval.
Replace the stub logic with a real OpenWeatherMap / IMD API call.

Future integration:
  - Real-time temperature, humidity, rainfall, wind speed
  - 7-day forecast
  - Agro-meteorological advisories
"""

import os

# Optional: import requests and use OPENWEATHER_API_KEY from env for live data


def get_weather_data(location: str, unit: str = "metric") -> dict:
    """
    Retrieve current weather data for a given location.

    Args:
        location (str): City name or district (e.g., "Nashik", "Ludhiana")
        unit (str): "metric" (°C) or "imperial" (°F)

    Returns:
        dict: Weather information including temperature, humidity, rainfall,
              wind speed, and farming advisory.

    TODO: Replace stub with real API call:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {"q": location, "appid": os.getenv("OPENWEATHER_API_KEY"), "units": unit}
        response = requests.get(url, params=params)
        return response.json()
    """
    # ── STUB DATA ─────────────────────────────────────────────────
    return {
        "location": location,
        "temperature": 28,
        "feels_like": 31,
        "humidity": 72,
        "rainfall_mm": 5.2,
        "wind_speed_kmh": 14,
        "condition": "Partly Cloudy",
        "condition_icon": "🌤️",
        "uv_index": 6,
        "forecast_7day": [
            {"day": "Mon", "high": 30, "low": 22, "condition": "Sunny", "rain_chance": 10},
            {"day": "Tue", "high": 28, "low": 21, "condition": "Cloudy", "rain_chance": 40},
            {"day": "Wed", "high": 25, "low": 19, "condition": "Rainy", "rain_chance": 80},
            {"day": "Thu", "high": 27, "low": 20, "condition": "Partly Cloudy", "rain_chance": 30},
            {"day": "Fri", "high": 29, "low": 21, "condition": "Sunny", "rain_chance": 5},
            {"day": "Sat", "high": 31, "low": 23, "condition": "Sunny", "rain_chance": 5},
            {"day": "Sun", "high": 30, "low": 22, "condition": "Cloudy", "rain_chance": 20},
        ],
        "farming_advisory": (
            "Moderate temperature and humidity are ideal for most Kharif crops. "
            "Rain expected mid-week — hold irrigation for 2 days."
        ),
        "source": "stub",  # change to "openweathermap" when live
    }
