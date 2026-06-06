BEGIN;

ALTER TABLE marketplace.orders 
ADD COLUMN IF NOT EXISTS offer_id UUID REFERENCES business.catalog_offers(id),
ADD COLUMN IF NOT EXISTS company_id UUID REFERENCES business.companies(id);

ALTER TABLE marketplace.orders ALTER COLUMN store_id DROP NOT NULL;

-- In postgres, status is just a VARCHAR(40) so we don't need to change constraints 
-- unless there is a specific check constraint on status which there isn't in 003_marketplace.

COMMIT;
