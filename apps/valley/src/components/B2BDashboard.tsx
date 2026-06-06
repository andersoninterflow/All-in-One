import React, { useState } from 'react';
import CalendarWidget from './CalendarWidget';

export default function B2BDashboard() {
  const [activeTab, setActiveTab] = useState<'overview' | 'calendar'>('overview');

  return (
    <div className="b2b-dashboard" style={{ padding: '2rem', background: '#f8fafc', minHeight: '100vh' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', color: '#0f172a' }}>Painel do Lojista (B2B)</h1>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button 
            style={{ padding: '0.5rem 1rem', background: activeTab === 'overview' ? '#3b82f6' : '#e2e8f0', color: activeTab === 'overview' ? 'white' : '#0f172a', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
            onClick={() => setActiveTab('overview')}
          >
            Visão Geral
          </button>
          <button 
            style={{ padding: '0.5rem 1rem', background: activeTab === 'calendar' ? '#3b82f6' : '#e2e8f0', color: activeTab === 'calendar' ? 'white' : '#0f172a', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
            onClick={() => setActiveTab('calendar')}
          >
            Agenda
          </button>
        </div>
      </header>

      {activeTab === 'overview' && (
        <div className="dashboard-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
          <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h3 style={{ color: '#64748b', fontSize: '0.875rem', textTransform: 'uppercase' }}>Faturamento Hoje</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#0f172a', margin: '0.5rem 0' }}>R$ 1.450,00</p>
            <span style={{ color: '#10b981', fontSize: '0.875rem' }}>+15% vs Ontem</span>
          </div>
          
          <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h3 style={{ color: '#64748b', fontSize: '0.875rem', textTransform: 'uppercase' }}>Pedidos Ativos</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#0f172a', margin: '0.5rem 0' }}>12</p>
            <span style={{ color: '#f59e0b', fontSize: '0.875rem' }}>3 aguardando preparo</span>
          </div>

          <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h3 style={{ color: '#64748b', fontSize: '0.875rem', textTransform: 'uppercase' }}>Saldo na Wallet</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#0f172a', margin: '0.5rem 0' }}>R$ 8.920,50</p>
            <span style={{ color: '#3b82f6', fontSize: '0.875rem', cursor: 'pointer' }}>Solicitar Saque (Cash-out)</span>
          </div>
        </div>
      )}

      {activeTab === 'calendar' && (
        <CalendarWidget />
      )}
    </div>
  );
}
