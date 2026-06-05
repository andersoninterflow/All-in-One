import React, { useState } from 'react'

export interface PaymentIntent {
  amount: string
  order_id: string
}

interface PaymentModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
  paymentIntent: PaymentIntent | null
  token: string | null
}

const API_HUB_URL = import.meta.env.VITE_API_HUB_URL ?? ''

const PaymentModal: React.FC<PaymentModalProps> = ({ isOpen, onClose, onSuccess, paymentIntent, token }) => {
  const [submitting, setSubmitting] = useState(false)
  const [feedback, setFeedback] = useState('')
  const [failed, setFailed] = useState(false)

  if (!isOpen || !paymentIntent) return null

  const handlePay = async () => {
    if (!token) return

    setSubmitting(true)
    setFeedback('')
    setFailed(false)

    try {
      const response = await fetch(`${API_HUB_URL}/gateway/payments/sandbox/authorize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          order_id: paymentIntent.order_id,
          method: 'pix_sandbox',
          idempotency_key: `payment-${paymentIntent.order_id}`
        })
      })

      const payload = await response.json()
      if (!response.ok) {
        throw new Error(payload.detail || 'Falha ao processar pagamento.')
      }

      setFeedback(payload.message || 'Pagamento sandbox autorizado.')
      
      setTimeout(() => {
        onSuccess()
      }, 2000)

    } catch (error) {
      setFailed(true)
      setFeedback(error instanceof Error ? error.message : 'Erro no processamento.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="modal-overlay" role="presentation">
      <div className="modal-content payment-modal" role="dialog" aria-modal="true" aria-labelledby="payment-title">
        <header className="modal-header">
          <h2 id="payment-title">Pagamento Seguro</h2>
          <button className="close-btn" onClick={onClose} aria-label="Fechar">&times;</button>
        </header>
        
        <div className="modal-body">
          <div className="payment-summary">
            <h3>Valor: R$ {Number(paymentIntent.amount).toFixed(2).replace('.', ',')}</h3>
            <p>Seu dinheiro fica protegido e so e liberado apos a conclusao do servico/entrega.</p>
          </div>

          <div className="payment-methods" aria-label="Forma de pagamento">
            <div className="method-card selected">
              <strong>PIX</strong>
              <span>Ambiente sandbox auditavel</span>
            </div>
          </div>

          {feedback && <p className={`action-feedback ${failed ? 'error' : 'success'}`} role="status">{feedback}</p>}

          <div className="actions">
            <button className="btn-secondary" onClick={onClose} disabled={submitting}>Cancelar</button>
            <button className="btn-primary" onClick={handlePay} disabled={submitting || (!failed && feedback !== '')}>
              {submitting ? 'Processando...' : 'Pagar com PIX'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PaymentModal
