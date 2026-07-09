from typing import Any, Dict, List, Optional, Tuple
from app.services.config_loader import load_json

QUESTIONS: List[Dict[str, Any]] = load_json("phq9_questions.json")
THRESHOLDS: Dict[str, Dict[str, int]] = load_json("thresholds.json")
TEMPLATES: Dict[str, Any] = load_json("response_templates.json")

LABEL_TO_VALUE = {
    "not at all": 0,
    "several days": 1,
    "more than half the days": 2,
    "nearly every day": 3,
}


def parse_answer(raw_message: str) -> Optional[int]:
    normalized = raw_message.strip().lower()
    if normalized in LABEL_TO_VALUE:
        return LABEL_TO_VALUE[normalized]
    if normalized.isdigit():
        value = int(normalized)
        if value in {0, 1, 2, 3}:
            return value
    return None


def calculate_score(answers: Dict[str, int]) -> int:
    return sum(answers.values())


def map_severity(score: int) -> str:
    for severity, bounds in THRESHOLDS.items():
        if bounds["min"] <= score <= bounds["max"]:
            return severity
    raise ValueError(f"PHQ-9 score out of range: {score}")


def get_current_question(session: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    index = session["current_question_index"]
    if index >= len(QUESTIONS):
        return None
    return QUESTIONS[index]


def record_answer(session: Dict[str, Any], answer: int) -> Tuple[Dict[str, Any], bool]:
    question = get_current_question(session)
    if not question:
        session["completed"] = True
        return session, True

    session["answers"][str(question["id"])] = answer
    session["current_question_index"] += 1
    if session["current_question_index"] >= len(QUESTIONS):
        session["completed"] = True
        return session, True
    return session, False


def build_result_message(score: int, severity: str) -> str:
    friendly = severity.replace("_", " ")
    return (
        f"Your screening score is {score}, which falls in the {friendly} range. "
        f"{TEMPLATES['screening_disclaimer']}"
    )


def progress_text(session: Dict[str, Any]) -> str:
    current = min(session["current_question_index"] + 1, len(QUESTIONS))
    return f"Question {current} of {len(QUESTIONS)}"


def answer_options() -> List[Dict[str, Any]]:
    return TEMPLATES["answer_options"]
