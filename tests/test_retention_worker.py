import json
from datetime import UTC, datetime

from modules.shared.retention_worker import RetentionCandidate, anonymize_payload, decide_retention, process_candidates


NOW = datetime(2026, 5, 31, 15, 0, tzinfo=UTC)


def candidate(**overrides: object) -> RetentionCandidate:
    data = {
        "module": "crm",
        "record_id": "lead-1",
        "resource_type": "leads",
        "subject_id": "user-1",
        "payload": {"name": "Pessoa", "email": "pessoa@example.com", "campaign": "local"},
        "legal_hold": [],
    }
    data.update(overrides)
    return RetentionCandidate.from_dict(data)


def test_anonymization_worker_redacts_sensitive_fields_and_keeps_business_context() -> None:
    decision = decide_retention(
        candidate(module="delivery", payload={"address": "Rua A", "route_id": "R-1", "customer_phone": "999"}),
        "anonymization_worker_hourly",
        observed_at=NOW,
    )

    assert decision.status == "applied"
    assert decision.audit_event == "compliance.data.anonymized"
    assert decision.payload == {"address": "[anonymized]", "route_id": "R-1", "customer_phone": "[anonymized]"}
    assert decision.evidence["anonymization_method"] == "field_redaction"
    assert decision.evidence["audit_event_id"] == "delivery:lead-1:anonymization_worker_hourly"


def test_deletion_worker_emits_tombstone_and_receipt_hash() -> None:
    decision = decide_retention(candidate(module="vision", record_id="recording-1"), "deletion_worker_daily", observed_at=NOW)

    assert decision.status == "applied"
    assert decision.audit_event == "compliance.data.deleted"
    assert decision.payload == {"deleted": True, "deleted_at": "2026-05-31T15:00:00+00:00"}
    assert len(decision.evidence["deletion_receipt_hash"]) == 64
    assert decision.evidence["record_selector_hash"]


def test_dry_run_keeps_payload_and_marks_decision_without_applying() -> None:
    original = {"name": "Pessoa", "email": "pessoa@example.com"}

    decision = decide_retention(candidate(payload=original), "deletion_worker_daily", dry_run=True, observed_at=NOW)

    assert decision.status == "dry_run"
    assert decision.payload == original
    assert decision.audit_event == "compliance.data.deleted"


def test_legal_hold_blocks_destructive_or_anonymizing_actions() -> None:
    decision = decide_retention(
        candidate(module="finance", legal_hold=["ledger"], requested_action="delete_ledger"),
        "deletion_worker_daily",
        observed_at=NOW,
    )

    assert decision.status == "blocked"
    assert decision.action == "legal_hold"
    assert decision.audit_event == "compliance.legal_hold.applied"
    assert decision.evidence["hold_reason"] == "ledger"


def test_forbidden_action_requires_legal_review_even_without_current_hold() -> None:
    blocked = decide_retention(
        candidate(module="health", requested_action="delete_medical_record"),
        "deletion_worker_daily",
        observed_at=NOW,
    )
    approved = decide_retention(
        candidate(module="health", requested_action="delete_medical_record", legal_review_approved=True),
        "deletion_worker_daily",
        observed_at=NOW,
    )

    assert blocked.status == "blocked"
    assert blocked.evidence["hold_reason"] == "legal_review_required"
    assert approved.status == "applied"
    assert approved.payload["deleted"] is True


def test_process_candidates_reuses_single_policy_timestamp_for_batch() -> None:
    decisions = process_candidates(
        [
            candidate(module="crm", record_id="lead-1"),
            candidate(module="bi", record_id="export-1"),
        ],
        "retention_review_daily",
        dry_run=True,
        observed_at=NOW,
    )

    assert [decision.status for decision in decisions] == ["dry_run", "dry_run"]
    assert {decision.evidence["job_run_id"] for decision in decisions} == {"retention_review_daily:20260531T150000Z"}


def test_anonymize_payload_handles_nested_values() -> None:
    payload = {"profile": {"document_number": "123", "city": "SP"}, "items": [{"phone": "999", "sku": "A"}]}

    assert anonymize_payload(payload) == {
        "profile": {"document_number": "[anonymized]", "city": "SP"},
        "items": [{"phone": "[anonymized]", "sku": "A"}],
    }


def test_candidate_accepts_jsonl_style_payload() -> None:
    raw = json.loads(
        '{"module":"api_hub","record_id":"client-1","subject_id":"u","payload":{"api_key":"secret"},"legal_hold":[]}'
    )

    parsed = RetentionCandidate.from_dict(raw)

    assert parsed.module == "api_hub"
    assert parsed.resource_type == "resource"
    assert parsed.payload == {"api_key": "secret"}
