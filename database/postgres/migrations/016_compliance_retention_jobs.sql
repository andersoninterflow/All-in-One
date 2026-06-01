BEGIN;

CREATE TABLE IF NOT EXISTS compliance.retention_candidates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module VARCHAR(80) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID NOT NULL,
    subject_id UUID REFERENCES identity.users(id),
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    legal_hold JSONB NOT NULL DEFAULT '[]'::jsonb,
    requested_action VARCHAR(120),
    legal_review_approved BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(40) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'dry_run', 'processed', 'blocked', 'failed')),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    locked_at TIMESTAMPTZ,
    created_by UUID REFERENCES identity.users(id),
    updated_by UUID REFERENCES identity.users(id)
);

CREATE TABLE IF NOT EXISTS compliance.retention_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES compliance.retention_candidates(id),
    module VARCHAR(80) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID NOT NULL,
    job_name VARCHAR(120) NOT NULL,
    action VARCHAR(160) NOT NULL,
    decision_status VARCHAR(40) NOT NULL,
    audit_event VARCHAR(120) NOT NULL,
    evidence JSONB NOT NULL DEFAULT '{}'::jsonb,
    payload JSONB,
    dry_run BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID REFERENCES identity.users(id)
);

CREATE INDEX IF NOT EXISTS idx_retention_candidates_status
    ON compliance.retention_candidates(status, created_at)
    WHERE status IN ('pending', 'failed');

CREATE INDEX IF NOT EXISTS idx_retention_candidates_module
    ON compliance.retention_candidates(module, resource_type, resource_id);

CREATE INDEX IF NOT EXISTS idx_retention_decisions_candidate
    ON compliance.retention_decisions(candidate_id, created_at DESC);

COMMIT;
