from app.services.phq9_engine import calculate_score, map_severity, parse_answer


def test_parse_numeric_answers():
    assert parse_answer("0") == 0
    assert parse_answer("1") == 1
    assert parse_answer("2") == 2
    assert parse_answer("3") == 3
    assert parse_answer("4") is None


def test_parse_label_answers():
    assert parse_answer("Not at all") == 0
    assert parse_answer("Several days") == 1
    assert parse_answer("More than half the days") == 2
    assert parse_answer("Nearly every day") == 3


def test_score_calculation():
    answers = {str(i): 1 for i in range(1, 10)}
    assert calculate_score(answers) == 9


def test_severity_mapping():
    assert map_severity(0) == "minimal"
    assert map_severity(5) == "mild"
    assert map_severity(10) == "moderate"
    assert map_severity(15) == "moderately_severe"
    assert map_severity(20) == "severe"
