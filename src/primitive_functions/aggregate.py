#  primitive_functions/aggregate.py

def aggregate_scores(history_risk, weather_analysis):
    """
    Aggregate simple numeric scores:
    - history_risk: 'low' -> 0.1, 'medium' -> 0.5, 'high' -> 0.9
    - weather_analysis: dict that contains 'risks_found'
      For each detected risk, apply a weight.
    
    Returns:
      {
        "score": float,
        "level": "Low/Medium/High",
        "history_score": float,
        "weather_score": float
      }
    """

    # Mapping textual history to numeric risk score
    history_mapping = {
        "low": 0.1,
        "medium": 0.5,
        "high": 0.9
    }

    hist_score = history_mapping.get(history_risk, 0.1)

    # Compute weather-based score from risks_found
    weather_score = 0.0
    risks_found = weather_analysis.get("risks_found", {})

    for risk in risks_found:
        if risk == "flood":
            weather_score += 0.6
        elif risk == "storm":
            weather_score += 0.4
        elif risk == "heatwave":
            weather_score += 0.3
        elif risk == "landslide":
            weather_score += 0.7
        elif risk == "lightning":
            weather_score += 0.4
        elif risk == "coldwave":
            weather_score += 0.5

    # Cap weather risk to max of 1.0
    weather_score = min(weather_score, 1.0)

    # Combine both with simple averaging
    combined = (hist_score + weather_score) / 2.0

    # Normalize between 0 and 1
    combined = max(0.0, min(1.0, combined))

    # Convert numerical score to level
    if combined >= 0.7:
        level = "High"
    elif combined >= 0.4:
        level = "Medium"
    else:
        level = "Low"

    return {
        "score": round(combined, 2),
        "level": level,
        "history_score": hist_score,
        "weather_score": weather_score
    }
 
