from datetime import datetime, timezone
from uuid import uuid4

from modules.shared.outbox_dispatcher import publication_message


def test_jobs_document_publication_uses_safe_allowlist() -> None:
    message = publication_message(
        {
            "id": uuid4(),
            "routing_key": "jobs.resume.ctps_imported",
            "schema_version": 1,
            "aggregate_type": "resume_documents",
            "aggregate_id": uuid4(),
            "correlation_id": uuid4(),
            "entity_id": None,
            "created_at": datetime.now(timezone.utc),
            "payload": {
                "resume_id": str(uuid4()),
                "document_type": "ctps_digital_pdf",
                "sha256": "hash",
                "storage_key": "private-key",
                "raw_document_text": "private text",
            },
        }
    )
    assert message["payload"]["sha256"] == "hash"
    assert "storage_key" not in message["payload"]
    assert "raw_document_text" not in message["payload"]


def test_unknown_domain_publishes_no_unreviewed_payload() -> None:
    message = publication_message(
        {
            "id": uuid4(),
            "routing_key": "health.record.created",
            "schema_version": 1,
            "aggregate_type": "medical_records",
            "aggregate_id": uuid4(),
            "correlation_id": uuid4(),
            "entity_id": None,
            "created_at": datetime.now(timezone.utc),
            "payload": {"patient_record": "must not publish"},
        }
    )
    assert message["payload"] == {}


def test_valley_pepita_publication_notifies_consumer_with_safe_payload() -> None:
    customer_id = str(uuid4())
    message = publication_message(
        {
            "id": uuid4(),
            "routing_key": "valley.pepitas.granted",
            "schema_version": 1,
            "aggregate_type": "pepita_grants",
            "aggregate_id": uuid4(),
            "correlation_id": uuid4(),
            "entity_id": uuid4(),
            "created_at": datetime.now(timezone.utc),
            "payload": {
                "order_id": str(uuid4()),
                "customer_user_id": customer_id,
                "merchant_business_id": str(uuid4()),
                "merchant_actor_user_id": str(uuid4()),
                "pepitas": 100,
                "merchant_gold_ledger_id": "gold-private-ledger",
                "grant_mode": "merchant_manual_free_will",
                "note": "private merchant note",
            },
        }
    )
    assert message["routing_key"] == "valley.pepitas.granted"
    assert message["payload"]["customer_user_id"] == customer_id
    assert message["payload"]["pepitas"] == 100
    assert message["payload"]["grant_mode"] == "merchant_manual_free_will"
    assert "merchant_gold_ledger_id" not in message["payload"]
    assert "note" not in message["payload"]


def test_valley_discount_publication_uses_progressive_discount_allowlist() -> None:
    message = publication_message(
        {
            "id": uuid4(),
            "routing_key": "valley.stock.discount.quoted",
            "schema_version": 1,
            "aggregate_type": "discount_quotes",
            "aggregate_id": uuid4(),
            "correlation_id": uuid4(),
            "entity_id": None,
            "created_at": datetime.now(timezone.utc),
            "payload": {
                "catalog_product_id": "stock-checkout",
                "selected_percent": 50,
                "pepitas_required": 500,
                "original_price_brl": "200.00",
                "discount_brl": "100.00",
                "final_price_brl": "100.00",
                "visibility_rule": "BR-STO-009",
                "internal_margin_brl": "must-not-publish",
            },
        }
    )
    assert message["payload"]["selected_percent"] == 50
    assert message["payload"]["pepitas_required"] == 500
    assert message["payload"]["final_price_brl"] == "100.00"
    assert "original_price_brl" not in message["payload"]
    assert "internal_margin_brl" not in message["payload"]
