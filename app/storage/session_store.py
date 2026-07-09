from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4


class InMemorySessionStore:
    """Simple session store for assignment/demo use. Swap with DB later."""

    def __init__(self) -> None:
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def create(self, user_name: Optional[str] = None) -> Dict[str, Any]:
        session_id = str(uuid4())
        session = {
            "session_id": session_id,
            "user_name": user_name,
            "answers": {},
            "current_question_index": 0,
            "completed": False,
            "safety_locked": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "events": [],
        }
        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._sessions.get(session_id)

    def save(self, session: Dict[str, Any]) -> None:
        self._sessions[session["session_id"]] = session

    def all(self) -> list[Dict[str, Any]]:
        return list(self._sessions.values())


session_store = InMemorySessionStore()
