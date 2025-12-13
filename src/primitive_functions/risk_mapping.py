# src/primitive_functions/risk_mapping.py

risk_mapping = {
    "flood": {
        "threshold": {"precipitation_sum_mm": 50},
        "label": "Flood Risk"
    },
    "storm": {
        "threshold": {"wind_speed_ms": 15},
        "label": "Storm Risk"
    },
    "heatwave": {
        "threshold": {"temperature_c": 40},
        "label": "Heatwave Risk"
    },
    "landslide": {
        "threshold": {"precipitation_sum_mm": 80},
        "label": "Landslide Risk"
    },
    "lightning": {
        "threshold": {"wind_speed_ms": 20},
        "label": "Lightning & Thunderstorm Risk"
    },
    "coldwave": {
        "threshold": {"temperature_c_min": 5},
        "label": "Cold Wave Risk"
    }
}
