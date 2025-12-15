# primitive_functions/preparedness_planner.py
"""
preparedness_planner.py

This module composes the Disaster Preparedness Planner:
- Guides user interaction (optional)
- Calls the Risk Assessment Engine
- Builds a preparedness workflow
- Displays the plan
"""

from src.primitive_functions.guide_user import guide_user_interaction
from src.primitive_functions.create_workflow import create_preparedness_workflow
from src.primitive_functions.display_information import display_plan
from src.risk_assessment_engine import risk_assessment_engine


def disaster_preparedness_planner(user_input=None, simulate_interaction_inputs=None):
    """
    Full composed function:
    1. Guide user (collect missing inputs)
    2. Run risk_assessment_engine()
    3. Build preparedness workflow
    4. Display the final plan

    Args:
        user_input (dict): Direct dictionary with keys:
            - location
            - policy
            - history
        simulate_interaction_inputs (dict): (Optional) fake user inputs for testing

    Returns:
        dict: Final plan object with risk summary, workflow steps, and metadata.
    """

    # Step 1 — Guide user or use provided input
    if simulate_interaction_inputs:
        user_data = guide_user_interaction(simulate_interaction_inputs)
    else:
        if not user_input:
            raise ValueError("user_input must be provided when simulate_interaction_inputs is not used.")
        user_data = user_input

    # Step 2 — Run complex function: Risk Assessment Engine
    risk_result = risk_assessment_engine(user_data)

    # Step 3 — Build workflow plan
    risks_found = risk_result["weather_analysis"].get("risks_found", {})
    plan_obj = create_preparedness_workflow(
        location=risk_result["location"],
        policy=risk_result["policy"],
        risks_found=risks_found
    )

    # Add more data to final output
    plan_obj["risk_summary"] = risk_result["aggregate"]
    plan_obj["weather_analysis"] = risk_result["weather_analysis"]

    # Step 4 — Display plan
    display_plan(plan_obj)

    return plan_obj


# Optional main execution (manual test)
if __name__ == "__main__":
    test_input = {
        "location": "Udupi",
        "policy": "Standard Home Insurance",
        "history": "Strong winds and storm last month"
    }

    final_plan = disaster_preparedness_planner(test_input)
