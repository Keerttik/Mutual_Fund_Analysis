import re
from datetime import datetime

# Basic list of keywords that indicate an advisory question
ADVISORY_KEYWORDS = [
    "should i invest", "good investment", "recommend", "advice", 
    "is it safe", "go up", "price prediction", "should i buy",
    "should i sell", "portfolio", "retire"
]

def check_input_guardrails(query: str) -> tuple[bool, str]:
    """
    Checks if the user query violates compliance rules (e.g., asking for advice).
    Returns (is_blocked: bool, block_message: str)
    """
    query_lower = query.lower()
    for kw in ADVISORY_KEYWORDS:
        if kw in query_lower:
            return True, "I can only provide factual information about HDFC mutual funds. I cannot provide investment advice or recommendations."
            
    return False, ""

def apply_output_guardrails(response: str, source_id: str) -> str:
    """
    Applies length validation, citation, and the mandatory footer.
    """
    # 1. Length Validator (Truncate to 3 sentences max)
    sentences = re.split(r'(?<=[.!?]) +', response.strip())
    if len(sentences) > 3:
        response = " ".join(sentences[:3])

    # 2. Automatically append footer and citation
    today = datetime.now().strftime("%Y-%m-%d")
    footer = f"\n\n---\n*Source: {source_id if source_id else 'General Context'}*\n*Last updated from sources: {today}*"
    
    return response + footer
