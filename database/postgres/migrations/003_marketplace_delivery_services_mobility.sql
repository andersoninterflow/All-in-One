BEGIN;

CREATE TABLE IF NOT EXISTS delivery.rider_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES identity.users(id),
    wallet_id UUID NOT NULL,
    cnh_number_hash TEXT,
    cnh_category VARCHAR(10),
    document_expiry DATE,
    proof_of_life_at TIMESTAMPTZ,
    approved_by UUID REFERENCES identity.users(id),
    status VARCHAR(40) NOT NULL DEFAULT 'pending_documents',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id),
    CONSTRAINT rider_wallet_owner_fk FOREIGN KEY (wallet_id, user_id) REFERENCES finance.wallets(id, user_id)
);

CREATE TABLE IF NOT EXISTS delivery.vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    rider_profile_id UUID NOT NULL REFERENCES delivery.rider_profiles(id),
    type VARCHAR(40) NOT NULL,
    license_plate VARCHAR(12),
    capacity_kg NUMERIC(12, 3),
    refrigerated BOOLEAN NOT NULL DEFAULT FALSE,
    approved_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'pending_review',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS marketplace.stores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID NOT NULL REFERENCES business.companies(id),
    name VARCHAR(200) NOT NULL,
    published_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'pending_validation',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS marketplace.products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    store_id UUID NOT NULL REFERENCES marketplace.stores(id),
    sku VARCHAR(100) NOT NULL,
    name VARCHAR(240) NOT NULL,
    price_brl NUMERIC(18, 4) NOT NULL CHECK (price_brl >= 0),
    stock_quantity NUMERIC(18, 4) NOT NULL DEFAULT 0,
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id),
    UNIQUE (store_id, sku)
);

CREATE TABLE IF NOT EXISTS marketplace.orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    store_id UUID NOT NULL REFERENCES marketplace.stores(id),
    escrow_id UUID REFERENCES finance.escrows(id),
    total_brl NUMERIC(18, 4) NOT NULL CHECK (total_brl >= 0),
    commission_brl NUMERIC(18, 4) NOT NULL DEFAULT 0 CHECK (commission_brl >= 0),
    status VARCHAR(40) NOT NULL DEFAULT 'created',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS stock.suppliers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID NOT NULL REFERENCES business.companies(id),
    homologated_at TIMESTAMPTZ,
    api_configuration JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(40) NOT NULL DEFAULT 'pending_validation',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS stock.catalog_products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    supplier_id UUID NOT NULL REFERENCES stock.suppliers(id),
    external_sku VARCHAR(120) NOT NULL,
    cost_brl NUMERIC(18, 4) NOT NULL CHECK (cost_brl >= 0),
    markup_percent NUMERIC(7, 4) NOT NULL DEFAULT 0 CHECK (markup_percent >= 0),
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS delivery.delivery_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    assigned_rider_user_id UUID REFERENCES identity.users(id),
    escrow_id UUID REFERENCES finance.escrows(id),
    service_type VARCHAR(40) NOT NULL,
    origin JSONB NOT NULL,
    destination JSONB NOT NULL,
    distance_km NUMERIC(12, 3),
    weight_kg NUMERIC(12, 3),
    volume_m3 NUMERIC(12, 4),
    quoted_brl NUMERIC(18, 4),
    insurance_required BOOLEAN NOT NULL DEFAULT FALSE,
    insurance_accepted BOOLEAN,
    status VARCHAR(40) NOT NULL DEFAULT 'created',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS services.providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES identity.users(id),
    category VARCHAR(100) NOT NULL,
    approved_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'pending_review',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS services.service_contracts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    provider_user_id UUID NOT NULL REFERENCES identity.users(id),
    escrow_id UUID NOT NULL REFERENCES finance.escrows(id),
    visit_price_brl NUMERIC(18, 4) NOT NULL CHECK (visit_price_brl >= 0),
    contracted_price_brl NUMERIC(18, 4),
    evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
    status VARCHAR(40) NOT NULL DEFAULT 'created',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS mobility.rides (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    driver_user_id UUID REFERENCES identity.users(id),
    escrow_id UUID REFERENCES finance.escrows(id),
    origin JSONB NOT NULL,
    destination JSONB NOT NULL,
    fare_brl NUMERIC(18, 4) CHECK (fare_brl >= 0),
    vehicle_type VARCHAR(40),
    status VARCHAR(40) NOT NULL DEFAULT 'requested',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS mobility.tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    route_code VARCHAR(80) NOT NULL,
    amount_brl NUMERIC(18, 4) NOT NULL CHECK (amount_brl >= 0),
    qr_token_hash TEXT NOT NULL UNIQUE,
    used_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

COMMIT;
