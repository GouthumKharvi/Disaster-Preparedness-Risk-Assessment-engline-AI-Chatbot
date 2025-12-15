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
    Loads disaster insurance plans from JSON file with error handling.
    """
    base_path = r"C:\Users\Gouthum\Downloads\Assisto Technologies Inc\JSON"
    file_path = os.path.join(base_path, "disaster_insurance.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Remove BOM if present
            content = content.lstrip('\ufeff')
            data = json.loads(content)
        return data
    except json.JSONDecodeError as e:
        st.error(f"JSON parsing error in insurance file at line {e.lineno}, column {e.colno}: {e.msg}")
        st.warning("Please check your disaster_insurance.json file for syntax errors (extra commas, missing brackets, etc.)")
        return {}
    except FileNotFoundError:
        st.warning(f"Insurance data file not found at: {file_path}")
        return {}
    except Exception as e:
        st.error(f"Failed to load insurance data: {str(e)}")
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

# Enhanced CSS with all visibility fixes
st.markdown("""
<style>
    /* Main background - lighter gradient */
    .main {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
    }
    
    /* Chat input container */
    .stChatFloatingInputContainer {
        background-color: white !important;
        border: 2px solid #667eea;
        border-radius: 15px;
        padding: 10px;
    }
    
    /* All chat messages - white background */
    .stChatMessage {
        background-color: white !important;
        border-radius: 15px;
        padding: 15px !important;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        color: #1a1a1a !important;
    }
    
    /* User message specific */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #e3f2fd !important;
    }
    
    /* Assistant message specific */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background-color: #f5f5f5 !important;
    }
    
    /* Message content text */
    .stChatMessage p, .stChatMessage div, .stChatMessage span {
        color: #1a1a1a !important;
    }
    
    /* Risk badges - high contrast */
    .risk-high {
        background-color: #d32f2f;
        color: white !important;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0;
        font-size: 16px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .risk-medium {
        background-color: #f57c00;
        color: white !important;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0;
        font-size: 16px;
    }
    
    .risk-low {
        background-color: #388e3c;
        color: white !important;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0;
        font-size: 16px;
    }
    
    /* Insurance plan cards */
    .insurance-card {
        background-color: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
    }
    
    .insurance-card h4 {
        color: #667eea;
        margin: 0 0 10px 0;
    }
    
    /* Sidebar - modern gradient design */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a237e 0%, #283593 50%, #3949ab 100%);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        background-color: white !important;
        color: #1a237e !important;
        border: 2px solid white;
        font-weight: bold;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #e8eaf6 !important;
        transform: scale(1.05);
    }
    
    /* Sidebar metrics */
    .sidebar-metric {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #ffd54f;
    }
    
    .sidebar-metric h4 {
        color: #ffd54f !important;
        margin: 0 0 5px 0;
        font-size: 0.9em;
    }
    
    .sidebar-metric p {
        color: white !important;
        margin: 0;
        font-size: 1.2em;
        font-weight: bold;
    }
    
    /* Title with shadow for readability */
    h1 {
        color: #4a148c;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 0;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.5);
        font-weight: bold;
    }
    
    /* Subtitle */
    .subtitle {
        color: #6a1b9a;
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 30px;
        font-weight: 500;
    }
    
    /* CRITICAL FIX: Expander with WHITE background and DARK text */
    .streamlit-expanderHeader {
        background-color: white !important;
        color: #1a1a1a !important;
        border-radius: 10px;
        border: 2px solid #667eea;
    }
    
    .streamlit-expanderContent {
        background-color: white !important;
        color: #1a1a1a !important;
        padding: 20px;
    }
    
    /* CRITICAL FIX: All expander text must be dark */
    .streamlit-expanderContent * {
        color: #1a1a1a !important;
        background-color: transparent !important;
    }
    
    /* CRITICAL FIX: Column headers and text */
    [data-testid="column"] {
        background-color: white !important;
        padding: 15px;
        border-radius: 10px;
    }
    
    [data-testid="column"] * {
        color: #1a1a1a !important;
    }
    
    /* CRITICAL FIX: JSON display - WHITE background, DARK text */
    .stJson {
        background-color: white !important;
        color: #1a1a1a !important;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .stJson * {
        background-color: white !important;
        color: #1a1a1a !important;
    }
    
    /* CRITICAL FIX: JSON pre and code elements */
    .stJson pre, 
    .stJson code,
    pre,
    code {
        background-color: #f8f9fa !important;
        color: #212529 !important;
        border: 1px solid #dee2e6;
        padding: 5px;
        border-radius: 4px;
    }
    
    /* CRITICAL FIX: Download button */
    .stDownloadButton > button {
        background-color: white !important;
        color: #667eea !important;
        border: 2px solid #667eea !important;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stDownloadButton > button:hover {
        background-color: #667eea !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Input text color */
    input, textarea {
        color: #1a1a1a !important;
        background-color: white !important;
    }
    
    /* Spinner text */
    .stSpinner > div {
        color: #667eea !important;
    }
    
    /* Markdown in columns */
    [data-testid="column"] .element-container {
        background-color: transparent !important;
    }
    
    [data-testid="column"] h1,
    [data-testid="column"] h2,
    [data-testid="column"] h3,
    [data-testid="column"] h4,
    [data-testid="column"] p,
    [data-testid="column"] strong {
        color: #1a1a1a !important;
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

with st.expander("💡 Quick Tips"):
    st.markdown("""
    **Example Queries:**
    - "Risk in Mumbai?"
    - "Weather for 13.34, 74.74"
    - "Heavy rains last week"
    - "What insurance do I need?"
    - "Show me flood insurance"
    """)

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #ffd54f; font-size: 0.8em;'>Developed By Gouthum</p>", unsafe_allow_html=True)


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
                    st.markdown("**🎯 Risk Summary**")
                    st.json(plan_obj["risk_summary"])
                    
                    st.markdown("**🌡️ Weather Analysis**")
                    st.json(plan_obj["weather_analysis"])
                
                with col2:
                    st.markdown("**📋 Your Preparedness Plan**")
                    for i, step in enumerate(plan_obj["plan"], 1):
                        st.markdown(f"**{i}.** {step}")
                
                if plan_obj.get("recommended_insurance"):
                    st.markdown("---")
                    st.markdown("## 🏦 Recommended Insurance Plans")
                
                    for plan in plan_obj["recommended_insurance"]:
                        policy_details = plan.get("policy_details", {})
                
                        policy_explanation = (
                            policy_details.get("policy_explanation")
                            or plan.get("policy_explanation")
                            or "No explanation provided"
                        )
                
                        why_choose = plan.get("why_choose_this_plan", [])
                
                        st.markdown(f"""
                ### 🛡️ {plan.get('plan_name', 'N/A')}
                
                **Best for:**  
                {plan.get('best_for', 'N/A')}
                
                **💰 Policy Cost:**  
                {policy_details.get('policy_cost', 'N/A')}
                
                **🛡️ Coverage:**  
                {policy_details.get('coverage_amount', 'N/A')}
                
                **⏳ Duration:**  
                {policy_details.get('policy_duration', 'N/A')}
                
                **⏰ Waiting Period:**  
                {policy_details.get('waiting_period', 'N/A')}
                
                **📘 Policy Explanation:**  
                {policy_explanation}
                
                **⭐ Why choose this plan?**
                """)
                
                        if isinstance(why_choose, list) and why_choose:
                            for reason in why_choose:
                                st.markdown(f"- {reason}")
                        elif isinstance(why_choose, str) and why_choose:
                            st.markdown(f"- {why_choose}")
                        else:
                            st.markdown("- Not specified")
                
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
