from uuid import uuid4

from platform_test_support import fresh_client_for


def actor_headers(user_id: str, roles: str = "owner", *, business_id: str | None = None) -> dict[str, str]:
    headers = {"X-Actor-User-Id": user_id, "X-Actor-Roles": roles, "X-Actor-Scopes": ""}
    if business_id:
        headers["X-Business-Id"] = business_id
        headers["X-Business-Status"] = "active"
    return headers


def test_valley_catalog_lists_all_modules_with_simple_categories() -> None:
    marketplace = fresh_client_for("marketplace")

    modules = marketplace.get("/valley/catalog/modules")
    assert modules.status_code == 200
    payload = modules.json()
    assert len(payload) == 25
    assert {item["source_module"] for item in payload} >= {"health", "services", "marketplace", "delivery"}
    assert {item["consumer_category"] for item in payload} >= {
        "Saude e Bem-estar",
        "Casa, Reparos e Imoveis",
        "Comida e Mercado",
    }
    assert all(item["consumer_title"] != item["source_module"] for item in payload)

    offers = marketplace.get("/valley/catalog/offers")
    assert offers.status_code == 200
    source_modules = {item["source_module"] for item in offers.json()}
    assert len(source_modules) == 25
    assert all(item["offer_type"] in {"food", "product", "service"} for item in offers.json())


def test_valley_catalog_search_filters_food_product_service_and_radius() -> None:
    marketplace = fresh_client_for("marketplace")
    merchant_id = str(uuid4())
    business_id = str(uuid4())

    near_food = marketplace.post(
        "/resources/products",
        headers=actor_headers(merchant_id, "merchant", business_id=business_id),
        json={
            "user_id": merchant_id,
            "entity_id": business_id,
            "payload": {
                "store_id": "store-food",
                "sku": "FOOD-ALPHA",
                "name": "Marmita local",
                "description": "Alimento pronto para entrega regional",
                "price_brl": "29.90",
                "stock_location_type": "local_physical",
                "stock_quantity": 10,
                "offer_type": "food",
                "consumer_category": "Comida e Mercado",
                "service_area": "local",
                "service_radius_km": 5,
                "latitude": -23.5505,
                "longitude": -46.6333,
                "region_label": "Centro de Sao Paulo",
                "rewards": ["Pepitas"],
            },
        },
    )
    assert near_food.status_code == 201

    far_food = marketplace.post(
        "/resources/products",
        headers=actor_headers(merchant_id, "merchant", business_id=business_id),
        json={
            "user_id": merchant_id,
            "entity_id": business_id,
            "payload": {
                "store_id": "store-food",
                "sku": "FOOD-BETA",
                "name": "Marmita fora do raio",
                "description": "Alimento longe do usuario",
                "price_brl": "32.90",
                "stock_location_type": "local_physical",
                "stock_quantity": 10,
                "offer_type": "food",
                "consumer_category": "Comida e Mercado",
                "service_area": "local",
                "service_radius_km": 2,
                "latitude": -22.9068,
                "longitude": -43.1729,
                "region_label": "Rio de Janeiro",
            },
        },
    )
    assert far_food.status_code == 201

    online_product = marketplace.post(
        "/resources/products",
        headers=actor_headers(merchant_id, "merchant", business_id=business_id),
        json={
            "user_id": merchant_id,
            "entity_id": business_id,
            "payload": {
                "store_id": "store-digital",
                "sku": "DIGITAL-ALPHA",
                "name": "Curso digital",
                "description": "Produto digital disponivel online",
                "price_brl": "49.90",
                "stock_location_type": "local_physical",
                "stock_quantity": 99,
                "offer_type": "product",
                "consumer_category": "Compras e Produtos",
                "service_area": "online",
                "region_label": "Online",
            },
        },
    )
    assert online_product.status_code == 201

    local_without_radius = marketplace.post(
        "/resources/products",
        headers=actor_headers(merchant_id, "merchant", business_id=business_id),
        json={
            "user_id": merchant_id,
            "entity_id": business_id,
            "payload": {
                "store_id": "store-local",
                "sku": "LOCAL-NO-RADIUS",
                "name": "Produto local incompleto",
                "description": "Produto local sem raio cadastrado",
                "price_brl": "19.90",
                "stock_location_type": "local_physical",
                "stock_quantity": 3,
                "offer_type": "product",
                "consumer_category": "Compras e Produtos",
                "service_area": "local",
                "latitude": -23.5505,
                "longitude": -46.6333,
            },
        },
    )
    assert local_without_radius.status_code == 201

    food_results = marketplace.get(
        "/valley/catalog/search",
        params={"offer_type": "food", "lat": -23.551, "lng": -46.634},
    )
    assert food_results.status_code == 200
    titles = [item["title"] for item in food_results.json()]
    assert "Marmita local" in titles
    assert "Marmita fora do raio" not in titles
    assert all(item["offer_type"] == "food" for item in food_results.json())
    local_offer = next(item for item in food_results.json() if item["title"] == "Marmita local")
    assert local_offer["distance_km"] is not None
    assert local_offer["distance_km"] <= local_offer["service_radius_km"]

    product_results = marketplace.get(
        "/valley/catalog/search",
        params={"offer_type": "product", "lat": -23.551, "lng": -46.634},
    )
    product_titles = [item["title"] for item in product_results.json()]
    assert "Curso digital" in product_titles
    assert "Produto local incompleto" not in product_titles


def test_valley_catalog_groups_repair_health_and_food_in_plain_language() -> None:
    services = fresh_client_for("services")
    provider_id = str(uuid4())

    provider = services.post(
        "/resources/providers",
        headers=actor_headers(provider_id),
        json={
            "user_id": provider_id,
            "payload": {
                "category": "eletricista residencial",
                "public_title": "Eletricista residencial",
                "public_description": "Reparos eletricos para casas e apartamentos",
                "offer_type": "service",
                "consumer_category": "Casa, Reparos e Imoveis",
                "service_radius_km": 12,
                "latitude": -23.5505,
                "longitude": -46.6333,
                "region_label": "Sao Paulo",
            },
        },
    )
    assert provider.status_code == 201

    repairs = services.get(
        "/valley/catalog/search",
        params={"category": "Casa", "lat": -23.551, "lng": -46.634},
    )
    assert repairs.status_code == 200
    assert any(item["title"] == "Eletricista residencial" for item in repairs.json())
    assert any(item["source_module"] == "property" for item in repairs.json())

    health = services.get("/valley/catalog/search", params={"category": "Saude"})
    assert health.status_code == 200
    assert any(item["source_module"] == "health" for item in health.json())
    assert all("consumer_category" in item for item in health.json())
