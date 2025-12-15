# src/primitive_functions/risk_mapping.py

risk_mapping = {
    "flood": {
        "threshold": {"precipitation_sum_mm": 50},
        "label": "Flood Risk"
    },
    "storm": {
        "threshold": {"wind_speed_ms": 15},
        "label": "Storm / Cyclone Risk"
    },
    "heatwave": {
        "threshold": {"temperature_c": 40},
        "label": "Heatwave Risk"
    },
    "cold_wave": {
        "threshold": {"temperature_c_min": 5},
        "label": "Cold Wave Risk"
    },
    "hailstorm": {
        "threshold": {"wind_speed_ms": 20},
        "label": "Hailstorm Risk"
    },
    "drought": {
        "threshold": {"precipitation_sum_mm": 10},
        "label": "Drought Risk"
    },
    "cyclone": {
        "threshold": {"wind_speed_ms": 25},
        "label": "Cyclone Risk"
    },
    "tsunami": {
        "threshold": {},
        "label": "Tsunami Risk"
    },
    "pandemic": {
        "threshold": {},
        "label": "Pandemic Risk"
    },
    "volcanic_eruption": {
        "threshold": {},
        "label": "Volcanic Eruption Risk"
    },
    "tornado": {
        "threshold": {"wind_speed_ms": 30},
        "label": "Tornado Risk"
    }
}
