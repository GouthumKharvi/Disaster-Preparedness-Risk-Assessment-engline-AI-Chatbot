# src/primitive_functions/create_workflow.py
from datetime import datetime
from .risk_templates import preparedness_templates

# Map risk keys to template names
RISK_LABEL_MAP = {
    "flood": "Flood Risk",
    "storm": "Storm Risk",
    "heatwave": "Heatwave Risk",
    "coldwave": "Cold Wave Risk",
    "winter_storm": "Winter Storm Risk",
    "cyclone": "Cyclone Risk",
    "hurricane": "Hurricane Risk",
    "tornado": "Tornado Risk",
    "hailstorm": "Hailstorm Risk",
    "drought": "Drought Risk",
    "landslide": "Landslide Risk",
    "tsunami": "Tsunami Risk",
    "pandemic": "Pandemic Risk",
    "volcanic_eruption": "Volcanic Eruption Risk"
}

def create_preparedness_workflow(location, policy, risks_found):
    plan_steps = []

    # 1️⃣ General preparedness (always)
    plan_steps.extend(preparedness_templates.get("General", []))

    # 2️⃣ Risk-specific preparedness
    if risks_found:
        for risk_key, info in risks_found.items():
            label = RISK_LABEL_MAP.get(risk_key)

            if not label:
                continue  # unknown risk, skip safely

            # Section header
            plan_steps.append(
                f"--- {label} (Level: {info.get('level')}, Metric: {info.get('metric')}) ---"
            )

            # Add precautions
            plan_steps.extend(
                preparedness_templates.get(label, ["No specific steps available."])
            )
    else:
        plan_steps.append(
            "No immediate high-risk weather threats detected. Continue general preparedness."
        )

    # 3️⃣ Policy advisory
    plan_steps.append(
        f"Policy Note: Your current policy is '{policy}'. "
        f"Ensure it covers damages related to the detected risks. "
        f"Keep insurer contact details accessible."
    )

    return {
        "location": location,
        "policy": policy,
        "plan": plan_steps,
        "generated_at": datetime.utcnow().isoformat()
    } 
