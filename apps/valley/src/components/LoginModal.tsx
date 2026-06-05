import React, { useState } from 'react'

interface LoginModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: (token: string, userId: string) => void
}

const API_HUB_URL = import.meta.env.VITE_API_HUB_URL ?? ''

const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isRegistering, setIsRegistering] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      if (isRegistering) {
        const now = new Date().toISOString()
        const payload = {
          full_name: email.split('@')[0].replace(/[._-]+/g, ' '),
          email,
          password_hash: password,
          document_cpf: `CPF-${window.crypto.randomUUID().replaceAll('-', '').slice(0, 12)}`,
          terms_accepted_at: now,
          lgpd_consent_at: now,
        }
        const response = await fetch(`${API_HUB_URL}/registrations`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })

        if (!response.ok) {
          const res = await response.json()
          throw new Error(res.detail || 'Falha ao realizar cadastro.')
        }
      }

      const loginResponse = await fetch(`${API_HUB_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      if (!loginResponse.ok) {
        throw new Error('E-mail ou senha invalidos.')
      }
      const session = await loginResponse.json()
      onSuccess(session.access_token, session.user_id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro na requisicao.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="modal-overlay" role="presentation">
      <div className="modal-content login-modal" role="dialog" aria-modal="true" aria-labelledby="login-title">
        <header className="modal-header">
          <h2 id="login-title">{isRegistering ? 'Criar Conta' : 'Acessar Valley'}</h2>
          <button className="close-btn" onClick={onClose} aria-label="Fechar">&times;</button>
        </header>
        <div className="modal-body">
          <form onSubmit={handleSubmit} className="login-form">
            <div className="input-group">
              <label htmlFor="email">E-mail</label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="seunome@email.com"
              />
            </div>
            <div className="input-group">
              <label htmlFor="password">Senha</label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="********"
              />
            </div>

            {error && <p className="action-feedback error">{error}</p>}

            <div className="actions">
              <button className="btn-primary" type="submit" disabled={loading}>
                {loading ? 'Aguarde...' : isRegistering ? 'Cadastrar' : 'Entrar'}
              </button>
            </div>
          </form>

          <div className="switch-mode">
            <button className="btn-link" onClick={() => setIsRegistering(!isRegistering)}>
              {isRegistering ? 'Ja tenho conta, fazer login' : 'Ainda nao tem conta? Cadastre-se'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoginModal
