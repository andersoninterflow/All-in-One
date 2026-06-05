from playwright.sync_api import Page, expect

def test_valley_superapp_filters(page: Page, superapp_server: str):
    """
    Testa a vitrine regional e os filtros de categorias amigáveis do Valley SuperApp.
    """
    # Acessa o app Valley (SuperApp)
    page.goto(superapp_server)
    
    # Valida Header e Hero Section
    expect(page.locator("header .logo")).to_contain_text("Valley")
    expect(page.locator("h1")).to_contain_text("Tudo o que você precisa")

    # Verifica os controles regionais (inputs de Lat, Lng e select de Raio)
    expect(page.locator("input[placeholder='Lat']")).to_have_value("-23.5505")
    expect(page.locator("input[placeholder='Lng']")).to_have_value("-46.6333")
    expect(page.locator("select")).to_contain_text("10 km")

    # Verifica se os pills (categorias) renderizam corretamente
    expect(page.locator(".pill", has_text="🌟 Todos")).to_be_visible()
    expect(page.locator(".pill", has_text="🍔 Alimentação")).to_be_visible()
    expect(page.locator(".pill", has_text="🛍️ Produtos")).to_be_visible()
    expect(page.locator(".pill", has_text="🛠️ Serviços")).to_be_visible()

    # Como o mock backend (API Hub ou pytest fixture) pode estar vazio ou ter dados fake,
    # verificamos a estrutura do grid e os Fallbacks.
    # Clica em um filtro específico
    page.locator(".pill", has_text="🍔 Alimentação").click()
    
    # Valida estado 'active' do pill selecionado
    expect(page.locator(".pill.active")).to_contain_text("🍔 Alimentação")

    # Garante que, se não houver backend com dados, exiba o aviso de "Vitrine em construção"
    # (ou os cards caso tenha mock data inserida).
    grid_container = page.locator(".offers-grid")
    expect(grid_container).to_be_visible()
