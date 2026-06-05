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
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Busca do API Hub central que agrega todos os módulos
    fetch('http://localhost:8100/gateway/catalog/offers?limit=20')
      .then(res => res.json())
      .then(data => {
        if (data.data) {
          setOffers(data.data)
        }
      })
      .catch(err => console.error("API Hub desativado ou sem ofertas", err))
      .finally(() => setLoading(false))
  }, [])

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
                  Aguardando a sincronização de lojistas, profissionais e motoristas (via módulos Business, Riders, etc.) para popular as ofertas.
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
