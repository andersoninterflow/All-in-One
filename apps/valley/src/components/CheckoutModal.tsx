import React from 'react'

interface CheckoutModalProps {
  isOpen: boolean
  onClose: () => void
  offerTitle: string
  priceAmount: string | null
}

const CheckoutModal: React.FC<CheckoutModalProps> = ({ isOpen, onClose, offerTitle, priceAmount }) => {
  if (!isOpen) return null

  return (
    <div className="modal-overlay" role="presentation">
      <div className="modal-content checkout-modal" role="dialog" aria-modal="true" aria-labelledby="checkout-title">
        <header className="modal-header">
          <h2 id="checkout-title">Finalizar pedido</h2>
          <button className="close-btn" onClick={onClose} aria-label="Fechar">&times;</button>
        </header>
        <div className="modal-body">
          <h3>{offerTitle}</h3>
          <div className="price-tag">
            {priceAmount ? `Total: R$ ${Number(priceAmount).toFixed(2).replace('.', ',')}` : 'Valor a combinar'}
          </div>
          <p className="mock-info">
            Revise os dados antes de confirmar.
          </p>
          <div className="actions">
            <button className="btn-secondary" onClick={onClose}>Cancelar</button>
            <button className="btn-primary" onClick={() => {
              alert('Pagamento simulado com sucesso!')
              onClose()
            }}>Confirmar Pagamento</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CheckoutModal
