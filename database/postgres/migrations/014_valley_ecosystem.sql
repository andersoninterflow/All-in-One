BEGIN;

CREATE TABLE IF NOT EXISTS marketplace.pepita_grants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    order_id UUID NOT NULL,
    customer_user_id UUID NOT NULL REFERENCES identity.users(id),
    pepitas INTEGER NOT NULL CHECK (pepitas IN (1, 10, 100)),
    merchant_gold_ledger_id VARCHAR(120) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'posted',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(metadata) = 'object'),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id),
    idempotency_key VARCHAR(100) UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_marketplace_pepita_grants_customer
    ON marketplace.pepita_grants(customer_user_id, created_at DESC);

CREATE TABLE IF NOT EXISTS stock.discount_quotes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    catalog_product_id UUID,
    selected_percent INTEGER NOT NULL CHECK (selected_percent IN (10, 20, 50)),
    pepitas_required INTEGER NOT NULL CHECK (pepitas_required > 0),
    status VARCHAR(40) NOT NULL DEFAULT 'quoted',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(metadata) = 'object'),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id),
    idempotency_key VARCHAR(100) UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_stock_discount_quotes_user
    ON stock.discount_quotes(user_id, created_at DESC);

COMMIT;
