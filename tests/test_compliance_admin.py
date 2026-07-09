from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_compliance_report_marks_core_requirements_satisfied():
    response = client.get('/admin/compliance')
    assert response.status_code == 200
    data = response.json()
    assert data['overall_status'] == 'submission_ready_functional_prototype'
    statuses = {item['requirement']: item['status'] for item in data['items']}
    assert statuses['custom_code_backend_api'] == 'satisfied'
    assert statuses['deterministic_phq9_logic'] == 'satisfied'
    assert statuses['dsm5_informed_cognitive_profiling'] == 'satisfied_responsibly'
    assert statuses['regex_semantic_kill_switch'] == 'satisfied'


def test_decision_trace_contract_contains_safety_before_scoring():
    data = client.get('/admin/decision-trace-contract').json()
    order = data['pipeline_order']
    assert order.index('Safety interceptor') < order.index('PHQ-9 answer validation')
    assert order.index('Medical boundary') < order.index('PHQ-9 answer validation')


def test_admin_analytics_available():
    response = client.get('/admin/analytics')
    assert response.status_code == 200
    assert 'total_sessions' in response.json()
