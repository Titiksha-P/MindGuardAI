from fastapi import APIRouter, HTTPException
from app.models.schemas import StartSessionRequest, StartSessionResponse, SessionSummaryResponse
from app.services import phq9_engine, response_engine
from app.services.dsm5_profile_engine import build_cognitive_profile
from app.storage.session_store import session_store

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/start", response_model=StartSessionResponse)
def start_session(payload: StartSessionRequest) -> StartSessionResponse:
    session = session_store.create(user_name=payload.user_name)
    question = phq9_engine.get_current_question(session)
    return StartSessionResponse(
        session_id=session["session_id"],
        message=response_engine.welcome_message(payload.user_name),
        question=question,
        progress=phq9_engine.progress_text(session),
        answer_options=phq9_engine.answer_options(),
    )


@router.get("/{session_id}/summary", response_model=SessionSummaryResponse)
def get_summary(session_id: str) -> SessionSummaryResponse:
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    score = phq9_engine.calculate_score(session["answers"])
    severity = phq9_engine.map_severity(score) if session["answers"] else "minimal"
    profile = build_cognitive_profile(session["answers"])
    return SessionSummaryResponse(
        session_id=session_id,
        user_name=session.get("user_name"),
        answers=session["answers"],
        score=score,
        severity=severity,
        dsm5_profile=profile,
        completed=session["completed"],
        events=session["events"],
    )
