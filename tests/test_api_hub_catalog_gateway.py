from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from modules.api_hub import main as api_hub


class FakeResponse:
    def __init__(self, status_code: int, payload: Any) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self) -> Any:
        return self._payload


class FakeCatalogClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.posts: list[tuple[str, dict[str, Any], dict[str, str]]] = []

    async def get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        timeout: float,
    ) -> FakeResponse:
        self.calls.append((url, params or {}))
        if "/valley/catalog/offers/" in url:
            return FakeResponse(
                200,
                {
                    "offer_id": "business:catalog_offers:offer-1",
                    "offer_type": "product",
                    "consumer_action": "buy",
                    "title": "Produto Valley",
                    "source_module": "marketplace",
                    "source_resource_type": "products",
                    "source_entity_id": "offer-1",
                    "seller_user_id": "seller-1",
                    "business_id": "store-1",
                    "availability_status": "available",
                    "price_amount": "99.90",
                },
            )
        if url.endswith("business:8000/valley/catalog/search"):
            return FakeResponse(
                200,
                [
                    {
                        "offer_id": "business:catalog_offers:offer-1",
                        "offer_type": "service",
                        "offer_type_label": "Servico",
                        "consumer_category": "Casa, Reparos e Imoveis",
                        "title": "Eletricista residencial",
                        "short_description": "Atendimento eletrico em residencias.",
                        "source_module": "services",
                        "source_resource_type": "providers",
                        "source_entity_id": "offer-1",
                        "availability_status": "available",
                        "service_area": "local",
                        "service_radius_km": 15,
                        "distance_km": 2.4,
                        "company_type": "pf_profissional",
                        "company_type_label": "Profissional autonomo",
                        "company_category": "Servicos",
                        "business_activity_id": "servicos_domesticos",
                        "business_activity_label": "Casa e manutencao",
                        "provider_label": "Profissional verificado",
                        "primary_action_label": "Contratar",
                    },
                    {
                        "offer_id": "module:services",
                        "title": "Servicos",
                        "availability_status": "coming_soon",
                        "service_area": "national",
                    },
                ],
            )
        if url.endswith("services:8000/valley/catalog/search"):
            return FakeResponse(
                200,
                [
                    {
                        "offer_id": "module:services",
                        "title": "Servicos",
                        "availability_status": "coming_soon",
                        "service_area": "national",
                    }
                ],
            )
        return FakeResponse(503, {"detail": "indisponivel"})

    async def post(
        self,
        url: str,
        *,
        headers: dict[str, str],
        json: dict[str, Any],
        timeout: float,
    ) -> FakeResponse:
        self.posts.append((url, json, headers))
        return FakeResponse(201, {"id": "resource-created", "status": "created"})


def test_gateway_aggregates_business_offer_with_consumer_filters(monkeypatch) -> None:
    fake_client = FakeCatalogClient()
    monkeypatch.setattr(api_hub, "client", fake_client)
    monkeypatch.setattr(api_hub, "redis_client", None)
    client = TestClient(api_hub.app)

    response = client.get(
        "/gateway/catalog/offers",
        params={
            "q": "eletricista",
            "category": "Casa, Reparos e Imoveis",
            "offer_type": "service",
            "lat": -23.5505,
            "lng": -46.6333,
            "company_type": "pf_profissional",
            "company_category": "Servicos",
            "business_activity": "servicos_domesticos",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["partial"] is True
    assert payload["total"] == 2
    assert sum(item["offer_id"] == "module:services" for item in payload["data"]) == 1
    assert payload["facets"]["company_types"] == [
        {"id": "pf_profissional", "label": "Profissional autonomo", "count": 1}
    ]
    assert payload["facets"]["company_categories"] == [
        {"id": "Servicos", "label": "Servicos", "count": 1}
    ]
    assert payload["facets"]["business_activities"] == [
        {"id": "servicos_domesticos", "label": "Casa e manutencao", "count": 1}
    ]

    offer = next(item for item in payload["data"] if item["offer_id"] == "business:catalog_offers:offer-1")
    assert offer["title"] == "Eletricista residencial"
    assert offer["source_module"] == "services"
    assert offer["consumer_category"] == "Casa, Reparos e Imoveis"
    assert offer["business_activity_id"] == "servicos_domesticos"

    assert len(fake_client.calls) == len(api_hub.CATALOG_SOURCE_MODULES)
    assert all(url.endswith("/valley/catalog/search") for url, _ in fake_client.calls)
    forwarded = fake_client.calls[0][1]
    assert forwarded["offer_type"] == "service"
    assert forwarded["company_type"] == "pf_profissional"
    assert forwarded["business_activity"] == "servicos_domesticos"


def test_gateway_applies_pagination_after_global_deduplication(monkeypatch) -> None:
    fake_client = FakeCatalogClient()
    monkeypatch.setattr(api_hub, "client", fake_client)
    monkeypatch.setattr(api_hub, "redis_client", None)
    client = TestClient(api_hub.app)

    response = client.get("/gateway/catalog/offers", params={"limit": 1, "offset": 1})

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 2
    assert payload["limit"] == 1
    assert payload["offset"] == 1
    assert len(payload["data"]) == 1


def test_gateway_creates_marketplace_order_from_canonical_offer(monkeypatch) -> None:
    fake_client = FakeCatalogClient()
    monkeypatch.setattr(api_hub, "client", fake_client)
    monkeypatch.setattr(api_hub, "redis_client", None)
    client = TestClient(api_hub.app)
    user_id = "11111111-1111-4111-8111-111111111111"
    token = api_hub.jwt.encode({"sub": user_id}, api_hub.JWT_SECRET, algorithm="HS256")

    response = client.post(
        "/gateway/catalog/actions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "offer_id": "business:catalog_offers:offer-1",
            "action": "buy",
            "customer_user_id": user_id,
            "idempotency_key": "checkout-offer-1",
            "quantity": 2,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "status": "created",
        "action": "buy",
        "target_module": "marketplace",
        "resource_type": "orders",
        "resource_id": "resource-created",
        "next_step": "payment_required",
        "message": "Pedido criado. O pagamento sera confirmado na proxima etapa.",
    }
    assert len(fake_client.posts) == 1
    url, request_body, headers = fake_client.posts[0]
    assert url.endswith("marketplace:8000/resources/orders")
    assert headers["X-Idempotency-Key"] == "checkout-offer-1"
    assert request_body["payload"]["total_brl"] == "99.90"
    assert request_body["payload"]["store_id"] == "store-1"
    assert request_body["payload"]["items"][0]["quantity"] == 2


def test_gateway_rejects_action_different_from_published_offer(monkeypatch) -> None:
    fake_client = FakeCatalogClient()
    monkeypatch.setattr(api_hub, "client", fake_client)
    monkeypatch.setattr(api_hub, "redis_client", None)
    client = TestClient(api_hub.app)
    user_id = "11111111-1111-4111-8111-111111111111"
    token = api_hub.jwt.encode({"sub": user_id}, api_hub.JWT_SECRET, algorithm="HS256")

    response = client.post(
        "/gateway/catalog/actions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "offer_id": "business:catalog_offers:offer-1",
            "action": "hire",
            "customer_user_id": user_id,
            "idempotency_key": "checkout-offer-1",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "A acao solicitada nao corresponde a esta oferta."
