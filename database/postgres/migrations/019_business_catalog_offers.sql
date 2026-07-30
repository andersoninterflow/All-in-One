BEGIN;

CREATE TABLE IF NOT EXISTS business.catalog_offers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    source_module VARCHAR(60) NOT NULL,
    source_entity_id UUID,
    offer_type VARCHAR(40) NOT NULL,
    title VARCHAR(240) NOT NULL,
    short_description TEXT,
    category_id UUID,
    business_category VARCHAR(120),
    business_type VARCHAR(80),
    activity_branch VARCHAR(120),
    price_type VARCHAR(40) NOT NULL DEFAULT 'fixed',
    price_amount NUMERIC(18, 4),
    currency VARCHAR(10) NOT NULL DEFAULT 'BRL',
    location_type VARCHAR(40) NOT NULL DEFAULT 'online',
    availability_type VARCHAR(40) NOT NULL DEFAULT 'immediate',
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    published_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id),
    idempotency_key VARCHAR(100) UNIQUE,
    CHECK (status IN ('draft', 'pending_review', 'published', 'paused', 'rejected', 'archived'))
);

CREATE INDEX IF NOT EXISTS idx_business_catalog_offers_user_status ON business.catalog_offers(user_id, status, created_at);
CREATE INDEX IF NOT EXISTS idx_business_catalog_offers_status_published ON business.catalog_offers(status) WHERE status = 'published';
CREATE INDEX IF NOT EXISTS idx_business_catalog_offers_idempotency ON business.catalog_offers(idempotency_key) WHERE idempotency_key IS NOT NULL;

COMMIT;
