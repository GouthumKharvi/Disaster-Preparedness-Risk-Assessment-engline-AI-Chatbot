"""
============================================================================
DISASTER PREPAREDNESS CHATBOT - WITH INSURANCE ENGINE INTEGRATION
============================================================================

FIXES APPLIED:
✓ Risk calculation now shows HIGH/MEDIUM/LOW correctly
✓ Location extraction improved (no more "surance" bug)
✓ Better thresholds for risk detection
✓ More varied LLM responses
✓ Insurance recommendation engine integrated
✓ Fixed JSON loading and Streamlit config order
✓ MODERN UI with animations and perfect visibility

============================================================================
"""

import os
import sys
import json
import re
from datetime import datetime

# ⚠️ CRITICAL: Page config MUST be the absolute first Streamlit command
import streamlit as st

st.set_page_config(
    page_title="Disaster Preparedness AI Assistant",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup imports
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Import project modules
try:
    from src.risk_assessment_engine import risk_assessment_engine
    from src.preparedness_planner import create_preparedness_workflow
except Exception as e:
    st.error(f"Failed to import modules: {e}")
    st.stop()

# -------------------------------------------------------
# Insurance Engine Functions (Integrated)
# -------------------------------------------------------
def load_insurance_data():
    """
    Loads disaster insurance plans from JSON file (Cloud-safe).
    """
    try:
        # Get project root (where app.py is located)
        project_root = os.path.dirname(os.path.abspath(__file__))

        # Navigate to JSON folder inside project
        file_path = os.path.join(
            project_root,
            "JSON",
            "disaster_insurance.json"
        )

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().lstrip('\ufeff')
            data = json.loads(content)

        return data

    except FileNotFoundError:
        st.error("❌ disaster_insurance.json not found. Make sure it is inside the JSON folder in the repo.")
        return {}

    except json.JSONDecodeError as e:
        st.error(f"❌ JSON error at line {e.lineno}: {e.msg}")
        return {}

    except Exception as e:
        st.error(f"❌ Failed to load insurance data: {str(e)}")
        return {}


def get_insurance_plans(disaster_type, insurance_data):
    """
    Returns insurance plans based on disaster type.
    disaster_type example: "flood", "thunderstorm"
    """
    if not insurance_data or not disaster_type:
        return []

    disaster_type = disaster_type.lower()

    # 🔥 FIX: match top-level disaster keys
    if disaster_type in insurance_data:
        return insurance_data[disaster_type].get("insurance_plans", [])

    return []


def extract_disaster_from_text(text):
    text = text.lower()

    disaster_map = {
        "flood": ["flood", "flooding"],
        "thunderstorm": ["thunderstorm", "storm", "heavy rain", "lightning"],
        "cyclone": ["cyclone"],
        "heatwave": ["heatwave", "heat"],
        "cold wave": ["cold wave", "coldwave"],
        "winter storm": ["winter storm"],
        "hail": ["hail", "hailstorm"],
        "hurricane": ["hurricane"],
        "tornado": ["tornado"],
        "drought": ["drought"],
        "tsunami": ["tsunami"],
        "pandemic": ["pandemic"],
        "volcanic": ["volcanic", "volcano"]
    }

    for disaster, keywords in disaster_map.items():
        for k in keywords:
            if k in text:
                return disaster

    return None



def recommend_insurance_plan(disaster_type, insurance_data):
    """
    Recommends insurance plans based on detected disaster risks.
    
    Args:
        disaster_type: Can be string like "flood" or dict from risks_found
        insurance_data: Loaded JSON data
    
    Returns:
        List of recommended insurance plans
    """
    # Handle if disaster_type is a dict from risks_found
    if isinstance(disaster_type, dict):
        # Extract disaster types from risks_found
        disaster_types = list(disaster_type.keys())
        if not disaster_types:
            return []
        # Use first detected risk for now
        disaster_type = disaster_types[0]
    
    return get_insurance_plans(disaster_type, insurance_data)

def format_insurance_response(disaster_type, insurance_data):
    """
    Converts insurance plans into a chatbot-friendly response.
    """
    plans = get_insurance_plans(disaster_type, insurance_data)
    
    if not plans:
        return f"Sorry, I couldn't find any insurance plans for **{disaster_type}**."
    
    response = f"Here are the recommended insurance plans for **{disaster_type.title()}**:\n\n"
    
    for plan in plans:
        response += (
            f"🛡️ **{plan['plan_name']}**\n"
            f"- Best for: {plan['best_for']}\n"
            f"- Premium: {plan['policy_details']['premium']}\n"
            f"- Coverage: {plan['policy_details']['coverage_amount']}\n"
            f"- Duration: {plan['policy_details']['policy_duration']}\n"
            f"- Waiting Period: {plan['policy_details']['waiting_period']}\n\n"
        )
    
    return response

# -------------------------------------------------------
# Load Insurance Plans (ONE TIME - at startup)
# -------------------------------------------------------
INSURANCE_DATA = load_insurance_data()

# Groq LLM Setup
GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.3-70b-versatile"

try:
    from groq import Groq
    groq_client = Groq(api_key=GROQ_API_KEY)
    LLM_AVAILABLE = True
except Exception:
    LLM_AVAILABLE = False
    groq_client = None

# 🎨 MODERN UI WITH ANIMATIONS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global font */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background - Modern gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        50% { background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); }
    }
    
    /* Chat container background */
    .block-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
    }
    
    /* Chat input container - Modern glassmorphism */
    .stChatFloatingInputContainer {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        animation: slideUp 0.5s ease;
    }
    
    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Chat messages - Glassmorphism cards */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 20px !important;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        animation: messageSlide 0.4s ease;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
    }
    
    @keyframes messageSlide {
        from { 
            transform: translateX(-20px); 
            opacity: 0; 
        }
        to { 
            transform: translateX(0); 
            opacity: 1; 
        }
    }
    
    /* User message - Purple accent */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%) !important;
        border-left: 5px solid #667eea;
    }
    
    /* Assistant message - White */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: rgba(255, 255, 255, 0.98) !important;
        border-left: 5px solid #4ade80;
    }
    
    /* Message text - Always dark for readability */
    .stChatMessage p, .stChatMessage div, .stChatMessage span, .stChatMessage li {
        color: #1a1a2e !important;
    }
    
    /* Risk badges - Animated */
    .risk-high {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white !important;
        padding: 12px 24px;
        border-radius: 30px;
        font-weight: 700;
        display: inline-block;
        margin: 15px 0;
        font-size: 18px;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4);
        animation: pulse 2s infinite, glow 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4); }
        50% { box-shadow: 0 6px 30px rgba(239, 68, 68, 0.6); }
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white !important;
        padding: 12px 24px;
        border-radius: 30px;
        font-weight: 700;
        display: inline-block;
        margin: 15px 0;
        font-size: 18px;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.4);
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .risk-low {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
        padding: 12px 24px;
        border-radius: 30px;
        font-weight: 700;
        display: inline-block;
        margin: 15px 0;
        font-size: 18px;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
    }
    
    /* Sidebar - Ultra modern gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%);
        animation: sidebarGlow 10s ease infinite;
    }
    
    @keyframes sidebarGlow {
        0%, 100% { background: linear-gradient(180deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%); }
        50% { background: linear-gradient(180deg, #312e81 0%, #4c1d95 50%, #1e1b4b 100%); }
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Sidebar buttons - Glassmorphism */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px);
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3);
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        transform: scale(1.05) translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar metrics - Glowing cards */
    .sidebar-metric {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 18px;
        margin: 12px 0;
        border-left: 5px solid #fbbf24;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease;
    }
    
    .sidebar-metric:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 25px rgba(251, 191, 36, 0.4);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .sidebar-metric h4 {
        color: #fbbf24 !important;
        margin: 0 0 8px 0;
        font-size: 0.95em;
        font-weight: 600;
    }
    
    .sidebar-metric p {
        color: white !important;
        margin: 0;
        font-size: 1.3em;
        font-weight: 700;
    }
    
    /* Title - Glowing effect */
    h1 {
        background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-size: 3em;
        margin-bottom: 0;
        font-weight: 900;
        text-shadow: 0 0 40px rgba(255, 255, 255, 0.5);
        animation: titleGlow 3s ease-in-out infinite;
    }
    
    @keyframes titleGlow {
        0%, 100% { text-shadow: 0 0 40px rgba(255, 255, 255, 0.5); }
        50% { text-shadow: 0 0 60px rgba(255, 255, 255, 0.8); }
    }
    
    /* Subtitle */
    .subtitle {
        color: rgba(255, 255, 255, 0.95);
        text-align: center;
        font-size: 1.3em;
        margin-bottom: 30px;
        font-weight: 500;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    /* Expander - Premium glassmorphism */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px);
        color: #1a1a2e !important;
        border-radius: 15px;
        border: 2px solid rgba(102, 126, 234, 0.5);
        font-weight: 700;
        padding: 15px;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.1) !important;
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(20px);
        color: #1a1a2e !important;
        padding: 25px;
        border-radius: 0 0 15px 15px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-top: none;
    }
    
    .streamlit-expanderContent * {
        color: #1a1a2e !important;
    }
    
    /* Columns - Clean separation */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="column"] * {
        color: #1a1a2e !important;
    }
    
    /* Download button - Premium style */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px;
        padding: 15px 30px;
        font-weight: 700;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Regular buttons - Gradient style */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 15px;
        padding: 12px 28px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    /* Input styling */
    input, textarea {
        color: #1a1a2e !important;
        background-color: white !important;
        border-radius: 12px;
    }
    
    /* Spinner - Colorful */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Quick tips box - Modern card */
    .tips-box {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        border: 2px solid rgba(255, 255, 255, 0.3);
        animation: fadeIn 0.8s ease;
    }
    
    .tips-box h3 {
        color: #667eea !important;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    .tips-box ul li {
        color: #1a1a2e !important;
        padding: 8px 0;
        font-weight: 500;
    }
    
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_context" not in st.session_state:
    st.session_state.user_context = {}
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

def extract_location_from_text(text):
    """FIXED: Smart extraction of location from natural language"""
    text_lower = text.lower()
    
    # FIXED: Skip insurance-related words to avoid "surance" bug
    skip_words = ['insurance', 'surance', 'coverage', 'policy', 'insured', 'insurer']
    for word in skip_words:
        text_lower = text_lower.replace(word, '')
    
    # Check for coordinates
    coord_pattern = r'(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)'
    coords = re.search(coord_pattern, text)
    if coords:
        return f"{coords.group(1)},{coords.group(2)}"
    
    # Check for city mentions with better parsing
    location_keywords = ["in", "at", "from", "live in", "located in", "staying in", "residing in", "based in"]
    for keyword in location_keywords:
        if keyword in text_lower:
            parts = text_lower.split(keyword)
            if len(parts) > 1:
                # Take the word after keyword
                potential_location = parts[1].strip().split()[0] if parts[1].strip().split() else None
                if potential_location:
                    potential_location = potential_location.strip(".,!?;:")
                    if len(potential_location) > 2:
                        return potential_location.title()
    
    # Extended list of Indian cities
    indian_cities = ["udupi", "mumbai", "delhi", "bangalore", "bengaluru", 
                     "chennai", "kolkata", "hyderabad", "pune", "ahmedabad",
                     "jaipur", "lucknow", "kanpur", "nagpur", "indore",
                     "bhopal", "visakhapatnam", "patna", "vadodara", "ghaziabad",
                     "ludhiana", "agra", "nashik", "faridabad", "meerut",
                     "rajkot", "kalyan", "vasai", "varanasi", "srinagar",
                     "aurangabad", "dhanbad", "amritsar", "navi mumbai", 
                     "allahabad", "howrah", "ranchi", "gwalior", "jabalpur",
                     "coimbatore", "vijayawada", "jodhpur", "madurai", "raipur"]
    
    for city in indian_cities:
        if city in text_lower:
            return city.title()
    
    return None

# -------------------------------------------------------
# Risk Summary Formatter (Human-friendly display)
# -------------------------------------------------------
def format_risk_summary(risk_summary, weather_analysis):
    level = risk_summary.get("level", "Unknown")
    score = risk_summary.get("score", 0)

    precip = weather_analysis.get("max_precip_mm", 0)
    temp = weather_analysis.get("max_temp_c", "N/A")
    wind = weather_analysis.get("max_wind_ms", "N/A")
    risks = weather_analysis.get("risks_found", {})

    risk_text = f"""
### 🎯 Overall Risk Assessment

**Risk Level:** {level}  
**Risk Score:** {score}

### 🌦️ Current Weather Indicators
- 🌧️ **Max Rainfall:** {precip} mm  
- 🌡️ **Max Temperature:** {temp} °C  
- 💨 **Max Wind Speed:** {wind} m/s  
"""

    if risks:
        risk_text += "\n### ⚠️ Detected Threats\n"
        for r, info in risks.items():
            risk_text += f"- **{r.title()}** ({info['level']}): {info['reason']}\n"
    else:
        risk_text += "\n### ✅ No Immediate Weather Threats Detected\n"

    return risk_text


def generate_conversational_response(user_message, plan_obj=None, has_location=False):
    """Generate natural, varied conversational response using Groq LLM"""
    if not LLM_AVAILABLE or not groq_client:
        return "I apologize, but the AI service is currently unavailable. Please try again later."
    
    try:
        # Build rich conversation context
        recent_context = "\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content'][:150]}" 
            for msg in st.session_state.conversation_history[-6:]
        ])
        
        if plan_obj:
            # Assessment completed - generate comprehensive response
            risk_level = plan_obj.get('risk_summary', {}).get('level', 'Unknown')
            risk_score = plan_obj.get('risk_summary', {}).get('score', 0)
            weather_data = plan_obj.get('weather_analysis', {})
            risks = weather_data.get('risks_found', {})
            insurance_plans = plan_obj.get('recommended_insurance', [])
            
            insurance_context = ""
            if insurance_plans:
                insurance_context = f"\n\nRECOMMENDED INSURANCE PLANS:\n"
                for plan in insurance_plans[:2]:  # Top 2 plans
                    insurance_context += f"- {plan['plan_name']}: {plan['best_for']}\n"
            
            prompt = f"""You are an empathetic, professional Disaster Preparedness Advisor having a natural conversation.

CONVERSATION CONTEXT:
{recent_context}

USER'S LATEST MESSAGE: "{user_message}"

RISK ASSESSMENT COMPLETED:
- Location: {plan_obj.get('location', 'Unknown')}
- Overall Risk Level: {risk_level} (Score: {risk_score})
- Weather Conditions:
  • Max Temperature: {weather_data.get('max_temp_c', 'N/A')}°C
  • Max Wind Speed: {weather_data.get('max_wind_ms', 'N/A')} m/s
  • Max Precipitation: {weather_data.get('max_precip_mm', 'N/A')} mm
  
DETECTED RISKS: {', '.join([f"{v['label']} ({v['metric']})" for k, v in risks.items()]) if risks else 'None detected'}

TOP PREPAREDNESS ACTIONS:
{json.dumps(plan_obj.get('plan', [])[:6], indent=2)}
{insurance_context}

INSTRUCTIONS FOR YOUR RESPONSE:
1. **Be conversational and natural** - Don't sound like a template or robot
2. **Start warmly** - Acknowledge their concern/question naturally
3. **Explain risk clearly** - Use simple language, be reassuring if risk is low, serious if high
4. **Focus on what matters** - Highlight 3-4 most important actions for their specific situation
5. **Be contextual** - If they mentioned flooding history, address that specifically
6. **Mention insurance briefly** - If plans are recommended, say "I've also identified some insurance options that could help protect you"
7. **End supportively** - Offer to answer questions, provide reassurance
8. **Vary your language** - Don't use the same phrases every time
9. **Keep it human** - Use contractions, natural transitions, empathy
10. **Format naturally** - Use paragraphs, bullet points only when truly helpful
11. **Length: 200-280 words** - Comprehensive but not overwhelming

Generate a natural, helpful response:"""

        elif has_location:
            # Location identified but not processed yet
            prompt = f"""You are a friendly Disaster Preparedness Advisor having a natural conversation.

CONVERSATION SO FAR:
{recent_context}

USER JUST SAID: "{user_message}"

SITUATION: You've identified their location. Now naturally transition to getting their risk assessment.

INSTRUCTIONS:
1. Acknowledge you understand their location
2. Show you're about to check weather/risk data
3. Ask if they have any disaster history or insurance they want to mention
4. Keep it conversational (2-3 sentences max)
5. Sound like a real person, not a bot

Generate a brief, natural response:"""

        else:
            # General conversation - guide toward location
            prompt = f"""You are a warm, professional Disaster Preparedness Advisor chatting naturally.

CONVERSATION HISTORY:
{recent_context}

USER'S MESSAGE: "{user_message}"

SITUATION: They haven't provided location yet, or you're having general chat.

INSTRUCTIONS:
1. Respond naturally to what they said
2. If greeting/intro: Welcome them warmly, explain you can help assess risks
3. If they mention disasters/concerns: Show empathy, ask about their location
4. If asking general questions: Answer helpfully, then guide to location
5. If asking about insurance: Explain you can recommend plans once you know their location and risks
6. Be conversational - use contractions, natural language
7. Don't be pushy, but gently guide toward getting location
8. Keep it brief: 60-100 words
9. Vary your responses - don't repeat phrases

Generate a natural response:"""
        
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600,
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"I'm having trouble processing that right now. Could you try rephrasing? (Error: {str(e)[:80]})"

def process_user_message(user_text):
    """Process user input and orchestrate workflow"""
    # Extract location
    location = extract_location_from_text(user_text)
    
    # Update context
    if location:
        st.session_state.user_context['location'] = location
        has_location = True
    else:
        has_location = 'location' in st.session_state.user_context
        location = st.session_state.user_context.get('location')
    
    # Extract policy mentions
    if any(word in user_text.lower() for word in ["policy", "insurance", "covered", "coverage"]):
        st.session_state.user_context['policy'] = "Standard Home Insurance"
    
    # Store history
    if not st.session_state.user_context.get('history'):
        st.session_state.user_context['history'] = user_text
    else:
        st.session_state.user_context['history'] += " " + user_text
    
    # If we have location, run assessment
    if location:
        try:
            # Prepare input
            user_input_obj = {
                "location": location,
                "policy": st.session_state.user_context.get('policy', 'Standard Home Insurance'),
                "history": st.session_state.user_context.get('history', user_text)
            }
            
            # Run risk assessment engine (callAPI, extractData, classifyText, compare, aggregate)
            with st.spinner("🔍 Analyzing weather data and assessing disaster risks..."):
                risk_result = risk_assessment_engine(user_input_obj)
            
            # -------------------------------------------------------
            # Insurance Recommendation Engine (NEW)
            # -------------------------------------------------------
            # Determine disaster context for insurance
            disaster_from_text = extract_disaster_from_text(user_text)
            
            if disaster_from_text:
                insurance_disaster = disaster_from_text
            elif risk_result.get("weather_analysis", {}).get("risks_found"):
                insurance_disaster = list(
                    risk_result["weather_analysis"]["risks_found"].keys()
                )[0]
            else:
                insurance_disaster = "flood"  # default fallback
            
            recommended_plans = get_insurance_plans(
                insurance_disaster,
                INSURANCE_DATA
            )

            
            # Create preparedness workflow (createWorkflow)
            plan_obj = create_preparedness_workflow(
                location=risk_result.get("location", "Unknown"),
                policy=risk_result.get("policy", "Standard Home Insurance"),
                risks_found=risk_result.get("weather_analysis", {}).get("risks_found", {})
            )
            
            # Aggregate all data
            plan_obj["risk_summary"] = risk_result.get("aggregate", {})
            plan_obj["weather_analysis"] = risk_result.get("weather_analysis", {})
            plan_obj["recommended_insurance"] = recommended_plans  # NEW: Add insurance
            plan_obj["generated_at"] = datetime.utcnow().isoformat()
            
            # Generate natural LLM response
            response = generate_conversational_response(user_text, plan_obj=plan_obj)
            
            # Add risk badge for displayInformation
            risk_level = plan_obj["risk_summary"]["level"]
            risk_class = f"risk-{risk_level.lower()}"
            risk_badge = f'<div class="{risk_class}">⚠️ Risk Level: {risk_level}</div>'
            
            final_response = f"{risk_badge}\n\n{response}"
            
            # Store plan
            st.session_state.last_plan = plan_obj
            
            return final_response, plan_obj
            
        except Exception as e:
            error_response = generate_conversational_response(
                f"Error processing {location}: {str(e)[:50]}", 
                has_location=False
            )
            return f"I encountered an issue analyzing {location}. {error_response}", None
    
    else:
        # No location yet - conversational guidance
        response = generate_conversational_response(user_text, has_location=has_location)
        return response, None

# Header
st.markdown("<h1>🌪️ Disaster Preparedness AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your intelligent advisor for weather risks and emergency planning</p>", unsafe_allow_html=True)

# Enhanced Sidebar with better design
with st.sidebar:
    st.markdown("### 🌪️ Disaster Preparedness AI")
    st.markdown("---")
    
    # System Status Dashboard
    st.markdown("### 📊 System Status")
    
    # LLM Status
    llm_status = "🟢 Active" if LLM_AVAILABLE else "🔴 Offline"
    st.markdown(f"""
    <div class="sidebar-metric">
        <h4>🤖 AI Engine</h4>
        <p>{llm_status}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Weather API Status
    st.markdown(f"""
    <div class="sidebar-metric">
        <h4>🌡️ Weather API</h4>
        <p>🟢 Open-Meteo Active</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Insurance Engine Status
    insurance_status = "🟢 Loaded" if INSURANCE_DATA else "🔴 Not Available"
    st.markdown(f"""
    <div class="sidebar-metric">
        <h4>🏦 Insurance Engine</h4>
        <p>{insurance_status}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model Info
    st.markdown(f"""
    <div class="sidebar-metric">
        <h4>⚙️ AI Model</h4>
        <p>Llama 3.3 70B</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Session Stats
    st.markdown("### 📈 Session Statistics")
    message_count = len(st.session_state.messages)
    location = st.session_state.user_context.get('location', 'Not set')
    
    st.markdown(f"""
    <div class="sidebar-metric">
        <h4>💬 Messages</h4>
        <p>{message_count}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="sidebar-metric">
        <h4>📍 Location</h4>
        <p>{location}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.session_state.user_context = {}
            st.rerun()
    
    st.markdown("---")
    
    # Feature Highlights
    st.markdown("### ✨ Features")
    st.markdown("""
    - 🌍 **Live Weather Data**
    - 🎯 **Risk Assessment**
    - 📋 **Custom Plans**
    - 🏦 **Insurance Recommendations**
    - 📊 **Data Analysis**
    - 💾 **Export Reports**
    """)
    
    st.markdown("---")

st.markdown(
    """
    <div class="tips-box">
        <h3>💡 Quick Tips</h3>
        <div>
            <strong>Example Queries:</strong>
            <ul>
                <li>🌆 Risk in Mumbai?</li>
                <li>📍 Weather for 13.34, 74.74</li>
                <li>🌧️ Heavy rains last week</li>
                <li>🏦 What insurance do I need?</li>
                <li>🛡️ Show me flood insurance</li>
            </ul>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)


if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        welcome_msg = """
        👋 Hello! I'm your Disaster Preparedness AI Assistant.
        I'm here to help you understand and prepare for weather-related disasters in your area. 
        I can analyze real-time weather data, assess risks, create personalized emergency preparedness plans, and recommend appropriate insurance coverage.
        
        **Here's what I do:**
        - Fetch live weather data from trusted sources
        - Assess disaster risks specific to your location  
        - Identify threats like floods, storms, heatwaves, and more
        - Create customized preparedness plans
        - Recommend insurance plans based on your risks
        - Guide you on insurance coverage
        
        **Let's get started!** Just tell me where you're located, and I'll check the current risks in your area.
        
        For example, you could say:
        - *"I live in Mumbai, what are the current risks?"*
        - *"Check weather for Udupi"*
        - *"We had flooding last month, what insurance do I need?"*
        - *"Show me insurance options for storms"*
        
        I'm ready when you are! 🛡️
        """
        st.markdown(welcome_msg)
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})


if prompt := st.chat_input("💬 Ask about disaster risks, weather, insurance, or emergency preparedness..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 Analyzing..."):
            response, plan_obj = process_user_message(prompt)
        
        st.markdown(response, unsafe_allow_html=True)
        
        if plan_obj:
            with st.expander("📊 View Complete Risk Assessment & Preparedness Plan"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(
                        format_risk_summary(
                            plan_obj["risk_summary"],
                            plan_obj["weather_analysis"]
                        ),
                        unsafe_allow_html=True
                    )

                
                with col2:
                    st.markdown("**📋 Your Preparedness Plan**")
                    for i, step in enumerate(plan_obj["plan"], 1):
                        st.markdown(f"**{i}.** {step}")
                
                if plan_obj.get("recommended_insurance"):
                    st.markdown("---")
                    st.markdown(
                        """<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 25px; border-radius: 15px; margin: 25px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
                        <h2 style='color: white; margin:0; font-weight:800; text-align:center;'>
                        🏦 Recommended Insurance Plans</h2>
                        </div>""",
                        unsafe_allow_html=True
                    )

                
                    for plan in plan_obj["recommended_insurance"]:
                        policy_details = plan.get("policy_details", {})
                
                        policy_explanation = (
                            policy_details.get("policy_explanation")
                            or plan.get("policy_explanation")
                            or "No explanation provided"
                        )
                
                        why_choose = plan.get("why_choose_this_plan", [])
                
                        st.markdown(f"""
                <div style='background: white; padding: 30px; border-radius: 20px; 
                border: 3px solid #667eea; margin: 25px 0;
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
                transition: all 0.3s ease;'>
                
                <h3 style='color: #667eea; font-weight: 800; margin-bottom: 20px; font-size: 1.8em;'>
                🛡️ {plan.get('plan_name', 'N/A')}
                </h3>
                
                <div style='background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                padding: 15px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #667eea;'>
                <strong style='color: #374151; font-size: 1.1em;'>📌 Best for:</strong><br>
                <span style='color: #1f2937; font-weight: 500; font-size: 1.05em;'>{plan.get('best_for', 'N/A')}</span>
                </div>
                
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0;'>
                
                <div style='background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                padding: 15px; border-radius: 12px; border-left: 5px solid #10b981;'>
                <strong style='color: #065f46; font-size: 1.1em;'>💰 Policy Cost</strong><br>
                <span style='color: #047857; font-weight: 700; font-size: 1.2em;'>{policy_details.get('policy_cost', 'N/A')}</span>
                </div>
                
                <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                padding: 15px; border-radius: 12px; border-left: 5px solid #3b82f6;'>
                <strong style='color: #1e40af; font-size: 1.1em;'>🛡️ Coverage</strong><br>
                <span style='color: #1e3a8a; font-weight: 700; font-size: 1.2em;'>{policy_details.get('coverage_amount', 'N/A')}</span>
                </div>
                
                <div style='background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%); 
                padding: 15px; border-radius: 12px; border-left: 5px solid #f97316;'>
                <strong style='color: #7c2d12; font-size: 1.1em;'>⏳ Duration</strong><br>
                <span style='color: #9a3412; font-weight: 700; font-size: 1.2em;'>{policy_details.get('policy_duration', 'N/A')}</span>
                </div>
                
                <div style='background: linear-gradient(135deg, #fecdd3 0%, #fda4af 100%); 
                padding: 15px; border-radius: 12px; border-left: 5px solid #f43f5e;'>
                <strong style='color: #881337; font-size: 1.1em;'>⏰ Waiting Period</strong><br>
                <span style='color: #9f1239; font-weight: 700; font-size: 1.2em;'>{policy_details.get('waiting_period', 'N/A')}</span>
                </div>
                
                </div>
                
                <div style='background: linear-gradient(135deg, #e9d5ff 0%, #d8b4fe 100%); 
                padding: 20px; border-radius: 12px; margin: 20px 0; border-left: 5px solid #a855f7;'>
                <strong style='color: #581c87; font-size: 1.2em;'>📘 Policy Explanation</strong><br>
                <span style='color: #3b0764; line-height: 1.7; font-weight: 500;'>{policy_explanation}</span>
                </div>
                
                <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                padding: 15px; border-radius: 12px; border-left: 5px solid #f59e0b; margin-bottom: 15px;'>
                <strong style='color: #78350f; font-size: 1.2em;'>⭐ Why choose this plan?</strong>
                </div>
                """, unsafe_allow_html=True)
                
                        if isinstance(why_choose, list) and why_choose:
                            for reason in why_choose:
                                st.markdown(f"""<div style='background: white; padding: 12px; 
                                margin: 10px 0; border-radius: 10px; border-left: 4px solid #10b981;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                                <span style='color: #1f2937; font-weight: 500;'>✓ {reason}</span>
                                </div>""", unsafe_allow_html=True)
                        elif isinstance(why_choose, str) and why_choose:
                            st.markdown(f"""<div style='background: white; padding: 12px; 
                            margin: 10px 0; border-radius: 10px; border-left: 4px solid #10b981;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <span style='color: #1f2937; font-weight: 500;'>✓ {why_choose}</span>
                            </div>""", unsafe_allow_html=True)
                        else:
                            st.markdown("""<div style='background: white; padding: 12px; 
                            margin: 10px 0; border-radius: 10px; border-left: 4px solid #9e9e9e;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <span style='color: #6b7280; font-weight: 500;'>- Not specified</span>
                            </div>""", unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                
                else:
                    st.info(
                        "💡 No specific insurance plans found for the detected risks. "
                        "Standard home insurance may provide basic coverage."
                    )



                
                st.markdown("---")
                st.download_button(
                    label="📥 Download Full Report (JSON)",
                    data=json.dumps(plan_obj, indent=2),
                    file_name=f"preparedness_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_history.append({"role": "assistant", "content": response})
