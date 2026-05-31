BEGIN;

CREATE TABLE IF NOT EXISTS finance.valley_gold_ledger_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id),
    merchant_business_id UUID NOT NULL REFERENCES business.companies(id),
    entry_type VARCHAR(40) NOT NULL CHECK (entry_type IN ('purchase_credit', 'pepita_grant_debit', 'manual_adjustment')),
    amount_gold_delta INTEGER NOT NULL CHECK (amount_gold_delta <> 0),
    reference_type VARCHAR(60) NOT NULL CHECK (reference_type IN ('gold_purchase', 'pepita_grant', 'manual_adjustment')),
    reference_id UUID,
    status VARCHAR(40) NOT NULL DEFAULT 'posted',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(metadata) = 'object'),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID REFERENCES identity.users(id),
    idempotency_key TEXT NOT NULL UNIQUE,
    CHECK (
        (entry_type = 'purchase_credit' AND amount_gold_delta > 0)
        OR (entry_type = 'pepita_grant_debit' AND amount_gold_delta < 0 AND reference_id IS NOT NULL)
        OR (entry_type = 'manual_adjustment')
    )
);

CREATE INDEX IF NOT EXISTS idx_finance_valley_gold_merchant_created
    ON finance.valley_gold_ledger_entries(merchant_business_id, created_at DESC);

DROP TRIGGER IF EXISTS immutable_valley_gold_ledger ON finance.valley_gold_ledger_entries;
CREATE TRIGGER immutable_valley_gold_ledger
BEFORE UPDATE OR DELETE ON finance.valley_gold_ledger_entries
FOR EACH ROW EXECUTE FUNCTION audit.reject_immutable_change();

COMMIT;
