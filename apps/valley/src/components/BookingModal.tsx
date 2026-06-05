import React from 'react'

interface BookingModalProps {
  isOpen: boolean
  onClose: () => void
  offerTitle: string
}

const BookingModal: React.FC<BookingModalProps> = ({ isOpen, onClose, offerTitle }) => {
  if (!isOpen) return null

  return (
    <div className="modal-overlay" role="presentation">
      <div className="modal-content booking-modal" role="dialog" aria-modal="true" aria-labelledby="booking-title">
        <header className="modal-header">
          <h2 id="booking-title">Solicitar horario</h2>
          <button className="close-btn" onClick={onClose} aria-label="Fechar">&times;</button>
        </header>
        <div className="modal-body">
          <h3>{offerTitle}</h3>
          <p className="mock-info">
            Escolha uma data e um horario de preferencia.
          </p>
          <div className="form-group">
            <label htmlFor="booking-date">Data desejada</label>
            <input id="booking-date" type="date" className="neo-input" />
          </div>
          <div className="form-group">
            <label htmlFor="booking-time">Horario aproximado</label>
            <input id="booking-time" type="time" className="neo-input" />
          </div>
          <div className="actions">
            <button className="btn-secondary" onClick={onClose}>Voltar</button>
            <button className="btn-primary" onClick={() => {
              alert('Solicitacao enviada ao prestador!')
              onClose()
            }}>Solicitar Agendamento</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default BookingModal
