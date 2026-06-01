import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ALERTS = {
    "RetentionCronJobFailed",
    "RetentionCronJobDelayed",
    "RetentionBacklogHigh",
    "RetentionOldestCandidateTooOld",
    "RetentionDecisionMissing",
}


def load_alerts() -> dict:
    return json.loads((ROOT / "config" / "observability" / "retention_alerts.json").read_text(encoding="utf-8"))


def test_retention_alerts_cover_failure_delay_backlog_and_missing_decisions() -> None:
    alerts = load_alerts()

    assert set(alerts["alerts"]) == REQUIRED_ALERTS
    assert alerts["scope"] == "retention-worker"
    assert alerts["runbook"] == "docs/OPERATIONS.md#retencao-lgpd"
    assert alerts["notification_policy"]["include_sensitive_payload"] is False


def test_retention_alerts_have_prometheus_expr_sla_and_evidence() -> None:
    alerts = load_alerts()

    for name, alert in alerts["alerts"].items():
        assert alert["severity"] in {"critical", "high", "medium"}
        assert alert["expr"], name
        assert alert["for"].endswith("m"), name
        assert 1 <= alert["response_sla_minutes"] <= 240, name
        assert "incident_ticket" in alert["evidence"], name
        assert "payload" not in " ".join(alert["evidence"]).casefold(), name


def test_retention_alert_expressions_reference_expected_signals() -> None:
    alerts = load_alerts()["alerts"]

    assert "kube_job_status_failed" in alerts["RetentionCronJobFailed"]["expr"]
    assert "kube_job_status_completion_time" in alerts["RetentionCronJobDelayed"]["expr"]
    assert "all_in_one_retention_candidates_pending" in alerts["RetentionBacklogHigh"]["expr"]
    assert "all_in_one_retention_oldest_candidate_age_seconds" in alerts["RetentionOldestCandidateTooOld"]["expr"]
    assert "all_in_one_retention_decisions_total" in alerts["RetentionDecisionMissing"]["expr"]
