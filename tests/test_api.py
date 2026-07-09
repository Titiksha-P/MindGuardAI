from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_session_start_and_complete_minimal_score():
    start = client.post("/session/start", json={"user_name": "Demo"})
    assert start.status_code == 200
    session_id = start.json()["session_id"]

    final = None
    for _ in range(9):
        final = client.post("/chat/message", json={"session_id": session_id, "message": "0"})
        assert final.status_code == 200

    data = final.json()
    assert data["session_complete"] is True
    assert data["score"] == 0
    assert data["severity"] == "minimal"


def test_crisis_override_blocks_flow():
    start = client.post("/session/start", json={})
    session_id = start.json()["session_id"]
    response = client.post("/chat/message", json={"session_id": session_id, "message": "suicide"})
    assert response.status_code == 200
    assert response.json()["response_type"] == "crisis_override"


def test_medical_boundary_exact_response():
    start = client.post("/session/start", json={})
    session_id = start.json()["session_id"]
    response = client.post("/chat/message", json={"session_id": session_id, "message": "Diagnose me"})
    assert response.status_code == 200
    assert response.json()["response_type"] == "medical_boundary"
    assert response.json()["message"] == "I do not diagnose medical conditions."


def test_completed_response_contains_dsm5_profile():
    start = client.post("/session/start", json={})
    session_id = start.json()["session_id"]
    final = None
    for value in [1, 1, 0, 0, 0, 0, 2, 0, 0]:
        final = client.post("/chat/message", json={"session_id": session_id, "message": str(value)})
    data = final.json()
    assert data["session_complete"] is True
    assert data["dsm5_profile"]["diagnostic_status"] == "non_diagnostic_profile_only"
    assert "concentration" in data["dsm5_profile"]["active_domains"]
