-- Last Edited: 2026-03-28
-- Migration: 002_tax_processing
-- Creates: transactions table, adds 'extracted' status to documents
--
-- ROLLBACK:
-- DROP TABLE IF EXISTS transactions;
-- ALTER TABLE documents DROP CONSTRAINT documents_status_check;
-- ALTER TABLE documents ADD CONSTRAINT documents_status_check
--   CHECK (status IN ('expected', 'received', 'submitted', 'verified'));

BEGIN;

-- =============================================================================
-- TABLE: transactions (Monarch CSV rows + triage state)
-- =============================================================================
CREATE TABLE transactions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tax_year smallint NOT NULL,
  date date NOT NULL,
  merchant text NOT NULL,
  category text NOT NULL,
  account text,
  original_statement text,
  notes text,
  amount numeric(12,2) NOT NULL,
  tags text,
  owner text,
  -- Classification (set by parse_csv.py)
  tax_schedule text,
  -- Triage state (set by portal UI)
  triage_status text NOT NULL DEFAULT 'pending'
    CHECK (triage_status IN ('pending', 'resolved', 'excluded')),
  resolved_schedule text,
  is_business boolean,
  triage_notes text,
  -- Anomaly flags (set by parse_csv.py)
  anomaly_reason text,
  anomaly_details text,
  -- Timestamps
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_transactions_tax_year ON transactions(tax_year);
CREATE INDEX idx_transactions_triage_status ON transactions(triage_status);
CREATE INDEX idx_transactions_tax_schedule ON transactions(tax_schedule);
CREATE INDEX idx_transactions_anomaly ON transactions(anomaly_reason)
  WHERE anomaly_reason IS NOT NULL;

CREATE TRIGGER trg_transactions_updated_at
  BEFORE UPDATE ON transactions
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- ALTER documents: add 'extracted' to status enum
-- =============================================================================
ALTER TABLE documents DROP CONSTRAINT documents_status_check;
ALTER TABLE documents ADD CONSTRAINT documents_status_check
  CHECK (status IN ('expected', 'received', 'extracted', 'submitted', 'verified'));

-- =============================================================================
-- RLS for transactions
-- =============================================================================
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "authenticated_full_access" ON transactions
  FOR ALL TO authenticated USING (true) WITH CHECK (true);

CREATE POLICY "service_role_full_access" ON transactions
  FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Anon gets read-only (will be refined in 003)
CREATE POLICY "anon_read_transactions" ON transactions
  FOR SELECT TO anon USING (true);

COMMIT;
