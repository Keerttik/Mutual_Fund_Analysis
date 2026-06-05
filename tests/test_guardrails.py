import pytest
from src.compliance.guardrails import check_input_guardrails, apply_output_guardrails

def test_check_input_guardrails_factual():
    query = "What is the expense ratio of the mid cap fund?"
    is_blocked, message = check_input_guardrails(query)
    assert not is_blocked
    assert message == ""

def test_check_input_guardrails_advisory():
    advisory_queries = [
        "Should I invest in HDFC Mid Cap?",
        "Is HDFC Small Cap a good investment?",
        "What is your recommendation for retirement?",
        "Please give me some advice on my portfolio."
    ]
    for query in advisory_queries:
        is_blocked, message = check_input_guardrails(query)
        assert is_blocked
        assert "I can only provide factual information" in message

def test_apply_output_guardrails_length():
    response = "This is sentence one. This is sentence two. This is sentence three. This is sentence four. This is sentence five."
    formatted = apply_output_guardrails(response, "hdfc-mid-cap")
    
    # Check that it only kept 3 sentences
    assert "This is sentence one." in formatted
    assert "This is sentence three." in formatted
    assert "This is sentence four." not in formatted

def test_apply_output_guardrails_footer():
    response = "This is a factual response."
    formatted = apply_output_guardrails(response, "hdfc-small-cap")
    
    assert "---" in formatted
    assert "Source: hdfc-small-cap" in formatted
    assert "Last updated from sources:" in formatted
