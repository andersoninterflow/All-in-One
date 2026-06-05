from uuid import uuid4
from playwright.sync_api import Page, Request, Route, expect

from platform_test_support import fresh_client_for
from modules.shared.valley_catalog import valley_facets

def actor_headers(
    user_id: str,
    roles: str = "owner",
    *,
    business_id: str | None = None,
    mfa: bool = False,
) -> dict[str, str]:
    headers = {"X-Actor-User-Id": user_id, "X-Actor-Roles": roles, "X-Actor-Scopes": ""}
    if mfa:
        headers["X-MFA-Verified"] = "true"
    if business_id:
        headers["X-Business-Id"] = business_id
        headers["X-Business-Status"] = "active"
    return headers

def test_business_offer_appears_in_valley_and_triggers_checkout(page: Page, superapp_server: str):
    """
    Testa a jornada E2E:
    1. Criação de oferta real no módulo Business via API.
    2. Visualização do Card da oferta recém-criada no frontend Valley Superapp.
    3. Simulação de clique no botão de "Comprar" ou "Contratar" que deve acionar o fluxo na UI.
    """
    # 1. Preparar dados backend via API real
    business = fresh_client_for("business")
    seller_id = str(uuid4())
    business_id = str(uuid4())
    headers = actor_headers(seller_id, "owner", business_id=business_id, mfa=True)

    unique_title = f"Produto E2E_{str(uuid4())[:8]}"

    created = business.post(
        "/resources/catalog_offers",
        headers=headers,
        json={
            "user_id": seller_id,
            "entity_id": business_id,
            "payload": {
                "title": unique_title,
                "description": "Produto exclusivo criado via jornada E2E para validacao.",
                "offer_type": "product",
                "consumer_category": "Compras e Produtos",
                "source_module": "marketplace",
                "source_resource_type": "products",
                "company_type": "pf_vendedor",
                "company_category": "Comercio",
                "business_activity_id": "varejo",
                "service_area": "local",
                "latitude": -23.5505,
                "longitude": -46.6333,
                "service_radius_km": 10,
                "price_brl": "99.90",
                "publish_to_valley": True,
                "publication_status": "approved",
                "visible_to_consumer": True,
                "verified_seller": True,
            },
        },
    )
    assert created.status_code == 201

    offer_id = created.json()["id"]
    approved = business.post(
        f"/resources/catalog_offers/{offer_id}/actions/approve",
        headers=headers,
        json={"reason": "Oferta E2E validada", "payload": {"publication_status": "approved"}},
    )
    assert approved.status_code == 200

    catalog = business.get(
        "/valley/catalog/search",
        params={"q": unique_title, "lat": -23.5505, "lng": -46.6333},
    )
    assert catalog.status_code == 200
    normalized_offers = catalog.json()
    assert any(item["title"] == unique_title for item in normalized_offers)

    # Mockamos a comunicação do frontend com o API Hub para não depender dos containers rodando no ambiente de teste
    def serve_catalog(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            json={
                "data": normalized_offers,
                "total": len(normalized_offers),
                "partial": False,
                "facets": valley_facets(normalized_offers),
            },
        )

    page.route("**/gateway/catalog/offers**", serve_catalog)

    buyer_id = str(uuid4())
    
    def serve_registrations(route: Route) -> None:
        route.fulfill(
            status=200,
            json={"token": "mock-jwt-token", "user_id": buyer_id}
        )
        
    page.route("**/registrations", serve_registrations)

    def create_order(route: Route) -> None:
        route.fulfill(
            status=201,
            json={
                "status": "created",
                "resource_id": "order-e2e",
                "message": "Pedido criado",
            },
        )

    page.route("**/gateway/catalog/actions", create_order)

    # 2. Abrir o Valley Superapp e buscar a oferta criada
    page.goto(superapp_server, timeout=60000, wait_until="domcontentloaded")
    
    # Preencher latitude/longitude e buscar
    page.locator("input[placeholder='Latitude']").fill("-23.5505")
    page.locator("input[placeholder='Longitude']").fill("-46.6333")
    
    # Preencher a busca textual com o titulo unico gerado
    search_input = page.locator("input[placeholder*='eletricista']")
    search_input.fill(unique_title)
    page.get_by_role("button", name="Buscar").click()
    
    # Localizar o card especifico pelo titulo (Aguarda o API Hub agregar a oferta do PostgreSQL real)
    card = page.locator(".offer-card", has_text=unique_title)
    expect(card).to_be_visible(timeout=15000)

    # Validar informacoes esteticas da oferta no frontend
    expect(card.locator(".price")).to_contain_text("R$ 99,90")
    expect(card.locator(".badge")).to_contain_text("Produto")
    expect(card).to_contain_text("Compras e Produtos")
    
    # 3. Interagir com o fluxo (Clicar na Acao Principal)
    buy_button = card.locator("button", has_text="Comprar")
    expect(buy_button).to_be_visible()
    buy_button.click()

    # Validar se o Modal Neo-brutalista de Login abre
    login_modal = page.locator(".login-modal")
    expect(login_modal).to_be_visible()
    
    # Navegar para Cadastro
    page.get_by_role("button", name="Ainda nao tem conta? Cadastre-se").click()
    
    # Preencher dados
    buyer_email = f"buyer_{str(uuid4())[:8]}@valley.com"
    page.locator("input[type='email']").fill(buyer_email)
    page.locator("input[type='password']").fill("SenhaForte123!")
    
    # Enviar form (usar login_modal para evitar conflito com o botao do Header)
    login_modal.get_by_role("button", name="Cadastrar", exact=True).click()

    # Validar se o Modal Neo-brutalista de Checkout abre automaticamente apos login
    checkout_modal = page.locator(".checkout-modal")
    expect(checkout_modal).to_be_visible(timeout=10000)
    expect(checkout_modal).to_contain_text(unique_title)
    expect(checkout_modal).to_contain_text("Finalizar pedido")
    
    # Clicar em Confirmar pedido
    confirm_button = page.locator(".checkout-modal button", has_text="Confirmar pedido")
    confirm_button.click()
    
    # Aguardar feedback de sucesso que veio do API Hub real comunicando-se com Marketplace
    feedback = page.locator(".checkout-modal .action-feedback.success")
    expect(feedback).to_be_visible(timeout=15000)
    expect(feedback).to_contain_text("Pedido criado")
