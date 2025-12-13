# primitive_functions/ compare.py

"""
Compares weather data returned from Open-Meteo API
against predefined risk thresholds (flood, storm, heatwave).
Returns a structured dictionary with detected risks and metrics.
"""

from src.primitive_functions.risk_mapping import risk_mapping


def compare_weather_to_thresholds(daily_data):
    """
    Compare daily_data (dict returned from Open-Meteo 'daily') to thresholds in risk_mapping.
    Returns a dict of found risks and basic computed metrics.
    """

    risks_found = {}

    # Extract daily series safely
    precip = daily_data.get("precipitation_sum", []) or []
    temp_max = daily_data.get("temperature_2m_max", []) or []
    wind_max = daily_data.get("windspeed_10m_max", []) or []

    # Compute max values across the next 3 days
    max_precip = max(precip) if precip else 0
    max_temp = max(temp_max) if temp_max else None
    max_wind = max(wind_max) if wind_max else None

    ### --- Compare with thresholds --- ###

    # Flood Risk → precipitation ≥ threshold
    flood_threshold = risk_mapping["flood"]["threshold"]["precipitation_sum_mm"]
    if max_precip >= flood_threshold:
        risks_found["flood"] = {
            "label": risk_mapping["flood"]["label"],
            "metric": max_precip
        }

    # Storm Risk → windspeed (km/h) converted to m/s
    # Open-Meteo returns windspeed in km/h, but your threshold is in m/s.
    # Convert: km/h → m/s by dividing by 3.6
    storm_threshold = risk_mapping["storm"]["threshold"]["wind_speed_ms"]
    wind_ms = max_wind / 3.6 if max_wind else 0

    if wind_ms >= storm_threshold:
        risks_found["storm"] = {
            "label": risk_mapping["storm"]["label"],
            "metric": round(wind_ms, 2)
        }

    # Heatwave Risk → temperature ≥ threshold
    heat_threshold = risk_mapping["heatwave"]["threshold"]["temperature_c"]
    if max_temp and max_temp >= heat_threshold:
        risks_found["heatwave"] = {
            "label": risk_mapping["heatwave"]["label"],
            "metric": max_temp
        }

    ### --- Return structured analysis --- ###
    return {
        "max_precip_mm": max_precip,
        "max_temp_c": max_temp,
        "max_wind_ms": round(wind_ms, 2) if max_wind else 0,
        "risks_found": risks_found
    }
