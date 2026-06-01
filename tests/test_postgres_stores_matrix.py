import importlib
import os
from uuid import UUID, uuid4

import psycopg
import pytest

from modules.shared.domain_rules import event_for_create, rule_for
from modules.shared.postgres_store import BasePostgresStore


POSTGRES_DSN = os.getenv("ALL_IN_ONE_POSTGRES_MATRIX_DSN")
pytestmark = pytest.mark.skipif(
    not POSTGRES_DSN,
    reason="DSN PostgreSQL da matriz de stores nao configurado.",
)


MODULE_CASES = [
    ("identity", "users"),
    ("business", "companies"),
    ("permissions", "roles"),
    ("finance", "wallets"),
    ("marketplace", "stores"),
    ("stock", "suppliers"),
    ("delivery", "delivery_requests"),
    ("riders", "rider_profiles"),
    ("services", "providers"),
    ("mobility", "rides"),
    ("jobs", "resumes"),
    ("erp", "fiscal_documents"),
    ("wms", "warehouses"),
    ("tms", "freights"),
    ("crm", "opportunities"),
    ("bpm", "workflow_instances"),
    ("document", "documents"),
    ("hr", "employees"),
    ("health", "patients"),
    ("vision", "devices"),
    ("legal", "cases"),
    ("property", "properties"),
    ("bi", "dashboards"),
    ("ai_core", "moderation_decisions"),
    ("api_hub", "api_clients"),
]


def class_name(module: str) -> str:
    return f"{module.title().replace('_', '')}PostgresStore"


def store_for(module: str):
    mod = importlib.import_module(f"modules.shared.{module}_postgres_store")
    return getattr(mod, class_name(module))(POSTGRES_DSN)


def seed_identity_and_company(nonce: str, *, seed_user: bool = True) -> tuple[str, str]:
    user_id = str(uuid4())
    company_id = str(uuid4())
    company_nonce = uuid4().hex[:12]
    with psycopg.connect(POSTGRES_DSN) as connection:
        if seed_user:
            connection.execute(
                """INSERT INTO identity.users
                   (id, full_name, cpf_document, birth_date, email, phone_e164, password_hash,
                    face_hash, liveness_score, terms_accepted_at, lgpd_consent_at, status)
                   VALUES (%s, %s, %s, DATE '1990-01-01', %s, %s, %s, %s, 0.9900, NOW(), NOW(), 'active')""",
                (
                    user_id,
                    f"Usuario Matrix {nonce}",
                    f"CPF-{nonce}",
                    f"matrix-{nonce}@example.test",
                    f"+55119{str(int(nonce[:7], 16)).zfill(8)[-8:]}",
                    f"hash-{nonce}",
                    f"face-{nonce}",
                ),
            )
        if seed_user:
            connection.execute(
                """INSERT INTO business.companies
                   (id, user_id, cnpj, root_cnpj, legal_name, legal_representative_user_id, status, created_by, updated_by)
                   VALUES (%s, %s, %s, %s, %s, %s, 'active', %s, %s)""",
                (
                    company_id,
                    user_id,
                    f"{int(company_nonce[:12], 16):014d}"[-14:],
                    f"{int(company_nonce[:8], 16):08d}"[-8:],
                    f"Empresa Matrix {nonce}",
                    user_id,
                    user_id,
                    user_id,
                ),
            )
    return user_id, company_id


def payload_for(module: str, resource_type: str, user_id: str, company_id: str, nonce: str) -> dict:
    common = {
        "company_id": company_id,
        "company_status": "active",
        "name": f"Registro Matrix {nonce}",
        "title": f"Titulo Matrix {nonce}",
        "amount_brl": "10.00",
        "risk_brl": "10.00",
        "expected_value_brl": "10.00",
        "freight_brl": "10.00",
        "toll_brl": "1.00",
        "definition": {"widgets": []},
        "address": {"street": "Rua Matrix", "number": nonce[:4]},
        "scopes": ["matrix:test"],
    }
    specific = {
        "identity": {
            "id": user_id,
            "full_name": f"Usuario Identity {nonce}",
            "cpf_document": f"ID-{nonce}",
            "document_cpf": f"ID-{nonce}",
            "birth_date": "1990-01-01",
            "email": f"identity-{nonce}@example.test",
            "phone_e164": f"+55118{str(int(nonce[:7], 16)).zfill(8)[-8:]}",
            "password_hash": f"hash-{nonce}",
            "face_hash": f"identity-face-{nonce}",
            "liveness_score": "0.9900",
            "terms_accepted_at": "2026-05-30T00:00:00Z",
            "lgpd_consent_at": "2026-05-30T00:00:00Z",
        },
        "business": {
            "cnpj": f"{int(nonce[:12], 16):014d}"[-14:],
            "root_cnpj": f"{int(nonce[:8], 16):08d}"[-8:],
            "legal_name": f"Business Matrix {nonce}",
            "legal_representative_user_id": user_id,
        },
        "permissions": {"name": f"role-{nonce}", "module": "matrix", "action": "create", "scope": "matrix", "limit_brl": "10.00"},
        "finance": {"wallet_type": f"matrix-{nonce}"},
        "marketplace": {"company_id": company_id, "company_status": "active", "name": f"Loja Matrix {nonce}"},
        "stock": {"company_id": company_id, "company_status": "active"},
        "delivery": {"service_type": "package", "origin": {"lat": 0}, "destination": {"lat": 1}},
        "riders": {"cnh_number_hash": f"cnh-{nonce}", "cnh_category": "AB", "wallet_id": str(uuid4())},
        "services": {"category": "maintenance"},
        "mobility": {"origin": {"lat": 0}, "destination": {"lat": 1}, "vehicle_type": "car"},
        "jobs": {"headline": f"Pessoa candidata {nonce}", "recruiter_visibility": "private"},
        "erp": {"company_id": company_id, "document_type": "nfe", "amount_brl": "10.00", "tax_amount_brl": "2.00"},
        "wms": {"company_id": company_id, "name": f"Armazem {nonce}", "addressing_rules": {"mode": "zone"}},
        "tms": {"company_id": company_id, "freight_brl": "10.00", "toll_brl": "1.00", "carrier_id": str(uuid4())},
        "crm": {"company_id": company_id, "title": f"Oportunidade {nonce}", "expected_value_brl": "10.00"},
        "bpm": {"company_id": company_id, "process_key": f"process-{nonce}"},
        "document": {"company_id": company_id, "storage_key": f"matrix/{nonce}.pdf", "filename": f"{nonce}.pdf"},
        "hr": {"company_id": company_id, "employment_type": "clt", "position_title": "Analista"},
        "health": {"health_identifier": f"health-{nonce}"},
        "vision": {"device_fingerprint": f"device-{nonce}", "location_label": "Lab"},
        "legal": {"company_id": company_id, "case_number": f"case-{nonce}", "risk_brl": "10.00"},
        "property": {"company_id": company_id, "address": {"street": "Rua Matrix"}, "property_type": "commercial"},
        "bi": {"company_id": company_id, "name": f"Dashboard {nonce}", "definition": {"widgets": []}},
        "ai_core": {"module": "matrix", "risk_score": "0.10", "reasons": []},
        "api_hub": {
            "company_id": company_id,
            "client_name": f"Client {nonce}",
            "client_id_hash": f"client-hash-{nonce}",
            "secret_reference": f"secret/{nonce}",
            "scopes": ["matrix:test"],
        },
    }
    payload = dict(common)
    payload.update(specific[module])
    return payload


@pytest.mark.parametrize(("module", "resource_type"), MODULE_CASES)
def test_postgres_store_matrix_core_contract(module: str, resource_type: str) -> None:
    nonce = uuid4().hex[:12]
    user_id, company_id = seed_identity_and_company(nonce, seed_user=module != "identity")
    store = store_for(module)
    rule = rule_for(module, resource_type)
    payload = payload_for(module, resource_type, user_id, company_id, nonce)
    idempotency_key = f"matrix-{module}-{nonce}"
    entity_id = None if module == "identity" else company_id

    created = store.create(
        resource_type,
        user_id,
        entity_id,
        rule.initial_status,
        payload,
        user_id,
        rule.unique_fields,
        event_for_create(module, resource_type),
        idempotency_key,
    )

    assert UUID(created["id"])
    assert created["module"] == module
    assert created["resource_type"] == resource_type
    assert created["user_id"] == user_id
    assert created["status"] == rule.initial_status
    assert store.get(resource_type, created["id"])["id"] == created["id"]
    assert any(item["id"] == created["id"] for item in store.list(resource_type, user_id))

    if isinstance(store, BasePostgresStore) and "idempotency_key" in store._table_columns(resource_type):
        repeated = store.create(
            resource_type,
            user_id,
            entity_id,
            rule.initial_status,
            payload,
            user_id,
            rule.unique_fields,
            event_for_create(module, resource_type),
            idempotency_key,
        )
        assert repeated["id"] == created["id"]

    if hasattr(store, "update") and not rule.immutable:
        updated_payload = {**payload, "matrix_updated": True}
        updated_status = rule.initial_status if module == "business" else "matrix_updated"
        updated = store.update(created, updated_payload, updated_status, user_id, "matrix_update")
        assert updated["status"] == updated_status

    if hasattr(store, "soft_delete"):
        store.soft_delete(created, user_id)
        assert store.get(resource_type, created["id"]) is None

    metrics = store.metrics()
    assert metrics[0] >= 1
    assert metrics[1] >= 1
    assert metrics[2] >= 1
