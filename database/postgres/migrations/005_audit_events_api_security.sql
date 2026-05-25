BEGIN;

CREATE TABLE IF NOT EXISTS audit.logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES identity.users(id),
    actor_user_id UUID REFERENCES identity.users(id),
    actor_entity_id UUID REFERENCES business.companies(id),
    action VARCHAR(100) NOT NULL,
    module VARCHAR(80) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID,
    before_data JSONB,
    after_data JSONB,
    ip_address INET,
    user_agent TEXT,
    device_fingerprint TEXT,
    status VARCHAR(40) NOT NULL DEFAULT 'recorded',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS audit.domain_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES identity.users(id),
    actor_user_id UUID REFERENCES identity.users(id),
    entity_id UUID REFERENCES business.companies(id),
    routing_key VARCHAR(120) NOT NULL,
    aggregate_type VARCHAR(100) NOT NULL,
    aggregate_id UUID NOT NULL,
    correlation_id UUID NOT NULL DEFAULT gen_random_uuid(),
    schema_version INTEGER NOT NULL DEFAULT 1,
    payload JSONB NOT NULL,
    published_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'pending',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS audit.event_deliveries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES identity.users(id),
    event_id UUID NOT NULL REFERENCES audit.domain_events(id),
    destination VARCHAR(120) NOT NULL,
    delivery_status VARCHAR(40) NOT NULL,
    response_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS compliance.moderation_cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    module VARCHAR(60) NOT NULL,
    resource_type VARCHAR(80) NOT NULL,
    resource_id UUID NOT NULL,
    matched_signals JSONB NOT NULL DEFAULT '[]'::jsonb,
    risk_score NUMERIC(5, 4) CHECK (risk_score BETWEEN 0 AND 1),
    reviewer_user_id UUID REFERENCES identity.users(id),
    decision TEXT,
    status VARCHAR(40) NOT NULL DEFAULT 'pending_review',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS api_hub.api_clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    client_name VARCHAR(150) NOT NULL,
    client_id_hash TEXT NOT NULL UNIQUE,
    secret_reference TEXT NOT NULL,
    scopes JSONB NOT NULL DEFAULT '[]'::jsonb,
    rate_limit_per_minute INTEGER NOT NULL DEFAULT 60,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS api_hub.webhooks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    target_url TEXT NOT NULL,
    event_patterns JSONB NOT NULL DEFAULT '[]'::jsonb,
    signing_secret_reference TEXT NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE OR REPLACE FUNCTION audit.reject_immutable_change()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Append-only table %.% rejects % operations', TG_TABLE_SCHEMA, TG_TABLE_NAME, TG_OP;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS immutable_audit_logs ON audit.logs;
CREATE TRIGGER immutable_audit_logs
BEFORE UPDATE OR DELETE ON audit.logs
FOR EACH ROW EXECUTE FUNCTION audit.reject_immutable_change();

DROP TRIGGER IF EXISTS immutable_event_deliveries ON audit.event_deliveries;
CREATE TRIGGER immutable_event_deliveries
BEFORE UPDATE OR DELETE ON audit.event_deliveries
FOR EACH ROW EXECUTE FUNCTION audit.reject_immutable_change();

DROP TRIGGER IF EXISTS immutable_finance_ledger ON finance.ledger_entries;
CREATE TRIGGER immutable_finance_ledger
BEFORE UPDATE OR DELETE ON finance.ledger_entries
FOR EACH ROW EXECUTE FUNCTION audit.reject_immutable_change();

CREATE INDEX IF NOT EXISTS idx_audit_logs_resource ON audit.logs(module, resource_type, resource_id, created_at);
CREATE INDEX IF NOT EXISTS idx_domain_events_pending ON audit.domain_events(status, created_at);
CREATE INDEX IF NOT EXISTS idx_moderation_cases_pending ON compliance.moderation_cases(status, risk_score);

COMMIT;
