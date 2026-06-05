import { useEffect, useState } from 'react'
import './index.css'

interface Offer {
  offer_id: string
  title: string
  short_description?: string
  description?: string
  price_amount?: string | null
  price_type: string
  consumer_category: string
  offer_type: 'food' | 'product' | 'service'
  offer_type_label: string
  source_module: string
  provider_label: string
  region_label: string
  distance_km?: number | null
  primary_action_label: string
  verified_seller: boolean
}

interface CatalogResponse {
  data: Offer[]
  total: number
  partial: boolean
}

const API_HUB_URL = import.meta.env.VITE_API_HUB_URL ?? ''

function App() {
  const [offers, setOffers] = useState<Offer[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [query, setQuery] = useState('')

  const [lat, setLat] = useState<string>('-23.5505')
  const [lng, setLng] = useState<string>('-46.6333')
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [selectedType, setSelectedType] = useState<string | null>(null)

  const categories = [
    'Comida e Mercado',
    'Compras e Produtos',
    'Saude e Bem-estar',
    'Casa, Reparos e Imoveis',
    'Mobilidade, Entregas e Logistica',
    'Negocios e Profissionais',
  ]

  const fetchOffers = () => {
    setLoading(true)
    setError('')
    const params = new URLSearchParams()
    params.append('limit', '50')
    if (lat && lng) {
      params.append('lat', lat)
      params.append('lng', lng)
    }
    if (query.trim()) params.append('q', query.trim())
    if (selectedCategory) {
      params.append('category', selectedCategory)
    }
    if (selectedType) params.append('offer_type', selectedType)

    fetch(`${API_HUB_URL}/gateway/catalog/offers?${params.toString()}`)
      .then(async res => {
        if (!res.ok) throw new Error(`Falha HTTP ${res.status}`)
        return res.json() as Promise<CatalogResponse>
      })
      .then(data => {
        setOffers(data.data ?? [])
        if (data.partial) setError('Algumas fontes estao temporariamente indisponiveis.')
      })
      .catch(() => {
        setOffers([])
        setError('Nao foi possivel carregar as ofertas agora.')
      })
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchOffers()
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCategory, selectedType])

  return (
    <>
      <header>
        <div className="logo">Valley</div>
        <nav>
          <span>Ofertas perto de voce</span>
        </nav>
      </header>
      
      <main className="container">
        <section className="hero">
          <h1>Encontre o que precisa</h1>
          <p>Produtos, alimentos e servicos organizados de um jeito simples.</p>
        </section>

        <section className="filters-section">
          <form className="search-row" onSubmit={(event) => { event.preventDefault(); fetchOffers() }}>
            <label className="search-field">
              <span>O que voce procura?</span>
              <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Ex.: eletricista, marmita, psicologo" />
            </label>
            <button className="btn-primary" type="submit">Buscar</button>
          </form>

          <div className="type-filter" aria-label="Tipo de oferta">
            {[
              { id: null, label: 'Tudo' },
              { id: 'food', label: 'Alimentos' },
              { id: 'product', label: 'Produtos' },
              { id: 'service', label: 'Servicos' },
            ].map(type => (
              <button
                type="button"
                key={type.label}
                className={selectedType === type.id ? 'active' : ''}
                onClick={() => setSelectedType(type.id)}
              >
                {type.label}
              </button>
            ))}
          </div>

          <div className="filters-row">
            <div className="filter-group">
              <label htmlFor="latitude">Sua localizacao</label>
              <input id="latitude" type="text" value={lat} onChange={(e) => setLat(e.target.value)} placeholder="Latitude" />
              <input type="text" value={lng} onChange={(e) => setLng(e.target.value)} placeholder="Longitude" />
            </div>
            <button className="btn-secondary" onClick={fetchOffers}>Atualizar regiao</button>
          </div>

          <div className="pills-container">
            <button
              type="button"
              className={`pill ${selectedCategory === null ? 'active' : ''}`}
              onClick={() => setSelectedCategory(null)}
            >
              Todas as categorias
            </button>
            {categories.map(category => (
              <button
                type="button"
                key={category}
                className={`pill ${selectedCategory === category ? 'active' : ''}`}
                onClick={() => setSelectedCategory(category)}
              >
                {category}
              </button>
            ))}
          </div>
        </section>

        {error && <p className="notice" role="status">{error}</p>}

        {loading ? (
          <div className="loader" aria-label="Carregando ofertas"></div>
        ) : (
          <div className="offers-grid">
            {offers.length > 0 ? offers.map((offer) => (
              <article className="offer-card" key={offer.offer_id}>
                <div className="offer-tags">
                  <span className="badge">{offer.offer_type_label}</span>
                  <span>{offer.consumer_category}</span>
                </div>
                <div className="offer-title">{offer.title}</div>
                <div className="offer-desc">{offer.short_description || offer.description}</div>
                <div className="provider">
                  {offer.provider_label}{offer.verified_seller ? ' - verificado' : ''}
                </div>
                <div className="region">
                  {offer.distance_km != null ? `${offer.distance_km.toFixed(1)} km - ` : ''}{offer.region_label}
                </div>
                <div className="offer-meta">
                  <span className="price">
                    {offer.price_amount ? `R$ ${Number(offer.price_amount).toFixed(2).replace('.', ',')}` : 'Sob orcamento'}
                  </span>
                  <button className="offer-action">{offer.primary_action_label}</button>
                </div>
              </article>
            )) : (
              <div className="empty-state">
                <h2>Nenhuma oferta encontrada</h2>
                <p>Tente outra categoria, busca ou localizacao.</p>
              </div>
            )}
          </div>
        )}
      </main>

    </>
  )
}

export default App
