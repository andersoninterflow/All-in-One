from datetime import datetime, timezone
from uuid import uuid4

from modules.shared.outbox_dispatcher import OutboxMetrics, OutboxSettings, prometheus_metrics, publication_message, retry_observation


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


def test_valley_gold_ledger_publication_uses_safe_payload() -> None:
    message = publication_message(
        {
            "id": uuid4(),
            "routing_key": "valley.gold.ledger.posted",
            "schema_version": 1,
            "aggregate_type": "valley_gold_ledger_entries",
            "aggregate_id": uuid4(),
            "correlation_id": uuid4(),
            "entity_id": uuid4(),
            "created_at": datetime.now(timezone.utc),
            "payload": {
                "merchant_business_id": str(uuid4()),
                "entry_type": "pepita_grant_debit",
                "amount_gold_delta": -100,
                "reference_type": "pepita_grant",
                "reference_id": str(uuid4()),
                "processor_fee_brl": "private",
                "internal_note": "must-not-publish",
            },
        }
    )
    assert message["routing_key"] == "valley.gold.ledger.posted"
    assert message["payload"]["entry_type"] == "pepita_grant_debit"
    assert message["payload"]["amount_gold_delta"] == -100
    assert "processor_fee_brl" not in message["payload"]
    assert "internal_note" not in message["payload"]


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


def test_valley_catalog_publication_uses_safe_payload() -> None:
    message = publication_message(
        {
            "id": uuid4(),
            "routing_key": "valley.catalog.offer.synced",
            "schema_version": 1,
            "aggregate_type": "valley_catalog_offers",
            "aggregate_id": uuid4(),
            "correlation_id": uuid4(),
            "entity_id": None,
            "created_at": datetime.now(timezone.utc),
            "payload": {
                "offer_id": "marketplace:products:123",
                "offer_type": "food",
                "consumer_category": "Comida e Mercado",
                "title": "Marmita local",
                "source_module": "marketplace",
                "source_resource_type": "products",
                "availability_status": "available",
                "price_brl": "29.90",
                "benefits": ["entrega regional"],
                "rewards": ["Pepitas"],
                "region_label": "Centro",
                "service_radius_km": 5,
                "consumer_action": "buy",
                "internal_margin_brl": "private",
                "supplier_cost_brl": "private",
                "street_address": "must-not-publish",
            },
        }
    )
    assert message["routing_key"] == "valley.catalog.offer.synced"
    assert message["payload"]["offer_type"] == "food"
    assert message["payload"]["consumer_category"] == "Comida e Mercado"
    assert message["payload"]["service_radius_km"] == 5
    assert "internal_margin_brl" not in message["payload"]
    assert "supplier_cost_brl" not in message["payload"]
    assert "street_address" not in message["payload"]


def test_retention_decision_publication_uses_safe_payload() -> None:
    message = publication_message(
        {
            "id": uuid4(),
            "routing_key": "compliance.data.anonymized",
            "schema_version": 1,
            "aggregate_type": "retention_decisions",
            "aggregate_id": uuid4(),
            "correlation_id": uuid4(),
            "entity_id": None,
            "created_at": datetime.now(timezone.utc),
            "payload": {
                "candidate_id": str(uuid4()),
                "module": "crm",
                "resource_type": "leads",
                "action": "delete_or_anonymize_opted_out_leads",
                "decision_status": "applied",
                "job_name": "anonymization_worker_hourly",
                "evidence": {"record_selector_hash": "hash", "policy_version": "2026-05-31"},
                "payload": {"email": "must-not-publish"},
                "raw_before": {"name": "private"},
            },
        }
    )
    assert message["payload"]["module"] == "crm"
    assert message["payload"]["decision_status"] == "applied"
    assert message["payload"]["evidence"]["record_selector_hash"] == "hash"
    assert "payload" not in message["payload"]
    assert "raw_before" not in message["payload"]


def test_retry_observation_uses_exponential_backoff_with_cap() -> None:
    settings = OutboxSettings(
        postgres_dsn="postgresql://example",
        rabbitmq_url="amqp://example",
        retry_base_seconds=10,
        retry_max_seconds=45,
    )
    now = datetime(2026, 5, 31, 12, 0, tzinfo=timezone.utc)

    first = retry_observation({"metadata": {}}, RuntimeError("broker offline"), settings, now)
    assert first["retry_count"] == 1
    assert first["retry_delay_seconds"] == 10
    assert first["next_retry_at"] == "2026-05-31T12:00:10+00:00"
    assert first["last_error_type"] == "RuntimeError"
    assert first["retryable"] is True

    capped = retry_observation({"metadata": {"retry_count": 4}}, RuntimeError("still offline"), settings, now)
    assert capped["retry_count"] == 5
    assert capped["retry_delay_seconds"] == 45
    assert capped["next_retry_at"] == "2026-05-31T12:00:45+00:00"


def test_retry_observation_truncates_error_for_metadata() -> None:
    settings = OutboxSettings(postgres_dsn="postgresql://example", rabbitmq_url="amqp://example")
    long_error = RuntimeError("x" * 600)

    metadata = retry_observation({"metadata": {"retry_count": 1}}, long_error, settings)

    assert metadata["retry_count"] == 2
    assert len(metadata["last_error"]) == 500


def test_prometheus_metrics_exposes_outbox_operational_signals() -> None:
    text = prometheus_metrics(
        OutboxMetrics(
            pending=7,
            due=3,
            published=11,
            failed_retryable=2,
            max_retry_count=5,
            oldest_pending_age_seconds=42.5,
        )
    )

    assert "all_in_one_outbox_pending 7\n" in text
    assert "all_in_one_outbox_due 3\n" in text
    assert "all_in_one_outbox_published_total 11\n" in text
    assert "all_in_one_outbox_failed_retryable_total 2\n" in text
    assert "all_in_one_outbox_max_retry_count 5\n" in text
    assert "all_in_one_outbox_oldest_pending_age_seconds 42.5\n" in text
