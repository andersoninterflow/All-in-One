-- Migration 017: Tabela de itens de fatura para o ERP
-- Data: 2026-06-01

CREATE TABLE IF NOT EXISTS erp.invoice_items (
    id UUID PRIMARY KEY,
    fiscal_document_id UUID NOT NULL REFERENCES erp.fiscal_documents(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    quantity NUMERIC(18, 4) NOT NULL DEFAULT 1,
    unit_price_brl NUMERIC(18, 4) NOT NULL,
    total_price_brl NUMERIC(18, 4) NOT NULL,
    tax_amount_brl NUMERIC(18, 4) NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_invoice_items_document ON erp.invoice_items (fiscal_document_id);

COMMENT ON TABLE erp.invoice_items IS 'Itens detalhados vinculados a um documento fiscal no modulo ERP';