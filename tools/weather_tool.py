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
import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_data(location: str):

    current_url = "https://api.openweathermap.org/data/2.5/weather"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }

    current = requests.get(current_url, params=params).json()
    forecast = requests.get(forecast_url, params=params).json()

    if current.get("cod") != 200:
        return {
            "location": location,
            "temperature": "--",
            "feels_like": "--",
            "humidity": "--",
            "rainfall_mm": 0,
            "wind_speed_kmh": 0,
            "condition": "Unavailable",
            "condition_icon": "❓",
            "uv_index": "N/A",
            "forecast_7day": [],
            "farming_advisory": "Unable to fetch weather.",
            "source": "openweather"
        }

    weather = current["weather"][0]
    main = current["main"]
    wind = current["wind"]

    # Pick one forecast around noon for each day
    forecast_days = []

    added = set()

    if forecast.get("cod") == "200":

        for item in forecast["list"]:

            date = item["dt_txt"].split()[0]

            if date in added:
                continue

            added.add(date)

            forecast_days.append({
                "day": date[5:],          # MM-DD
                "high": round(item["main"]["temp_max"]),
                "low": round(item["main"]["temp_min"]),
                "condition": item["weather"][0]["main"],
                "rain_chance": int(item["pop"] * 100)
            })

            if len(forecast_days) == 5:
                break

    advisory = "Weather conditions are suitable for normal farming operations."

    if weather["main"] == "Rain":
        advisory = "Rain expected. Avoid irrigation and protect harvested crops."

    elif main["temp"] > 35:
        advisory = "High temperature detected. Irrigate crops during early morning or evening."

    elif main["humidity"] > 85:
        advisory = "High humidity may increase fungal disease risk."

    return {

        "location": current["name"],

        "temperature": round(main["temp"]),

        "feels_like": round(main["feels_like"]),

        "humidity": main["humidity"],

        "rainfall_mm": current.get("rain", {}).get("1h", 0),

        "wind_speed_kmh": round(wind["speed"] * 3.6, 1),

        "condition": weather["main"],

        "condition_icon": {
            "Clear":"☀️",
            "Clouds":"☁️",
            "Rain":"🌧️",
            "Thunderstorm":"⛈️",
            "Drizzle":"🌦️",
            "Mist":"🌫️"
        }.get(weather["main"],"🌤️"),

        "uv_index":"N/A",

        "forecast_7day":forecast_days,

        "farming_advisory":advisory,

        "source":"OpenWeather"
    }

def get_weather_by_coordinates(lat, lon):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params).json()

    # Use the same formatting logic as get_weather_data()
    # (You can refactor it later to avoid duplication.)

    return {
        "location": response["name"],
        "temperature": round(response["main"]["temp"]),
        "feels_like": round(response["main"]["feels_like"]),
        "humidity": response["main"]["humidity"],
        "rainfall_mm": response.get("rain", {}).get("1h", 0),
        "wind_speed_kmh": round(response["wind"]["speed"] * 3.6, 1),
        "condition": response["weather"][0]["main"],
        "condition_icon": "🌤️",
        "uv_index": "N/A",
        "forecast_7day": [],
        "farming_advisory": "Live weather based on your location.",
        "source": "OpenWeather"
    }