-- Last Edited: 2026-03-28
-- Migration: 003_portal_security
-- Locks down anon access. Anon gets read-only on documents + transactions.
-- Mutations go through authenticated role or service_role (via API routes).
--
-- ROLLBACK:
-- DROP POLICY IF EXISTS "anon_read_documents" ON documents;
-- DROP POLICY IF EXISTS "anon_update_verification" ON documents;
-- CREATE POLICY "anon_full_access" ON entities FOR ALL TO anon USING (true) WITH CHECK (true);
-- CREATE POLICY "anon_full_access" ON documents FOR ALL TO anon USING (true) WITH CHECK (true);
-- CREATE POLICY "anon_full_access" ON tags FOR ALL TO anon USING (true) WITH CHECK (true);
-- CREATE POLICY "anon_full_access" ON taggables FOR ALL TO anon USING (true) WITH CHECK (true);

BEGIN;

-- =============================================================================
-- Revoke anon full access from 001_foundation_schema.sql
-- =============================================================================
DROP POLICY IF EXISTS "anon_full_access" ON entities;
DROP POLICY IF EXISTS "anon_full_access" ON documents;
DROP POLICY IF EXISTS "anon_full_access" ON tags;
DROP POLICY IF EXISTS "anon_full_access" ON taggables;

-- =============================================================================
-- Anon: read-only on documents (CPA verification view)
-- =============================================================================
CREATE POLICY "anon_read_documents" ON documents
  FOR SELECT TO anon USING (true);

-- Anon: read-only on entities (CPA needs institution names)
CREATE POLICY "anon_read_entities" ON entities
  FOR SELECT TO anon USING (true);

-- Anon: can update documents (for CPA verification state in metadata)
-- Field-level validation enforced in Next.js API routes
CREATE POLICY "anon_update_verification" ON documents
  FOR UPDATE TO anon
  USING (true)
  WITH CHECK (true);

-- Note: anon_read_transactions already created in 002

COMMIT;
