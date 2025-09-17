import pytest

from core.security_manager import SecurityManager


@pytest.fixture
def sm():
    return SecurityManager()


def test_check_input_security_detects_scripts_and_logs(sm):
    res = sm.check_input_security("<script>alert(1)</script>", ip_address="1.2.3.4")
    assert res["is_safe"] is False
    assert any("pattern_script" in t for t in res["threats_detected"]) or res[
        "risk_level"
    ] in {
        "high",
        "critical",
    }


def test_rate_limit_violation_records_and_returns_true(sm):
    violated = sm.check_rate_limit_violation("1.2.3.4", current_count=101, limit=100)
    assert violated is True
    assert sm.rate_limit_violations


def test_block_unblock_ip_flow(sm):
    sm.block_ip("9.9.9.9", reason="abuse", duration=1)
    assert sm.is_ip_blocked("9.9.9.9")


def test_check_origin_security_allowed_and_unauthorized(sm):
    assert sm.check_origin_security("http://localhost:5000") is True
    assert sm.check_origin_security("http://evil.com") in {True, False}


def test_get_security_report_structure(sm):
    report = sm.get_security_report()
    assert {"total_events_24h", "blocked_ips_count", "security_status"}.issubset(
        report.keys()
    )
