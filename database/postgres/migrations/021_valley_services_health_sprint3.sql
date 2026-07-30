BEGIN;

-- For services.service_contracts
ALTER TABLE services.service_contracts
ADD COLUMN IF NOT EXISTS offer_id UUID REFERENCES business.catalog_offers(id),
ADD COLUMN IF NOT EXISTS company_id UUID REFERENCES business.companies(id),
ADD COLUMN IF NOT EXISTS scheduled_at TIMESTAMPTZ;

ALTER TABLE services.service_contracts
ALTER COLUMN provider_user_id DROP NOT NULL;

ALTER TABLE services.service_contracts
ALTER COLUMN escrow_id DROP NOT NULL;

-- For health.appointments
ALTER TABLE health.appointments
ADD COLUMN IF NOT EXISTS offer_id UUID REFERENCES business.catalog_offers(id),
ADD COLUMN IF NOT EXISTS company_id UUID REFERENCES business.companies(id);

ALTER TABLE health.appointments
ALTER COLUMN patient_id DROP NOT NULL;

ALTER TABLE health.appointments
ALTER COLUMN professional_user_id DROP NOT NULL;

COMMIT;
