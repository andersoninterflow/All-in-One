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

    async def get(self, url: str, *, params: dict[str, Any], timeout: float) -> FakeResponse:
        self.calls.append((url, params))
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
