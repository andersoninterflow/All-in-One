BEGIN;

CREATE TABLE IF NOT EXISTS api_hub.api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    client_id UUID REFERENCES api_hub.api_clients(id),
    key_name VARCHAR(150) NOT NULL,
    key_hash TEXT NOT NULL UNIQUE,
    key_hint VARCHAR(20) NOT NULL,
    scopes JSONB NOT NULL DEFAULT '[]'::jsonb,
    expires_at TIMESTAMPTZ,
    last_used_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    idempotency_key VARCHAR(120) UNIQUE,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS api_hub.integration_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    integration_type VARCHAR(80) NOT NULL,
    provider_name VARCHAR(100) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ended_at TIMESTAMPTZ,
    log_summary TEXT,
    status VARCHAR(40) NOT NULL DEFAULT 'running',
    idempotency_key VARCHAR(120) UNIQUE,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

-- Adicionando idempotency_key as tabelas existentes de api_hub se nao houver
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='api_hub' AND table_name='api_clients' AND column_name='idempotency_key') THEN
        ALTER TABLE api_hub.api_clients ADD COLUMN idempotency_key VARCHAR(120) UNIQUE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='api_hub' AND table_name='webhooks' AND column_name='idempotency_key') THEN
        ALTER TABLE api_hub.webhooks ADD COLUMN idempotency_key VARCHAR(120) UNIQUE;
    END IF;
END $$;

COMMIT;
