from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
RETENTION_CONFIG = ROOT / "config" / "compliance" / "retention_jobs.json"
SENSITIVE_PAYLOAD_KEYS = {
    "address",
    "biometric",
    "biometrics",
    "card",
    "cpf",
    "ctps",
    "document",
    "document_number",
    "email",
    "lat",
    "latitude",
    "lng",
    "longitude",
    "name",
    "phone",
    "prontuario",
    "raw_text",
    "storage_key",
}


@dataclass(frozen=True)
class RetentionCandidate:
    module: str
    record_id: str
    resource_type: str
    subject_id: str | None
    payload: dict[str, Any]
    legal_hold: list[str]
    requested_action: str | None = None
    legal_review_approved: bool = False

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "RetentionCandidate":
        return cls(
            module=str(raw["module"]),
            record_id=str(raw["record_id"]),
            resource_type=str(raw.get("resource_type") or "resource"),
            subject_id=str(raw["subject_id"]) if raw.get("subject_id") else None,
            payload=dict(raw.get("payload") or {}),
            legal_hold=[str(item) for item in raw.get("legal_hold", [])],
            requested_action=str(raw["requested_action"]) if raw.get("requested_action") else None,
            legal_review_approved=bool(raw.get("legal_review_approved", False)),
        )


@dataclass(frozen=True)
class RetentionDecision:
    module: str
    record_id: str
    resource_type: str
    job_name: str
    action: str
    status: str
    audit_event: str
    evidence: dict[str, Any]
    payload: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "module": self.module,
            "record_id": self.record_id,
            "resource_type": self.resource_type,
            "job_name": self.job_name,
            "action": self.action,
            "status": self.status,
            "audit_event": self.audit_event,
            "evidence": self.evidence,
            "payload": self.payload,
        }


def load_retention_config(path: Path = RETENTION_CONFIG) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def selector_hash(candidate: RetentionCandidate) -> str:
    source = {
        "module": candidate.module,
        "record_id": candidate.record_id,
        "resource_type": candidate.resource_type,
        "subject_id": candidate.subject_id,
    }
    return hashlib.sha256(json.dumps(source, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def deletion_receipt_hash(candidate: RetentionCandidate, job_name: str, observed_at: datetime) -> str:
    source = {
        "job_name": job_name,
        "module": candidate.module,
        "record_id": candidate.record_id,
        "selector_hash": selector_hash(candidate),
        "observed_at": observed_at.isoformat(),
    }
    return hashlib.sha256(json.dumps(source, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def anonymize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in payload.items():
        normalized_key = key.casefold()
        if normalized_key in SENSITIVE_PAYLOAD_KEYS or any(token in normalized_key for token in SENSITIVE_PAYLOAD_KEYS):
            redacted[key] = "[anonymized]"
        elif isinstance(value, dict):
            redacted[key] = anonymize_payload(value)
        elif isinstance(value, list):
            redacted[key] = [anonymize_payload(item) if isinstance(item, dict) else item for item in value]
        else:
            redacted[key] = value
    return redacted


def _base_evidence(
    candidate: RetentionCandidate,
    config: dict[str, Any],
    job_name: str,
    observed_at: datetime,
) -> dict[str, Any]:
    rule = config["module_rules"][candidate.module]
    return {
        "job_run_id": f"{job_name}:{observed_at.strftime('%Y%m%dT%H%M%SZ')}",
        "module": candidate.module,
        "policy_version": config["version"],
        "record_selector_hash": selector_hash(candidate),
        "evidence_domain": rule["evidence_domain"],
        "audit_event_id": f"{candidate.module}:{candidate.record_id}:{job_name}",
    }


def decide_retention(
    candidate: RetentionCandidate,
    job_name: str,
    *,
    dry_run: bool = False,
    observed_at: datetime | None = None,
    config: dict[str, Any] | None = None,
) -> RetentionDecision:
    config = config or load_retention_config()
    observed = observed_at or datetime.now(UTC)
    if candidate.module not in config["module_rules"]:
        raise ValueError(f"Modulo sem regra de retencao: {candidate.module}")
    if job_name not in config["jobs"]:
        raise ValueError(f"Job de retencao desconhecido: {job_name}")

    rule = config["module_rules"][candidate.module]
    evidence = _base_evidence(candidate, config, job_name, observed)
    hold_reasons = sorted(set(candidate.legal_hold).intersection(set(rule["legal_hold"])))
    if hold_reasons:
        evidence.update({"hold_reason": ",".join(hold_reasons), "hold_until": "manual_review"})
        return RetentionDecision(
            module=candidate.module,
            record_id=candidate.record_id,
            resource_type=candidate.resource_type,
            job_name=job_name,
            action="legal_hold",
            status="blocked",
            audit_event="compliance.legal_hold.applied",
            evidence=evidence,
            payload=candidate.payload,
        )

    action = candidate.requested_action or rule["default_action"]
    forbidden = set(config["safety_rules"]["forbidden_without_legal_review"])
    if action in forbidden and not candidate.legal_review_approved:
        evidence.update({"hold_reason": "legal_review_required", "hold_until": "approval"})
        return RetentionDecision(
            module=candidate.module,
            record_id=candidate.record_id,
            resource_type=candidate.resource_type,
            job_name=job_name,
            action=action,
            status="blocked",
            audit_event="compliance.legal_hold.applied",
            evidence=evidence,
            payload=candidate.payload,
        )

    if job_name == "retention_review_daily":
        evidence["candidate_count"] = 1
        return RetentionDecision(
            module=candidate.module,
            record_id=candidate.record_id,
            resource_type=candidate.resource_type,
            job_name=job_name,
            action=action,
            status="dry_run" if dry_run else "reviewed",
            audit_event="compliance.retention.reviewed",
            evidence=evidence,
            payload=candidate.payload,
        )

    if job_name == "anonymization_worker_hourly":
        evidence["anonymization_method"] = "field_redaction"
        return RetentionDecision(
            module=candidate.module,
            record_id=candidate.record_id,
            resource_type=candidate.resource_type,
            job_name=job_name,
            action=action,
            status="dry_run" if dry_run else "applied",
            audit_event="compliance.data.anonymized",
            evidence=evidence,
            payload=candidate.payload if dry_run else anonymize_payload(candidate.payload),
        )

    if job_name == "deletion_worker_daily":
        evidence["deletion_receipt_hash"] = deletion_receipt_hash(candidate, job_name, observed)
        return RetentionDecision(
            module=candidate.module,
            record_id=candidate.record_id,
            resource_type=candidate.resource_type,
            job_name=job_name,
            action=action,
            status="dry_run" if dry_run else "applied",
            audit_event="compliance.data.deleted",
            evidence=evidence,
            payload=candidate.payload if dry_run else {"deleted": True, "deleted_at": observed.isoformat()},
        )

    evidence.update({"hold_reason": "legal_hold_reconciliation", "hold_until": "policy_review"})
    return RetentionDecision(
        module=candidate.module,
        record_id=candidate.record_id,
        resource_type=candidate.resource_type,
        job_name=job_name,
        action="legal_hold_reconciliation",
        status="reviewed",
        audit_event="compliance.legal_hold.applied",
        evidence=evidence,
        payload=candidate.payload,
    )


def process_candidates(
    candidates: Iterable[RetentionCandidate],
    job_name: str,
    *,
    dry_run: bool = False,
    observed_at: datetime | None = None,
    config: dict[str, Any] | None = None,
) -> list[RetentionDecision]:
    config = config or load_retention_config()
    observed = observed_at or datetime.now(UTC)
    return [decide_retention(candidate, job_name, dry_run=dry_run, observed_at=observed, config=config) for candidate in candidates]


def _load_jsonl(path: Path) -> list[RetentionCandidate]:
    candidates: list[RetentionCandidate] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            candidates.append(RetentionCandidate.from_dict(json.loads(line)))
    return candidates


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Processa candidatos de retencao LGPD em JSONL.")
    parser.add_argument("--job", required=True, choices=sorted(load_retention_config()["jobs"]))
    parser.add_argument("--input", required=True, type=Path, help="Arquivo JSONL com candidatos de retencao.")
    parser.add_argument("--dry-run", action="store_true", help="Calcula decisoes sem aplicar transformacoes destrutivas.")
    args = parser.parse_args(argv)

    decisions = process_candidates(_load_jsonl(args.input), args.job, dry_run=args.dry_run)
    for decision in decisions:
        print(json.dumps(decision.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
