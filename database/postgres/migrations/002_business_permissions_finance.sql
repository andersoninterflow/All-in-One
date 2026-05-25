BEGIN;

CREATE TABLE IF NOT EXISTS business.companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    parent_company_id UUID REFERENCES business.companies(id),
    cnpj VARCHAR(18) NOT NULL UNIQUE,
    root_cnpj VARCHAR(18) NOT NULL,
    legal_name VARCHAR(240) NOT NULL,
    trade_name VARCHAR(240),
    cnae VARCHAR(20),
    state_registration VARCHAR(40),
    municipal_registration VARCHAR(40),
    legal_representative_user_id UUID NOT NULL REFERENCES identity.users(id),
    submitted_at TIMESTAMPTZ,
    approved_at TIMESTAMPTZ,
    approved_by UUID REFERENCES identity.users(id),
    rejection_reason TEXT,
    status VARCHAR(40) NOT NULL DEFAULT 'pending_validation',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id),
    CHECK (status IN ('draft', 'pending_documents', 'pending_validation', 'under_review', 'approved', 'active', 'rejected', 'blocked', 'suspended', 'archived'))
);

CREATE TABLE IF NOT EXISTS business.company_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID NOT NULL REFERENCES business.companies(id),
    document_type VARCHAR(80) NOT NULL,
    storage_key TEXT NOT NULL,
    expires_at DATE,
    status VARCHAR(40) NOT NULL DEFAULT 'pending_review',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS business.user_company_memberships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID NOT NULL REFERENCES business.companies(id),
    department VARCHAR(100),
    cost_center VARCHAR(100),
    status VARCHAR(40) NOT NULL DEFAULT 'pending_invitation',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id),
    UNIQUE (user_id, company_id)
);

CREATE TABLE IF NOT EXISTS permissions.roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    name VARCHAR(80) NOT NULL,
    is_system BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS permissions.permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    module VARCHAR(60) NOT NULL,
    action VARCHAR(40) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id),
    UNIQUE (user_id, module, action)
);

CREATE TABLE IF NOT EXISTS permissions.user_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    role_id UUID NOT NULL REFERENCES permissions.roles(id),
    company_id UUID REFERENCES business.companies(id),
    valid_until TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS permissions.access_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    module VARCHAR(60) NOT NULL,
    expression JSONB NOT NULL CHECK (jsonb_typeof(expression) = 'object'),
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS permissions.approval_limits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    role_id UUID REFERENCES permissions.roles(id),
    limit_brl NUMERIC(18, 4),
    requires_dual_approval BOOLEAN NOT NULL DEFAULT FALSE,
    scope VARCHAR(60) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id),
    CHECK (limit_brl IS NULL OR limit_brl >= 0)
);

CREATE TABLE IF NOT EXISTS finance.wallets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    wallet_type VARCHAR(30) NOT NULL DEFAULT 'personal',
    brl_available NUMERIC(18, 4) NOT NULL DEFAULT 0 CHECK (brl_available >= 0),
    brl_held NUMERIC(18, 4) NOT NULL DEFAULT 0 CHECK (brl_held >= 0),
    nex_available NUMERIC(18, 8) NOT NULL DEFAULT 0 CHECK (nex_available >= 0),
    nex_held NUMERIC(18, 8) NOT NULL DEFAULT 0 CHECK (nex_held >= 0),
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id),
    UNIQUE (id, user_id)
);

CREATE TABLE IF NOT EXISTS finance.ledger_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    wallet_id UUID NOT NULL,
    counterparty_user_id UUID REFERENCES identity.users(id),
    currency VARCHAR(10) NOT NULL CHECK (currency IN ('BRL', 'NEX')),
    amount_brl NUMERIC(18, 4),
    amount_nex NUMERIC(18, 8),
    entry_type VARCHAR(40) NOT NULL,
    reference_type VARCHAR(60),
    reference_id UUID,
    idempotency_key TEXT NOT NULL UNIQUE,
    status VARCHAR(40) NOT NULL DEFAULT 'posted',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID REFERENCES identity.users(id),
    CONSTRAINT ledger_wallet_owner_fk FOREIGN KEY (wallet_id, user_id) REFERENCES finance.wallets(id, user_id),
    CHECK ((currency = 'BRL' AND amount_brl IS NOT NULL AND amount_nex IS NULL) OR
           (currency = 'NEX' AND amount_nex IS NOT NULL AND amount_brl IS NULL))
);

CREATE TABLE IF NOT EXISTS finance.escrows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    wallet_id UUID NOT NULL,
    beneficiary_user_id UUID NOT NULL REFERENCES identity.users(id),
    amount_brl NUMERIC(18, 4) NOT NULL CHECK (amount_brl > 0),
    release_condition JSONB NOT NULL DEFAULT '{}'::jsonb,
    dispute_deadline TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'created',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id),
    CONSTRAINT escrow_wallet_owner_fk FOREIGN KEY (wallet_id, user_id) REFERENCES finance.wallets(id, user_id),
    CHECK (status IN ('created', 'authorized', 'captured', 'held', 'released', 'partially_released', 'refunded', 'disputed', 'cancelled', 'expired'))
);

CREATE TABLE IF NOT EXISTS identity.led_cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    wallet_id UUID NOT NULL,
    card_uid_hash TEXT NOT NULL UNIQUE,
    nfc_public_token_hash TEXT UNIQUE,
    activated_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'issued',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id),
    CONSTRAINT led_card_wallet_owner_fk FOREIGN KEY (wallet_id, user_id) REFERENCES finance.wallets(id, user_id),
    UNIQUE (id, user_id)
);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'users_default_wallet_fk'
    ) THEN
        ALTER TABLE identity.users
            ADD CONSTRAINT users_default_wallet_fk
            FOREIGN KEY (default_wallet_id, id) REFERENCES finance.wallets(id, user_id)
            DEFERRABLE INITIALLY DEFERRED;
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'users_primary_led_card_fk'
    ) THEN
        ALTER TABLE identity.users
            ADD CONSTRAINT users_primary_led_card_fk
            FOREIGN KEY (primary_led_card_id, id) REFERENCES identity.led_cards(id, user_id)
            DEFERRABLE INITIALLY DEFERRED;
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_business_companies_owner ON business.companies(user_id);
CREATE INDEX IF NOT EXISTS idx_finance_wallets_user ON finance.wallets(user_id);
CREATE INDEX IF NOT EXISTS idx_finance_ledger_wallet_created ON finance.ledger_entries(wallet_id, created_at);

COMMIT;
