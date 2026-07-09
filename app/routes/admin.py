from fastapi import APIRouter
from app.storage.session_store import session_store
from app.services import phq9_engine
from app.services.compliance_engine import assignment_compliance, compact_trace_contract

router = APIRouter(prefix="/admin", tags=["admin-demo"])


@router.get("/compliance")
def compliance_report():
    return assignment_compliance()


@router.get("/decision-trace-contract")
def decision_trace_contract():
    return {"pipeline_order": compact_trace_contract()}


@router.get("/analytics")
def analytics():
    sessions = session_store.all()
    total = len(sessions)
    completed = [s for s in sessions if s.get("completed")]
    locked = [s for s in sessions if s.get("safety_locked")]
    severity_distribution = {"minimal": 0, "mild": 0, "moderate": 0, "moderately_severe": 0, "severe": 0}
    scores = []
    for session in completed:
        score = phq9_engine.calculate_score(session.get("answers", {}))
        scores.append(score)
        severity_distribution[phq9_engine.map_severity(score)] += 1
    return {
        "total_sessions": total,
        "completed_sessions": len(completed),
        "safety_overrides": len(locked),
        "completion_rate": round(len(completed) / total, 3) if total else 0,
        "average_score": round(sum(scores) / len(scores), 2) if scores else 0,
        "severity_distribution": severity_distribution,
    }


@router.get("/sessions")
def sessions():
    return {"sessions": session_store.all()}
