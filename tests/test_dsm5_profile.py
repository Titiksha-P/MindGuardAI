from app.services.dsm5_profile_engine import build_cognitive_profile


def test_dsm5_profile_is_non_diagnostic_and_domain_based():
    profile = build_cognitive_profile({"1": 2, "7": 3, "9": 0})
    assert profile["diagnostic_status"] == "non_diagnostic_profile_only"
    assert "diagnose" in profile["clinical_boundary"].lower()
    assert "anhedonia" in profile["active_domains"]
    assert "concentration" in profile["active_domains"]
    assert profile["risk_item_flag"] is False


def test_risk_item_flag_when_item_9_non_zero():
    profile = build_cognitive_profile({"9": 1})
    assert profile["risk_item_flag"] is True
    assert profile["domains"]["risk_item"]["signal"] == "mild_signal"
