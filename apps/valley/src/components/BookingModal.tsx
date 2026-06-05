import React from 'react'

interface BookingModalProps {
  isOpen: boolean
  onClose: () => void
  offerTitle: string
}

const BookingModal: React.FC<BookingModalProps> = ({ isOpen, onClose, offerTitle }) => {
  if (!isOpen) return null

  return (
    <div className="modal-overlay">
      <div className="modal-content booking-modal">
        <header className="modal-header">
          <h2>Agendamento Valley</h2>
          <button className="close-btn" onClick={onClose} aria-label="Fechar">&times;</button>
        </header>
        <div className="modal-body">
          <h3>{offerTitle}</h3>
          <p className="mock-info">
            Escolha uma data e horario. O modulo <strong>Services</strong> vai intermediar o contrato de prestacao de servico.
          </p>
          <div className="form-group">
            <label>Data desejada:</label>
            <input type="date" className="neo-input" />
          </div>
          <div className="form-group">
            <label>Horario aproximado:</label>
            <input type="time" className="neo-input" />
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
