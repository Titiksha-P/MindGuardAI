from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class StartSessionRequest(BaseModel):
    user_name: Optional[str] = None


class StartSessionResponse(BaseModel):
    session_id: str
    message: str
    question: Dict[str, Any]
    progress: str
    answer_options: List[Dict[str, Any]]


class ChatMessageRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class ChatMessageResponse(BaseModel):
    session_id: str
    response_type: str
    message: str
    question: Optional[Dict[str, Any]] = None
    progress: Optional[str] = None
    answer_options: Optional[List[Dict[str, Any]]] = None
    score: Optional[int] = None
    severity: Optional[str] = None
    dsm5_profile: Optional[Dict[str, Any]] = None
    decision_trace: List[Dict[str, Any]]
    session_complete: bool = False


class SessionSummaryResponse(BaseModel):
    session_id: str
    user_name: Optional[str]
    answers: Dict[str, int]
    score: int
    severity: str
    dsm5_profile: Dict[str, Any]
    completed: bool
    events: List[Dict[str, Any]]
