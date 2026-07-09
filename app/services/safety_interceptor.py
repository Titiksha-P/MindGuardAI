import re
from typing import Any, Dict, List
from app.services.config_loader import load_json

TRIGGERS: Dict[str, Any] = load_json("safety_triggers.json")
CRISIS_RESOURCES: Dict[str, Any] = load_json("crisis_resources.json")


def semantic_risk_classifier(message: str) -> Dict[str, Any]:
    """
    Deterministic approximation of semantic risk.
    This avoids LLM hallucination and keeps the assignment fully custom-code.
    """
    text = message.lower()
    high_risk_fragments = [
        "no reason to live",
        "don't want to be here",
        "want everything to stop",
        "i might do something",
        "i am not safe",
        "goodbye forever",
    ]
    matched = [fragment for fragment in high_risk_fragments if fragment in text]
    return {
        "intent": "immediate_self_harm_risk" if matched else "none",
        "confidence": 0.91 if matched else 0.0,
        "matched_fragments": matched,
    }


def check_safety(message: str) -> Dict[str, Any]:
    regex_matches: List[str] = []
    for pattern in TRIGGERS["crisis_patterns"]:
        if re.search(pattern, message, flags=re.IGNORECASE):
            regex_matches.append(pattern)

    semantic = semantic_risk_classifier(message)
    semantic_triggered = semantic["intent"] in TRIGGERS["high_risk_intents"]
    triggered = bool(regex_matches) or semantic_triggered

    return {
        "triggered": triggered,
        "regex_matches": regex_matches,
        "semantic": semantic,
        "resources": CRISIS_RESOURCES if triggered else None,
    }


def crisis_response() -> str:
    resources = CRISIS_RESOURCES["resources"]
    resource_lines = "; ".join([f"{item['name']}: {item['contact']}" for item in resources])
    return f"{CRISIS_RESOURCES['message']} Resources: {resource_lines}. Emergency: {CRISIS_RESOURCES['emergency']}."
