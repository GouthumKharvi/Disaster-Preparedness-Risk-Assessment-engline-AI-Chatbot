# src/primitive_functions/call_api.py

import requests
from datetime import datetime, timedelta

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"


def geocode_city(city_name: str):
    """
    Convert a city name into (latitude, longitude) using the free Nominatim API.
    No API key required.
    """
    params = {"q": city_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "DisasterPreparednessPlanner/1.0"}

    response = requests.get(GEOCODE_URL, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    results = response.json()
    if not results:
        raise ValueError(f"Could not geocode location: {city_name}")

    lat = float(results[0]["lat"])
    lon = float(results[0]["lon"])
    return lat, lon


def call_api_weather(lat: float, lon: float, days: int = 3):
    """
    Fetch daily weather forecast (temperature, rainfall, windspeed)
    from Open-Meteo API.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
        "timezone": "auto",
        "start_date": datetime.utcnow().date().isoformat(),
        "end_date": (datetime.utcnow().date() + timedelta(days=days - 1)).isoformat()
    }

    response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    response.raise_for_status()

    return response.json().get("daily", {})
