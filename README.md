# Disaster-Preparedness-Risk-Assessment-engline-AI-Chatbot
An intelligent chatbot that assesses real-time disaster risks and generates personalized emergency preparedness plans. The system integrates Groq LLM (Llama 3.3 70B) for natural conversational responses and Open-Meteo API for live weather data analysis.

Below is a **complete, professional `README.md` written in Markdown**, aligned with your **final assessment structure**, **use-case**, **complex + primitive functions**, and **what you actually implemented**.
You can **copy-paste this directly into `readme.md`** and upload to GitHub.

---

```markdown
# 🌪️ Disaster Preparedness Planner

An end-to-end **AI-driven Disaster Preparedness Planner** that assesses regional disaster risks using live weather data and user context, then generates a **personalized preparedness plan**.  
This project was developed as part of an **assessment for Assisto Technologies Inc**.

---

## 📌 Use Case

**Use Case Name:** Disaster Preparedness Planner  
**Customer Problem:** Customers are often unprepared for regional disaster risks (floods, storms, heatwaves, etc.).  
**Solution:**  
This system analyzes location-based weather risks, past incident history, and user vulnerability to generate a **custom preparedness workflow** that reduces losses and simplifies response during disasters.

---

## 🧠 System Overview

The project is built using **modular primitive functions** combined into **complex workflows**, following a clean and explainable architecture.

### Key Capabilities
- 🌍 Location-based risk assessment
- ☁️ Live weather data via **Open-Meteo API**
- 🧩 Rule-based risk classification
- 📊 Risk aggregation (Low / Medium / High)
- 📋 Personalized preparedness plan generation
- 💬 Interactive chatbot (Streamlit)
- 📁 Exportable JSON outputs

---

## 🏗️ Project Architecture

```

Assisto Technologies Inc/
│
├── app.py                           # Streamlit chatbot application
├── Disaster_Preparedness_Planner.ipynb
├── readme.md
├── requirements.txt
│
├── data/
│   ├── preparedness_templates.json
│   ├── risk_mapping.json
│   ├── sample_policy_coverage.json
│   └── sample_user_input.json
│
├── examples/
│   ├── preparedness_plan_output.json
│   └── risk_assessment_output.json
│
└── src/
├── risk_assessment_engine.py
├── preparedness_planner.py
└── primitive_functions/
├── extract_data.py
├── classify_text.py
├── call_api.py
├── compare.py
├── aggregate.py
├── guide_user.py
├── create_workflow.py
├── display_information.py
├── risk_mapping.py
├── risk_templates.py

````

---

## 🔗 APIs Used

### 🌦️ Open-Meteo Weather API
Used to fetch:
- Daily precipitation
- Maximum temperature
- Maximum wind speed

No API key required.

---

## ⚙️ Core Functional Design

### 🔹 Primitive Functions

| Function | Description |
|--------|------------|
| `extractData()` | Extracts age, location, history from user input |
| `classifyText()` | Converts user history into risk level (low/medium/high) |
| `callAPI()` | Fetches live weather data from Open-Meteo |
| `compare()` | Compares weather data against risk thresholds |
| `aggregate()` | Aggregates age, history, and weather scores |
| `guideUser()` | Collects missing user inputs |
| `createWorkflow()` | Builds preparedness plan |
| `displayInformation()` | Displays plan in readable format |

---

### 🔹 Complex Function: Risk Assessment Engine

The **Risk Assessment Engine** composes multiple primitive functions:

```text
extractData → classifyText → callAPI → compare → aggregate
````

#### Example Composition

```python
extractData(application, ['age', 'history', 'location'])
classifyText(history, ['low', 'medium', 'high'])
callAPI(weatherService, 'GET', {location})
compare(weatherRisk, 'threshold', '>')
aggregate([ageScore, historyScore, weatherScore], 'average')
```

---

## 📊 Risk Logic

### Risk Levels

| Score Range | Level  |
| ----------- | ------ |
| ≥ 0.7       | High   |
| 0.4 – 0.69  | Medium |
| < 0.4       | Low    |

### Supported Risks

* Flood
* Storm
* Heatwave
* Cyclone
* Landslide
* Power Outage
* Cold Wave

---

## 📋 Preparedness Plan Generation

Plans are generated based on:

* Detected risks
* Risk severity (Low / Medium / High)
* Policy coverage
* Regional relevance

Each risk contains **7–10 real-world actionable steps**, aligned with disaster management practices.

---

## 🧪 Example Output

### Risk Summary

```json
{
  "score": 0.82,
  "level": "High",
  "history_score": 0.9,
  "weather_score": 0.75
}
```

### Preparedness Plan

```text
--- Flood Risk ---
Move valuables to higher floors.
Avoid flooded roads.
Prepare evacuation kit.

--- Storm Risk ---
Secure outdoor furniture.
Stay indoors during alerts.

Policy Note:
Review flood and storm damage coverage.
```

---

## 🖥️ Running the Application

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run Streamlit App

```bash
streamlit run app.py
```

### 3️⃣ Open Browser

```
http://localhost:8501
```

---

## 📁 Exported Outputs

* `preparedness_plan_output.json`
* `risk_assessment_output.json`

These can be used for:

* Audits
* Reports
* Insurance workflows
* Future integrations

---

## 🧠 Design Highlights

* Modular & testable architecture
* Clear separation of primitive vs complex logic
* Explainable risk scoring
* API-driven but deterministic (no black box ML)
* Ready for LLM integration (Groq / OpenAI)

---

## 🚀 Future Enhancements

* Real-time alert subscriptions
* Insurance claim recommendations
* Multilingual support
* Mobile app integration
* ML-based risk prediction

---

## 👤 Author

**Gouthum Kharvi**
Data Scientist | AI & ML Practitioner
Assessment Submission – **Assisto Technologies Inc**

---

---

```

