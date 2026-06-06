import React, { useEffect, useState } from 'react'
import ReviewModal from './ReviewModal'

interface OrderItem {
  id: string
  kind: 'order' | 'appointment' | 'service'
  title: string
  status: string
  amount_brl?: string | null
  scheduled_at?: string | null
  created_at?: string
}

interface OrdersDrawerProps {
  isOpen: boolean
  onClose: () => void
  token: string | null
}

const API_HUB_URL = import.meta.env.VITE_API_HUB_URL ?? ''

const statusMap: Record<string, string> = {
  created: 'Aguardando pagamento',
  awaiting_payment: 'Aguardando pagamento',
  paid: 'Pagamento aprovado',
  accepted: 'Pedido aceito',
  in_progress: 'Em andamento',
  delivered: 'Entregue',
  completed: 'Concluido',
  cancelled: 'Cancelado',
  refunded: 'Reembolsado',
  disputed: 'Em disputa',
}

const OrdersDrawerContent: React.FC<{ onClose: () => void; token: string }> = ({ onClose, token }) => {
  const [items, setItems] = useState<OrderItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [reviewOrder, setReviewOrder] = useState<OrderItem | null>(null)
  const [reviewedOrders, setReviewedOrders] = useState<Set<string>>(new Set())

  useEffect(() => {
    fetch(`${API_HUB_URL}/gateway/consumer/orders`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => {
        if (!res.ok) throw new Error('Falha ao carregar historico')
        return res.json()
      })
      .then(data => {
        setItems(data.data || [])
      })
      .catch(err => {
        setError(err.message)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [token])

  const submitReview = async (rating: number, comment: string) => {
    if (!reviewOrder) throw new Error('Selecione um pedido concluido.')
    const response = await fetch(`${API_HUB_URL}/gateway/consumer/orders/${reviewOrder.id}/reviews`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        rating,
        comment: comment || null,
        idempotency_key: `review-${reviewOrder.id}-${window.crypto.randomUUID()}`,
      }),
    })
    const payload = await response.json()
    if (!response.ok) {
      throw new Error(payload.detail || 'Nao foi possivel publicar a avaliacao.')
    }
    setReviewedOrders(current => new Set(current).add(reviewOrder.id))
    return payload
  }

  return (
    <>
      <div className="drawer-overlay" onClick={onClose} role="presentation">
        <div className="drawer-content orders-drawer" onClick={e => e.stopPropagation()} role="dialog" aria-modal="true" aria-labelledby="drawer-title">
        <header className="drawer-header">
          <h2 id="drawer-title">Meus Pedidos e Agendamentos</h2>
          <button className="close-btn" onClick={onClose} aria-label="Fechar">&times;</button>
        </header>
        <div className="drawer-body">
          {loading && <div className="loader"></div>}
          {error && <p className="notice error">{error}</p>}
          {!loading && !error && items.length === 0 && (
            <div className="empty-state">
              <p>Voce ainda nao tem pedidos ou agendamentos.</p>
            </div>
          )}
          {!loading && !error && items.length > 0 && (
            <div className="orders-list">
              {items.map(item => (
                <article key={`${item.kind}-${item.id}`} className="order-card">
                  <div className="order-header">
                    <span className="badge">{item.kind === 'appointment' ? 'Agendamento' : item.kind === 'service' ? 'Servico' : 'Pedido'}</span>
                    <span className="date">
                      {item.created_at ? new Date(item.created_at).toLocaleDateString() : ''}
                    </span>
                  </div>
                  <div className="order-details">
                    <strong>{item.title}</strong>
                    <p>Status: {statusMap[item.status] || item.status}</p>
                    {item.amount_brl && <p className="price">Valor: R$ {Number(item.amount_brl).toFixed(2).replace('.', ',')}</p>}
                    {item.scheduled_at && <p className="schedule">Agendado para: {new Date(item.scheduled_at).toLocaleString()}</p>}
                    {['delivered', 'completed'].includes(item.status) && (
                      <button
                        className="btn-secondary review-action"
                        disabled={reviewedOrders.has(item.id)}
                        onClick={() => setReviewOrder(item)}
                      >
                        {reviewedOrders.has(item.id) ? 'Avaliacao enviada' : 'Avaliar'}
                      </button>
                    )}
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
      </div>
      </div>
      {reviewOrder && (
        <ReviewModal
          orderTitle={reviewOrder.title}
          onClose={() => setReviewOrder(null)}
          onSubmit={submitReview}
        />
      )}
    </>
  )
}

const OrdersDrawer: React.FC<OrdersDrawerProps> = ({ isOpen, onClose, token }) => {
  if (!isOpen || !token) return null
  return <OrdersDrawerContent onClose={onClose} token={token} />
}

export default OrdersDrawer
