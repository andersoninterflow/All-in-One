from uuid import uuid4

from platform_test_support import fresh_client_for


def headers(user_id: str) -> dict[str, str]:
    return {"X-Actor-User-Id": user_id, "X-Actor-Roles": "auditor"}


def test_marketplace_opens_support_case_from_paid_order_and_exports_metrics() -> None:
    marketplace = fresh_client_for("marketplace")
    user_id = str(uuid4())
    store_id = str(uuid4())

    order = marketplace.post(
        "/resources/orders",
        headers={**headers(user_id), "X-Idempotency-Key": f"order-{uuid4().hex}"},
        json={
            "user_id": user_id,
            "entity_id": store_id,
            "payload": {
                "store_id": str(store_id),
                "total_brl": "99.90",
            },
        },
    )
    assert order.status_code == 201

    paid = marketplace.post(
        f"/resources/orders/{order.json()['id']}/actions/pay",
        headers=headers(user_id),
        json={"reason": "pagamento confirmado"},
    )
    assert paid.status_code == 200

    support = marketplace.post(
        f"/valley/orders/{order.json()['id']}/support",
        headers={**headers(user_id), "X-Idempotency-Key": f"support-{uuid4().hex}"},
        json={
            "kind": "dispute",
            "subject": "Atraso na entrega",
            "message": "Preciso de uma resposta sobre o pedido.",
            "desired_resolution": "Reembolso ou reenvio.",
            "idempotency_key": f"support-body-{uuid4().hex}",
        },
    )
    assert support.status_code == 201
    assert support.json()["kind"] == "dispute"

    review = marketplace.post(
        "/resources/reviews",
        headers={**headers(user_id), "X-Idempotency-Key": f"review-{uuid4().hex}"},
        json={
            "user_id": user_id,
            "payload": {
                "order_id": order.json()["id"],
                "rating": 5,
                "comment": "Tudo certo.",
            },
        },
    )
    assert review.status_code == 201

    insights = marketplace.get("/valley/insights/commercial", headers=headers(user_id))
    assert insights.status_code == 200
    payload = insights.json()
    assert payload["orders_total"] == 1
    assert payload["support_cases_total"] == 1
    assert payload["reviews_total"] == 1
    assert payload["average_rating"] == 5.0
