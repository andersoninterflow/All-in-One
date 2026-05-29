BEGIN;

ALTER TABLE business.companies ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
ALTER TABLE business.company_documents ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
ALTER TABLE business.user_company_memberships ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

COMMIT;
