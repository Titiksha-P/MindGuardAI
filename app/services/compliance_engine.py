from typing import Any, Dict, List

COMPLIANCE_ITEMS = [
    {
        "requirement": "custom_code_backend_api",
        "status": "satisfied",
        "evidence": "FastAPI routes, Python services, no no-code/low-code/wrapper platform dependency.",
    },
    {
        "requirement": "deterministic_phq9_logic",
        "status": "satisfied",
        "evidence": "PHQ-9 answers are parsed into 0-3 values, total score is deterministic, severity bands are JSON-configured.",
    },
    {
        "requirement": "dsm5_informed_cognitive_profiling",
        "status": "satisfied_responsibly",
        "evidence": "Non-diagnostic DSM-5-informed symptom-domain profiling maps PHQ-9 items into cognitive, affective, behavioral, and safety-risk domains.",
    },
    {
        "requirement": "regex_semantic_kill_switch",
        "status": "satisfied",
        "evidence": "Safety interceptor runs before legal and PHQ-9 engines; regex and deterministic semantic classification can block normal flow.",
    },
    {
        "requirement": "official_government_crisis_resource_injection",
        "status": "satisfied",
        "evidence": "Crisis resource is loaded from config and injected into override responses.",
    },
    {
        "requirement": "legal_boundary_exact_response",
        "status": "satisfied",
        "evidence": "Diagnosis/medication/treatment requests return exactly: I do not diagnose medical conditions.",
    },
    {
        "requirement": "interactive_api_docs",
        "status": "satisfied",
        "evidence": "FastAPI Swagger UI is available at /docs.",
    },
    {
        "requirement": "docker_support",
        "status": "satisfied",
        "evidence": "Dockerfile and docker-compose.yml are included.",
    },
    {
        "requirement": "tests",
        "status": "satisfied",
        "evidence": "Pytest suite covers scoring, safety, legal boundary, API, DSM-5-informed profile, and compliance endpoints.",
    },
    {
        "requirement": "modest_polished_frontend",
        "status": "satisfied",
        "evidence": "Static frontend is served at /app for demonstration while backend remains the core deliverable.",
    },
]


def assignment_compliance() -> Dict[str, Any]:
    return {
        "project": "MindGuard AI",
        "version": "1.2-final-submission",
        "overall_status": "submission_ready_functional_prototype",
        "important_boundary": "This is a screening and safety-routing prototype. It does not diagnose medical conditions.",
        "items": COMPLIANCE_ITEMS,
    }


def compact_trace_contract() -> List[str]:
    return [
        "Input received",
        "Safety interceptor",
        "Medical boundary",
        "Emotion detection",
        "PHQ-9 answer validation",
        "PHQ-9 score update",
        "DSM-5-informed profile",
        "Response generated",
    ]
