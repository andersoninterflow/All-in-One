from uuid import uuid4

from platform_test_support import fresh_client_for


def actor_headers(user_id: str, roles: str = "merchant", *, business_id: str | None = None) -> dict[str, str]:
    headers = {"X-Actor-User-Id": user_id, "X-Actor-Roles": roles, "X-Actor-Scopes": ""}
    if business_id:
        headers["X-Business-Id"] = business_id
        headers["X-Business-Status"] = "active"
    return headers


def test_valley_gold_ledger_is_append_only_idempotent_and_emits_event() -> None:
    finance = fresh_client_for("finance")
    merchant_id = str(uuid4())
    business_id = str(uuid4())
    entry_key = f"gold-purchase-{uuid4()}"

    created = finance.post(
        "/resources/valley_gold_ledger_entries",
        headers={**actor_headers(merchant_id, business_id=business_id), "X-Idempotency-Key": entry_key},
        json={
            "user_id": merchant_id,
            "entity_id": business_id,
            "payload": {
                "merchant_business_id": business_id,
                "entry_type": "purchase_credit",
                "amount_gold_delta": 1000,
                "reference_type": "gold_purchase",
                "reference_id": str(uuid4()),
            },
        },
    )
    assert created.status_code == 201
    entry = created.json()
    assert entry["status"] == "posted"
    assert entry["payload"]["amount_gold_delta"] == 1000

    repeated = finance.post(
        "/resources/valley_gold_ledger_entries",
        headers={**actor_headers(merchant_id, business_id=business_id), "X-Idempotency-Key": entry_key},
        json={
            "user_id": merchant_id,
            "entity_id": business_id,
            "payload": {
                "merchant_business_id": business_id,
                "entry_type": "purchase_credit",
                "amount_gold_delta": 1000,
                "reference_type": "gold_purchase",
                "reference_id": str(uuid4()),
            },
        },
    )
    assert repeated.status_code == 201
    assert repeated.json()["id"] == entry["id"]

    patched = finance.patch(
        f"/resources/valley_gold_ledger_entries/{entry['id']}",
        headers=actor_headers(merchant_id, business_id=business_id),
        json={"payload": {"amount_gold_delta": 2000}},
    )
    assert patched.status_code == 409

    deleted = finance.delete(
        f"/resources/valley_gold_ledger_entries/{entry['id']}",
        headers=actor_headers(merchant_id, business_id=business_id),
    )
    assert deleted.status_code == 409

    outbox = finance.get("/events/outbox", headers=actor_headers(merchant_id, "auditor"))
    assert outbox.status_code == 200
    assert any(event["routing_key"] == "valley.gold.ledger.posted" for event in outbox.json())


def test_valley_gold_ledger_blocks_automatic_pepitas_and_invalid_debits() -> None:
    finance = fresh_client_for("finance")
    merchant_id = str(uuid4())
    business_id = str(uuid4())

    automated = finance.post(
        "/resources/valley_gold_ledger_entries",
        headers={
            **actor_headers(merchant_id, business_id=business_id),
            "X-Idempotency-Key": f"gold-auto-{uuid4()}",
        },
        json={
            "user_id": merchant_id,
            "entity_id": business_id,
            "payload": {
                "merchant_business_id": business_id,
                "entry_type": "purchase_credit",
                "amount_gold_delta": 100,
                "reference_type": "gold_purchase",
                "auto_grant_pepitas": True,
            },
        },
    )
    assert automated.status_code == 422

    invalid_debit = finance.post(
        "/resources/valley_gold_ledger_entries",
        headers={
            **actor_headers(merchant_id, business_id=business_id),
            "X-Idempotency-Key": f"gold-debit-{uuid4()}",
        },
        json={
            "user_id": merchant_id,
            "entity_id": business_id,
            "payload": {
                "merchant_business_id": business_id,
                "entry_type": "pepita_grant_debit",
                "amount_gold_delta": 100,
                "reference_type": "pepita_grant",
                "reference_id": str(uuid4()),
            },
        },
    )
    assert invalid_debit.status_code == 422
