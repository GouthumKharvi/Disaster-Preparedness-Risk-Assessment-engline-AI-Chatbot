# src/primitive_functions/create_workflow.py
from datetime import datetime

# Import the templates
from .risk_templates import preparedness_templates


def create_preparedness_workflow(location, policy, risks_found):
    """
    Build a structured disaster-preparedness workflow.
    - Always includes general preparedness steps
    - Adds risk-specific steps based on detected risks
    - Adds policy-specific advisory
    Returns a dictionary representing the complete plan.
    """

    plan_steps = []

    # 1. Add general preparedness steps
    plan_steps.extend(preparedness_templates.get("General", []))

    # 2. Add risk-specific steps
    if not risks_found:
        plan_steps.append(
            "No immediate weather-based risks detected. Maintain general preparedness."
        )
    else:
        for risk_key, info in risks_found.items():
            label = info.get("label", risk_key)
            metric = info.get("metric", "N/A")

            # Section header for the risk
            plan_steps.append(f"--- {label} (metric observed: {metric}) ---")

            # Add steps associated with the risk label
            plan_steps.extend(
                preparedness_templates.get(label, ["No specific steps available."])
            )

    # 3. Add policy-specific advisory
    plan_steps.append(
        f"Policy Note: Your current policy is '{policy}'. "
        f"Ensure it covers damages for the detected risks (if any). "
        f"Keep insurer contact information accessible."
    )

    # 4. Build the final workflow object
    workflow = {
        "location": location,
        "policy": policy,
        "plan": plan_steps,
        "generated_at": datetime.utcnow().isoformat(),
    }

    return workflow
