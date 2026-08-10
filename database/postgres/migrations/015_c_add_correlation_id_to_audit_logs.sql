BEGIN;

ALTER TABLE audit.logs ADD COLUMN IF NOT EXISTS correlation_id UUID NOT NULL DEFAULT gen_random_uuid();

COMMIT;
