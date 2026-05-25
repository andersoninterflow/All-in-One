BEGIN;

CREATE TABLE IF NOT EXISTS erp.fiscal_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID NOT NULL REFERENCES business.companies(id),
    document_type VARCHAR(20) NOT NULL,
    access_key TEXT,
    amount_brl NUMERIC(18, 4) NOT NULL DEFAULT 0,
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS wms.warehouses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID NOT NULL REFERENCES business.companies(id),
    name VARCHAR(160) NOT NULL,
    addressing_rules JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS wms.inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    warehouse_id UUID NOT NULL REFERENCES wms.warehouses(id),
    sku VARCHAR(120) NOT NULL,
    bin_code VARCHAR(80) NOT NULL,
    quantity NUMERIC(18, 4) NOT NULL DEFAULT 0,
    lot_code VARCHAR(80),
    expires_at DATE,
    status VARCHAR(40) NOT NULL DEFAULT 'available',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS tms.freights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    driver_user_id UUID REFERENCES identity.users(id),
    freight_brl NUMERIC(18, 4) NOT NULL DEFAULT 0,
    toll_brl NUMERIC(18, 4) NOT NULL DEFAULT 0,
    proof_of_delivery JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(40) NOT NULL DEFAULT 'planned',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS crm.opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    title VARCHAR(240) NOT NULL,
    expected_value_brl NUMERIC(18, 4),
    stage VARCHAR(50) NOT NULL DEFAULT 'lead',
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS bpm.workflow_instances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    process_key VARCHAR(120) NOT NULL,
    current_task VARCHAR(120),
    sla_due_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'running',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS document.documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    storage_key TEXT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    mime_type VARCHAR(120),
    version_number INTEGER NOT NULL DEFAULT 1,
    retention_until DATE,
    searchable_text TEXT,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS billing.subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    plan_code VARCHAR(80) NOT NULL,
    recurring_brl NUMERIC(18, 4) NOT NULL DEFAULT 0,
    next_billing_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'trial',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS fiscal.tax_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    type VARCHAR(20) NOT NULL,
    amount_brl NUMERIC(18, 4) NOT NULL DEFAULT 0,
    authority_protocol TEXT,
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS hr.employees (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID NOT NULL REFERENCES business.companies(id),
    employment_type VARCHAR(40) NOT NULL,
    position_title VARCHAR(120),
    admission_date DATE,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS health.patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES identity.users(id),
    health_identifier VARCHAR(80) UNIQUE,
    blood_type VARCHAR(5),
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS health.appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    patient_id UUID NOT NULL REFERENCES health.patients(id),
    professional_user_id UUID NOT NULL REFERENCES identity.users(id),
    scheduled_at TIMESTAMPTZ NOT NULL,
    telemedicine BOOLEAN NOT NULL DEFAULT FALSE,
    clinical_data_encrypted TEXT,
    status VARCHAR(40) NOT NULL DEFAULT 'scheduled',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS vision.devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    device_fingerprint TEXT NOT NULL,
    location_label VARCHAR(160),
    retention_days INTEGER NOT NULL DEFAULT 7 CHECK (retention_days > 0),
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS legal.cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    case_number VARCHAR(120),
    risk_brl NUMERIC(18, 4),
    next_deadline TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS property.properties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    address JSONB NOT NULL,
    property_type VARCHAR(60) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS insurance.policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    reference_type VARCHAR(50) NOT NULL,
    reference_id UUID NOT NULL,
    premium_brl NUMERIC(18, 4) NOT NULL,
    insured_value_brl NUMERIC(18, 4) NOT NULL,
    accepted_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'quoted',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS notifications.messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    channel VARCHAR(30) NOT NULL,
    template_key VARCHAR(100) NOT NULL,
    dispatched_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'queued',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS bi.dashboards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    company_id UUID REFERENCES business.companies(id),
    name VARCHAR(160) NOT NULL,
    definition JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(40) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS ai_core.moderation_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    module VARCHAR(60) NOT NULL,
    resource_id UUID,
    risk_score NUMERIC(5, 4) CHECK (risk_score BETWEEN 0 AND 1),
    reasons JSONB NOT NULL DEFAULT '[]'::jsonb,
    status VARCHAR(40) NOT NULL DEFAULT 'pending_review',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

COMMIT;
