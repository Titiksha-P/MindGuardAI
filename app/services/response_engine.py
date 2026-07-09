from typing import Any, Dict
from app.services import phq9_engine
from app.services.config_loader import load_json

TEMPLATES = load_json("response_templates.json")


def welcome_message(user_name: str | None = None) -> str:
    greeting = f"Hi {user_name}. " if user_name else ""
    return greeting + TEMPLATES["welcome"]


def next_question_payload(session: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "message": "Thanks. Please choose the option that fits best.",
        "question": phq9_engine.get_current_question(session),
        "progress": phq9_engine.progress_text(session),
        "answer_options": phq9_engine.answer_options(),
    }
