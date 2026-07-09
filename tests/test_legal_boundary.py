from app.services.legal_boundary import check_legal_boundary


def test_diagnosis_request_blocked():
    result = check_legal_boundary("Do I have depression?")
    assert result["triggered"] is True
    assert result["response"] == "I do not diagnose medical conditions."


def test_medication_request_blocked():
    result = check_legal_boundary("Which antidepressant should I take?")
    assert result["triggered"] is True
