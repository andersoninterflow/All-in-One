from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from fastapi import FastAPI, Header, HTTPException, Response
from pydantic import BaseModel, Field


PROTECTED_MODULES = {"marketplace", "delivery", "services", "mobility"}
OFF_PLATFORM_PATTERNS = (
    re.compile(r"\b(?:whats?app|telegram|instagram|facebook|pix)\b", re.IGNORECASE),
    re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", re.IGNORECASE),
    re.compile(r"https?://|www\.", re.IGNORECASE),
    re.compile(r"(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?\d{4,5}[-\s]?\d{4}"),
)


class CreatePayload(BaseModel):
    user_id: UUID
    entity_id: UUID | None = None
    status: str = Field(default="draft", max_length=40)
    payload: dict[str, Any] = Field(default_factory=dict)


class PatchPayload(BaseModel):
    status: str | None = Field(default=None, max_length=40)
    payload: dict[str, Any] = Field(default_factory=dict)


class DecisionPayload(BaseModel):
    id: UUID
    reason: str = Field(min_length=3, max_length=500)


class AuditPayload(BaseModel):
    action: str = Field(min_length=3, max_length=80)
    resource_type: str = Field(min_length=2, max_length=80)
    resource_id: UUID
    payload: dict[str, Any] = Field(default_factory=dict)


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _check_off_platform(module_name: str, payload: dict[str, Any]) -> None:
    if module_name not in PROTECTED_MODULES:
        return
    material = str(payload)
    if any(pattern.search(material) for pattern in OFF_PLATFORM_PATTERNS):
        raise HTTPException(
            status_code=422,
            detail="Conteudo bloqueado pela politica anti-burla; encaminhado para auditoria.",
        )


def create_module_app(module_name: str, version: str = "0.1.0") -> FastAPI:
    app = FastAPI(title=f"All-in-One {module_name}", version=version)
    records: dict[UUID, dict[str, Any]] = {}
    audit_events: list[dict[str, Any]] = []

    def record_audit(actor_user_id: UUID, action: str, resource_id: UUID, data: Any) -> None:
        audit_events.append(
            {
                "id": str(uuid4()),
                "actor_user_id": str(actor_user_id),
                "module": module_name,
                "action": action,
                "resource_id": str(resource_id),
                "data": data,
                "created_at": _now(),
            }
        )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "module": module_name}

    @app.get("/version")
    def get_version() -> dict[str, str]:
        return {"module": module_name, "version": version}

    @app.get("/status")
    def status() -> dict[str, Any]:
        return {"module": module_name, "state": "baseline_active", "records": len(records)}

    @app.get("/metrics")
    def metrics() -> Response:
        output = (
            f'all_in_one_records{{module="{module_name}"}} {len(records)}\n'
            f'all_in_one_audit_events{{module="{module_name}"}} {len(audit_events)}\n'
        )
        return Response(output, media_type="text/plain; version=0.0.4")

    @app.get("/list")
    def list_records(user_id: UUID | None = None) -> list[dict[str, Any]]:
        active = [item for item in records.values() if item["deleted_at"] is None]
        if user_id is None:
            return active
        return [item for item in active if item["user_id"] == str(user_id)]

    @app.post("/create", status_code=201)
    def create_record(
        body: CreatePayload,
        x_actor_user_id: UUID | None = Header(default=None, alias="X-Actor-User-Id"),
    ) -> dict[str, Any]:
        actor = x_actor_user_id
        if module_name == "identity" and actor is None:
            actor = body.user_id
        if actor is None:
            raise HTTPException(status_code=401, detail="X-Actor-User-Id obrigatorio.")
        _check_off_platform(module_name, body.payload)
        record_id = uuid4()
        item = {
            "id": str(record_id),
            "user_id": str(body.user_id),
            "entity_id": str(body.entity_id) if body.entity_id else None,
            "status": body.status,
            "payload": body.payload,
            "created_by": str(actor),
            "updated_by": str(actor),
            "created_at": _now(),
            "updated_at": _now(),
            "deleted_at": None,
        }
        records[record_id] = item
        record_audit(actor, "create", record_id, item)
        return item

    @app.get("/{resource_id}")
    def get_record(resource_id: UUID) -> dict[str, Any]:
        item = records.get(resource_id)
        if item is None or item["deleted_at"] is not None:
            raise HTTPException(status_code=404, detail="Registro nao encontrado.")
        return item

    @app.patch("/{resource_id}")
    def patch_record(
        resource_id: UUID,
        body: PatchPayload,
        x_actor_user_id: UUID = Header(alias="X-Actor-User-Id"),
    ) -> dict[str, Any]:
        item = get_record(resource_id)
        _check_off_platform(module_name, body.payload)
        before = dict(item)
        if body.status is not None:
            item["status"] = body.status
        item["payload"] = {**item["payload"], **body.payload}
        item["updated_by"] = str(x_actor_user_id)
        item["updated_at"] = _now()
        record_audit(x_actor_user_id, "update", resource_id, {"before": before, "after": item})
        return item

    @app.delete("/{resource_id}", status_code=204)
    def delete_record(
        resource_id: UUID,
        x_actor_user_id: UUID = Header(alias="X-Actor-User-Id"),
    ) -> Response:
        item = get_record(resource_id)
        item["deleted_at"] = _now()
        item["updated_by"] = str(x_actor_user_id)
        record_audit(x_actor_user_id, "soft_delete", resource_id, item)
        return Response(status_code=204)

    @app.post("/approve")
    def approve(
        body: DecisionPayload,
        x_actor_user_id: UUID = Header(alias="X-Actor-User-Id"),
    ) -> dict[str, Any]:
        item = get_record(body.id)
        item["status"] = "approved"
        item["updated_by"] = str(x_actor_user_id)
        item["updated_at"] = _now()
        record_audit(x_actor_user_id, "approve", body.id, {"reason": body.reason})
        return item

    @app.post("/reject")
    def reject(
        body: DecisionPayload,
        x_actor_user_id: UUID = Header(alias="X-Actor-User-Id"),
    ) -> dict[str, Any]:
        item = get_record(body.id)
        item["status"] = "rejected"
        item["updated_by"] = str(x_actor_user_id)
        item["updated_at"] = _now()
        record_audit(x_actor_user_id, "reject", body.id, {"reason": body.reason})
        return item

    @app.post("/audit", status_code=201)
    def audit(
        body: AuditPayload,
        x_actor_user_id: UUID = Header(alias="X-Actor-User-Id"),
    ) -> dict[str, Any]:
        record_audit(x_actor_user_id, body.action, body.resource_id, body.payload)
        return audit_events[-1]

    return app
