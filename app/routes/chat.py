from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatMessageRequest, ChatMessageResponse
from app.services import phq9_engine
from app.services.decision_trace import append_event, trace_step
from app.services.emotion_engine import detect_emotions
from app.services.legal_boundary import check_legal_boundary
from app.services.dsm5_profile_engine import build_cognitive_profile
from app.services.safety_interceptor import check_safety, crisis_response
from app.storage.session_store import session_store

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/message", response_model=ChatMessageResponse)
def chat_message(payload: ChatMessageRequest) -> ChatMessageResponse:
    session = session_store.get(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    trace = []
    trace.append(trace_step("Input received", "ok", {"message_length": len(payload.message)}))

    if session.get("safety_locked"):
        trace.append(trace_step("Safety lock", "blocked", {"reason": "Previous crisis override triggered"}))
        return ChatMessageResponse(
            session_id=payload.session_id,
            response_type="safety_locked",
            message=crisis_response(),
            decision_trace=trace,
            session_complete=session["completed"],
        )

    safety = check_safety(payload.message)
    trace.append(trace_step("Safety interceptor", "triggered" if safety["triggered"] else "passed", safety))
    if safety["triggered"]:
        session["safety_locked"] = True
        append_event(session, "safety_override", safety)
        session_store.save(session)
        trace.append(trace_step("Response generated", "blocked", {"response_type": "crisis_override"}))
        return ChatMessageResponse(
            session_id=payload.session_id,
            response_type="crisis_override",
            message=crisis_response(),
            decision_trace=trace,
            session_complete=False,
        )

    legal = check_legal_boundary(payload.message)
    trace.append(trace_step("Medical boundary", "triggered" if legal["triggered"] else "passed", legal))
    if legal["triggered"]:
        append_event(session, "medical_boundary", legal)
        session_store.save(session)
        trace.append(trace_step("Response generated", "blocked", {"response_type": "medical_boundary"}))
        return ChatMessageResponse(
            session_id=payload.session_id,
            response_type="medical_boundary",
            message="I do not diagnose medical conditions.",
            decision_trace=trace,
            session_complete=session["completed"],
        )

    emotions = detect_emotions(payload.message)
    trace.append(trace_step("Emotion detection", "ok", emotions))

    if session["completed"]:
        score = phq9_engine.calculate_score(session["answers"])
        severity = phq9_engine.map_severity(score)
        profile = build_cognitive_profile(session["answers"])
        trace.append(trace_step("DSM-5-informed profile", "ok", {"active_domains": profile["active_domains"], "diagnostic_status": profile["diagnostic_status"]}))
        trace.append(trace_step("Session status", "complete", {"score": score, "severity": severity}))
        return ChatMessageResponse(
            session_id=payload.session_id,
            response_type="already_complete",
            message=phq9_engine.build_result_message(score, severity),
            score=score,
            severity=severity,
            dsm5_profile=profile,
            decision_trace=trace,
            session_complete=True,
        )

    answer = phq9_engine.parse_answer(payload.message)
    trace.append(trace_step("PHQ-9 answer validation", "valid" if answer is not None else "invalid", {"parsed_answer": answer}))
    if answer is None:
        return ChatMessageResponse(
            session_id=payload.session_id,
            response_type="invalid_answer",
            message="Please answer using 0, 1, 2, or 3, or one of the quick-reply labels.",
            question=phq9_engine.get_current_question(session),
            progress=phq9_engine.progress_text(session),
            answer_options=phq9_engine.answer_options(),
            decision_trace=trace,
            session_complete=False,
        )

    session, completed = phq9_engine.record_answer(session, answer)
    append_event(session, "phq9_answer_recorded", {"answer": answer, "completed": completed})
    score = phq9_engine.calculate_score(session["answers"])
    severity = phq9_engine.map_severity(score)
    trace.append(trace_step("PHQ-9 score update", "ok", {"score": score, "severity": severity}))
    profile = build_cognitive_profile(session["answers"])
    trace.append(trace_step("DSM-5-informed profile", "ok", {"active_domains": profile["active_domains"], "risk_item_flag": profile["risk_item_flag"]}))

    session_store.save(session)

    if completed:
        trace.append(trace_step("Response generated", "ok", {"response_type": "screening_result"}))
        return ChatMessageResponse(
            session_id=payload.session_id,
            response_type="screening_result",
            message=phq9_engine.build_result_message(score, severity),
            score=score,
            severity=severity,
            dsm5_profile=profile,
            decision_trace=trace,
            session_complete=True,
        )

    trace.append(trace_step("Response generated", "ok", {"response_type": "next_question"}))
    return ChatMessageResponse(
        session_id=payload.session_id,
        response_type="next_question",
        message="Thanks. Please choose the option that fits best.",
        question=phq9_engine.get_current_question(session),
        progress=phq9_engine.progress_text(session),
        answer_options=phq9_engine.answer_options(),
        score=score,
        severity=severity,
        dsm5_profile=profile,
        decision_trace=trace,
        session_complete=False,
    )
