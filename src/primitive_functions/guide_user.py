#primitive_functions/ guide_user.py
"""
Primitive Function: guideUser()

This function guides the user through providing necessary inputs.
It supports two modes:
1. Interactive mode (asks questions using input())
2. Simulated mode (useful for notebooks/testing)
"""

def guide_user_interaction(simulated_inputs=None):
    """
    Guide user or use simulated inputs.
    Returns a dict with keys:
    - location
    - policy
    - history
    """
    # === Simulated Mode (for notebook/testing) ===
    if simulated_inputs:
        return {
            "location": simulated_inputs.get("location"),
            "policy": simulated_inputs.get("policy"),
            "history": simulated_inputs.get("history")
        }

    # === Interactive Mode ===
    print("Let's collect some information to generate your preparedness plan.\n")

    location = input("Enter your city or coordinates (city name or 'lat,lon'): ").strip()
    policy = input("Which insurance policy do you have? (e.g., 'Standard Home Insurance'): ").strip()
    history = input("Any recent disaster-related incidents or history? (optional): ").strip()

    return {
        "location": location,
        "policy": policy,
        "history": history
    }
