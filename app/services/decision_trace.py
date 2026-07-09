from datetime import datetime, timezone
from typing import Any, Dict, List


def trace_step(name: str, status: str, details: Dict[str, Any] | None = None) -> Dict[str, Any]:
    return {
        "step": name,
        "status": status,
        "details": details or {},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def append_event(session: Dict[str, Any], event_type: str, payload: Dict[str, Any]) -> None:
    session["events"].append(trace_step(event_type, "recorded", payload))
