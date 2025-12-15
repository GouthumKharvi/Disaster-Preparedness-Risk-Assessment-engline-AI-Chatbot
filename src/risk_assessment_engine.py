# primitive_functions/risk_assessment_engine.py
"""
risk_assessment_engine.py

Implements the Complex Function: Risk Assessment Engine
(From Sheet-2 of the Assessment)

This function composes primitive functions:
1. extractData
2. classifyText
3. callAPI (weather)
4. compare thresholds
5. aggregate scores
"""

from src.primitive_functions.extract_data import extract_data
from src.primitive_functions.classify_text import classify_text
from src.primitive_functions.call_api import call_api_weather
from src.primitive_functions.compare import compare_weather_to_thresholds
from src.primitive_functions.aggregate import aggregate_scores
from src.primitive_functions.guide_user import guide_user_interaction


def risk_assessment_engine(user_input, geocode_if_needed=True):
    """
    Risk Assessment Engine:
    -------------------------------------
    Input:
        user_input = {
            "location": "Udupi",
            "policy": "Standard Home Insurance",
            "history": "My house flooded last year"
        }

    Steps:
        1) extractData
        2) classifyText
        3) callAPI() - weather forecast
        4) compare() - threshold-based risk detection
        5) aggregate() - combine history + weather risk into final score

    Output:
        {
            "location": "Udupi",
            "lat": <float>,
            "lon": <float>,
            "history_risk": "high",
            "weather_analysis": {...},
            "aggregate": {...},
            "policy": "Standard Home Insurance"
        }
    """

    # -----------------------------------------------------------
    # 1. extractData
    # -----------------------------------------------------------
    data = extract_data(user_input, ["location", "policy", "history"])
    location = data["location"]
    policy = data["policy"]
    history = data["history"]

    # -----------------------------------------------------------
    # 2. Convert location -> lat/lon
    # -----------------------------------------------------------
    from primitive_functions.call_api import geocode_city

    if isinstance(location, str) and "," not in location and geocode_if_needed:
        lat, lon = geocode_city(location)
    else:
        if isinstance(location, str) and "," in location:
            lat, lon = map(float, location.split(","))
        elif isinstance(location, (list, tuple)) and len(location) == 2:
            lat, lon = location
        else:
            raise ValueError("Location must be a city name or 'lat,lon' format")

    # -----------------------------------------------------------
    # 3. callAPI - Fetch weather forecast (3 days)
    # -----------------------------------------------------------
    daily_weather = call_api_weather(lat, lon, days=3)

    # -----------------------------------------------------------
    # 4. compare() - Identify weather-based risks
    # -----------------------------------------------------------
    weather_analysis = compare_weather_to_thresholds(daily_weather)

    # -----------------------------------------------------------
    # 5. classifyText() - Convert user history into risk label
    # -----------------------------------------------------------
    history_risk = classify_text(history)

    # -----------------------------------------------------------
    # 6. aggregate() - Combine history + weather risk
    # -----------------------------------------------------------
    aggregate_result = aggregate_scores(history_risk, weather_analysis)

    # -----------------------------------------------------------
    # Final structured output
    # -----------------------------------------------------------
    result = {
        "location": location,
        "lat": lat,
        "lon": lon,
        "history_risk": history_risk,
        "weather_analysis": weather_analysis,
        "aggregate": aggregate_result,
        "policy": policy
    }

    return result



# -------------------------------------------------------------------
# Optional helper to run interactively or simulate user input
# -------------------------------------------------------------------
def run_risk_engine_interactive(simulated_input=None):
    """
    Wrapper that uses user-guided input or simulated test input.
    """
    if simulated_input:
        user_data = guide_user_interaction(simulated_input)
    else:
        user_data = guide_user_interaction()

    return risk_assessment_engine(user_data)
