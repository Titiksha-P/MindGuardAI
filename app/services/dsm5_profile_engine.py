from typing import Any, Dict
from app.services.config_loader import load_json

DSM5_CONFIG: Dict[str, Any] = load_json("dsm5_domains.json")


def _signal_label(value: int) -> str:
    if value <= 0:
        return "none"
    if value == 1:
        return "mild_signal"
    if value == 2:
        return "moderate_signal"
    return "high_signal"


def build_cognitive_profile(answers: Dict[str, int]) -> Dict[str, Any]:
    """
    Build a DSM-5-informed, non-diagnostic symptom-domain profile.

    This deliberately avoids diagnostic declarations. It only groups deterministic
    PHQ-9 item values into cognitive/affective/behavioral domains for explainability.
    """
    domain_results = {}
    active_domains = []
    risk_item_flag = False

    for key, domain in DSM5_CONFIG["domains"].items():
        item_values = []
        for item_id in domain["items"]:
            item_values.append(int(answers.get(str(item_id), 0)))
        total = sum(item_values)
        max_value = max(item_values) if item_values else 0
        signal = _signal_label(max_value)
        if signal != "none":
            active_domains.append(key)
        if key == "risk_item" and max_value > 0:
            risk_item_flag = True

        domain_results[key] = {
            "label": domain["label"],
            "description": domain["description"],
            "items": domain["items"],
            "score": total,
            "max_item_value": max_value,
            "signal": signal,
        }

    return {
        "framework": DSM5_CONFIG["framework_name"],
        "clinical_boundary": DSM5_CONFIG["clinical_boundary"],
        "diagnostic_status": "non_diagnostic_profile_only",
        "active_domains": active_domains,
        "risk_item_flag": risk_item_flag,
        "domains": domain_results,
    }
