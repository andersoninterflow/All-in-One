BEGIN;

-- Marketplace
ALTER TABLE marketplace.stores ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
ALTER TABLE marketplace.products ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
ALTER TABLE marketplace.orders ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- Stock
ALTER TABLE stock.suppliers ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
ALTER TABLE stock.catalog_products ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- Delivery
ALTER TABLE delivery.rider_profiles ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
ALTER TABLE delivery.vehicles ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
ALTER TABLE delivery.delivery_requests ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- Services
ALTER TABLE services.providers ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
ALTER TABLE services.service_contracts ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- Mobility
ALTER TABLE mobility.rides ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
ALTER TABLE mobility.tickets ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- ERP
ALTER TABLE erp.fiscal_documents ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- WMS
ALTER TABLE wms.warehouses ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
ALTER TABLE wms.inventory ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- TMS
ALTER TABLE tms.freights ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- CRM
ALTER TABLE crm.opportunities ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- BPM
ALTER TABLE bpm.workflow_instances ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- Document
ALTER TABLE document.documents ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- Billing (if table exists, it was created in 004 but under schema erp? No, 004 says billing.subscriptions)
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='billing' AND table_name='subscriptions') THEN
    ALTER TABLE billing.subscriptions ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
END IF; END $$;

-- Fiscal
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='fiscal' AND table_name='tax_documents') THEN
    ALTER TABLE fiscal.tax_documents ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
END IF; END $$;

-- HR
ALTER TABLE hr.employees ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- Health
ALTER TABLE health.patients ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
ALTER TABLE health.appointments ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- Vision
ALTER TABLE vision.devices ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- Legal
ALTER TABLE legal.cases ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- Property
ALTER TABLE property.properties ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- Insurance
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='insurance' AND table_name='policies') THEN
    ALTER TABLE insurance.policies ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
END IF; END $$;

-- Notifications
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='notifications' AND table_name='messages') THEN
    ALTER TABLE notifications.messages ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;
END IF; END $$;

-- BI
ALTER TABLE bi.dashboards ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

-- AI Core
ALTER TABLE ai_core.moderation_decisions ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(120) UNIQUE;

COMMIT;
