from app.services.safety_interceptor import check_safety


def test_regex_crisis_trigger():
    result = check_safety("suicide")
    assert result["triggered"] is True
    assert result["resources"] is not None


def test_semantic_crisis_trigger():
    result = check_safety("I am not safe right now")
    assert result["triggered"] is True
    assert result["semantic"]["intent"] == "immediate_self_harm_risk"


def test_safe_message_passes():
    result = check_safety("I feel tired today")
    assert result["triggered"] is False
