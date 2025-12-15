# primitive_functions/ classify_text.py

def classify_text(history_text):
    """
    Rule-based text classifier for incident history.
    
    Converts a short user-written history description into a 
    risk level: 'low', 'medium', or 'high'.

    NOTE:
    In a full LLM version, this function could call an LLM 
    to classify the text semantically. For this assignment, 
    rule-based logic meets the requirement.
    """
    if not history_text:
        return "low"

    text = history_text.lower()
    score = 0

    # Flood / Water-related signs
    if any(w in text for w in ["flood", "inundation", "overflow", "river"]):
        score += 2

    # Storm / Wind indicators
    if any(w in text for w in ["storm", "cyclone", "wind", "hail"]):
        score += 1

    # Repeated or recent incidents
    if any(w in text for w in ["frequent", "frequently", "repeated", "recent"]):
        score += 1

    # Severe events
    if "evacuated" in text or "major damage" in text:
        score += 3

    # Final classification
    if score >= 3:
        return "high"
    elif score >= 1:
        return "medium"
    else:
        return "low"
 
