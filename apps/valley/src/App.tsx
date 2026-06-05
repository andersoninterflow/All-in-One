import { useEffect, useState } from 'react'
import './index.css'

interface Offer {
  id: string
  title: string
  description: string
  price?: number
  category: string
  _source_module: string
}

function App() {
  const [offers, setOffers] = useState<Offer[]>([])
  const [loading, setLoading] = useState(false)

  // Filtros Regionais
  const [lat, setLat] = useState<string>('-23.5505') // São Paulo base
  const [lng, setLng] = useState<string>('-46.6333')
  const [radiusKm, setRadiusKm] = useState<number>(10)
  
  // Categorias (taxonomia amigável do Valley)
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)

  const categories = [
    { id: 'food', label: '🍔 Alimentação' },
    { id: 'product', label: '🛍️ Produtos' },
    { id: 'service', label: '🛠️ Serviços' },
    { id: 'mobility', label: '🚗 Mobilidade' },
    { id: 'health', label: '⚕️ Saúde' },
  ]

  const fetchOffers = () => {
    setLoading(true)
    // Constrói URL dinamicamente
    const params = new URLSearchParams()
    params.append('limit', '20')
    if (lat && lng) {
      params.append('lat', lat)
      params.append('lng', lng)
      params.append('radius_km', radiusKm.toString())
    }
    if (selectedCategory) {
      params.append('category', selectedCategory)
    }

    fetch(`http://localhost:8100/gateway/catalog/offers?${params.toString()}`)
      .then(res => res.json())
      .then(data => {
        if (data.data) {
          setOffers(data.data)
        }
      })
      .catch(err => console.error("API Hub desativado ou sem ofertas", err))
      .finally(() => setLoading(false))
  }

  // Effect inicial
  useEffect(() => {
    fetchOffers()
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCategory])

  return (
    <>
      <header>
        <div className="logo">Valley</div>
        <nav>
          <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Marketplace Global Integrado</span>
        </nav>
      </header>
      
      <main className="container">
        <section className="hero">
          <h1>Tudo o que você precisa,<br/>em um só lugar.</h1>
          <p>Explore produtos, serviços, vagas e mobilidade no ecossistema definitivo All-in-One.</p>
        </section>

        <section className="filters-section">
          <div className="filters-row">
            <div className="filter-group">
              <label>Sua Localização:</label>
              <input type="text" value={lat} onChange={(e) => setLat(e.target.value)} placeholder="Lat" style={{ width: '100px' }} />
              <input type="text" value={lng} onChange={(e) => setLng(e.target.value)} placeholder="Lng" style={{ width: '100px' }} />
            </div>
            <div className="filter-group">
              <label>Raio (km):</label>
              <select value={radiusKm} onChange={(e) => setRadiusKm(Number(e.target.value))}>
                <option value={5}>5 km</option>
                <option value={10}>10 km</option>
                <option value={20}>20 km</option>
                <option value={50}>50 km</option>
                <option value={100}>100 km (Global)</option>
              </select>
            </div>
            <button className="btn-primary" onClick={fetchOffers}>Buscar</button>
          </div>

          <div className="pills-container">
            <div 
              className={`pill ${selectedCategory === null ? 'active' : ''}`}
              onClick={() => setSelectedCategory(null)}
            >
              🌟 Todos
            </div>
            {categories.map(cat => (
              <div 
                key={cat.id}
                className={`pill ${selectedCategory === cat.id ? 'active' : ''}`}
                onClick={() => setSelectedCategory(cat.id)}
              >
                {cat.label}
              </div>
            ))}
          </div>
        </section>

        {loading ? (
          <div className="loader"></div>
        ) : (
          <div className="offers-grid">
            {offers.length > 0 ? offers.map((offer, idx) => (
              <div className="offer-card" key={offer.id || idx}>
                <div className="offer-title">{offer.title}</div>
                <div className="offer-desc">{offer.description || "Nenhuma descrição fornecida."}</div>
                <div className="offer-meta">
                  <span className="badge">{offer.category || offer._source_module}</span>
                  <span className="price">{offer.price ? `R$ ${offer.price.toFixed(2)}` : 'Sob orçamento'}</span>
                </div>
              </div>
            )) : (
              <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '4rem', color: 'var(--text-muted)' }}>
                <h3>A Vitrine está em construção</h3>
                <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>
                  Aguardando a sincronização de lojistas, profissionais e motoristas (via módulos Business, Riders, etc.) para popular as ofertas na sua região.
                </p>
              </div>
            )}
          </div>
        )}
      </main>

    </>
  )
}

export default App
