# 🗣️ Example Conversation: Disaster Preparedness Planner

This example demonstrates how a user interacts with the Disaster Preparedness Planner system.  
It includes:

- User inputs  
- System guiding questions  
- LLM-generated preparedness advisory  
- Final risk summary  

---

## **1. User Starts Interaction**

**User:**  
Hi, I want to check disaster preparedness for my home.

**System:**  
Sure! I can help you generate a personalized disaster-preparedness plan.  
To begin, may I know your **location**?

---

## **2. User Provides Required Inputs**

**User:**  
Udupi

**System:**  
Thank you. Do you have any **recent incident history** related to weather (e.g., floods, storms, evacuation)?

**User:**  
Yes, there were strong winds last month, but no damage.

**System:**  
Noted. Lastly, what is your **policy coverage type**?

**User:**  
Standard Home Insurance.

---

## **3. System Performs Risk Assessment (Using API + Functions)**

The system now executes:

- `extract_data()`  
- `geocode_city()`  
- `call_api_weather()`  
- `compare_weather_to_thresholds()`  
- `classify_text()`  
- `aggregate_scores()`  
- `risk_assessment_engine()`  

---

### **Extracted Weather Summary (Example)**

```json
{
  "max_precip_mm": 0.0,
  "max_temp_c": 30.4,
  "max_wind_ms": 21.9,
  "risks_found": {
    "storm": {
      "label": "Storm Risk",
      "metric": 21.9
    }
  }
}

---

## **4. LLM Generates Human-Friendly Preparedness Advisory**

Below is an example output from the LLM (`llm_generate_plan()`):

### **Preparedness Advisory (Example)**

> Based on the current weather outlook and your recent incident history, there is a **moderate storm risk** in your area.  
> Winds up to **21.9 m/s** are expected, though no rainfall is predicted.  
> Your overall disaster risk score is **0.45 (Medium)**.
>
> To stay prepared:
> - Keep essential documents safely stored in waterproof protection.
> - Secure outdoor furniture and loose objects around your home.
> - Charge your devices (phones, power banks) in case of power fluctuations.
> - Stay updated with local alerts and avoid unnecessary travel during strong winds.
>  
> Your policy **Standard Home Insurance** covers storm damage, so ensure you have your insurer’s emergency contact available.

---

## **5. Final Generated Preparedness Plan (Structured Output)**

The system produces a structured plan object like this:

```json
{
  "location": "Udupi",
  "policy": "Standard Home Insurance",
  "generated_at": "2025-12-10T12:45:23Z",
  "plan": [
    "Keep important documents in waterproof bags.",
    "Maintain a small emergency medical kit.",
    "Know the nearest shelter and evacuation route.",
    "--- Storm Risk (metric: 21.9) ---",
    "Secure outdoor furniture.",
    "Charge your devices and power banks.",
    "Stay indoors and avoid travel during storm warnings.",
    "Policy note: Your recorded policy is 'Standard Home Insurance'. Check policy coverages for relevant damages (flood/storm) and save insurer contact."
  ],
  "risk_summary": {
    "score": 0.45,
    "level": "Medium",
    "history_score": 0.5,
    "weather_score": 0.4
  },
  "weather_analysis": {
    "max_precip_mm": 0.0,
    "max_temp_c": 30.4,
    "max_wind_ms": 21.9,
    "risks_found": {
      "storm": {
        "label": "Storm Risk",
        "metric": 21.9
      }
    }
  }
}
```

---

## **6. End of Example Conversation**

**System:**  
Your personalized preparedness plan has been generated. Review the steps carefully and stay safe.  
Would you like to download the plan as a JSON file or generate another for a different location?

---

# 🎉 This completes the full example conversation file.

