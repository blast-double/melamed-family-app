-- Last Edited: 2026-03-26
-- Migration: 001_foundation_schema
-- Creates: entities, documents, tags, taggables + indexes, views, triggers, RLS
--
-- ROLLBACK (uncomment and run to tear down):
-- DROP VIEW IF EXISTS v_people, v_institutions, v_businesses, v_properties;
-- DROP TABLE IF EXISTS taggables, tags, documents, entities CASCADE;
-- DROP FUNCTION IF EXISTS update_updated_at();

BEGIN;

-- =============================================================================
-- FUNCTION: updated_at trigger
-- =============================================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- TABLE: entities
-- =============================================================================
CREATE TABLE entities (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  type text NOT NULL CHECK (type IN ('person', 'institution', 'business', 'government', 'property')),
  name text NOT NULL UNIQUE,
  relationship text,
  email text,
  phone text,
  address jsonb,
  metadata jsonb NOT NULL DEFAULT '{}',
  is_family boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_entities_type ON entities(type);
CREATE INDEX idx_entities_is_family ON entities(is_family) WHERE is_family = true;
CREATE INDEX idx_entities_relationship ON entities(relationship);

CREATE TRIGGER trg_entities_updated_at
  BEFORE UPDATE ON entities
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- TABLE: documents
-- =============================================================================
CREATE TABLE documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL UNIQUE,
  type text NOT NULL CHECK (type IN ('tax_form', 'receipt', 'legal', 'medical', 'financial', 'identification', 'other')),
  source_entity_id uuid REFERENCES entities(id),
  owner_entity_id uuid REFERENCES entities(id),
  tax_year smallint,
  tax_schedule text,
  form_number text,
  status text NOT NULL DEFAULT 'expected' CHECK (status IN ('expected', 'received', 'submitted', 'verified')),
  file_path text,
  storage_url text,
  notes text,
  metadata jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_documents_tax_year ON documents(tax_year);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_tax_schedule ON documents(tax_schedule);
CREATE INDEX idx_documents_type ON documents(type);
CREATE INDEX idx_documents_source_entity ON documents(source_entity_id);
CREATE INDEX idx_documents_owner_entity ON documents(owner_entity_id);

CREATE TRIGGER trg_documents_updated_at
  BEFORE UPDATE ON documents
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- TABLE: tags
-- =============================================================================
CREATE TABLE tags (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL UNIQUE,
  display_name text NOT NULL,
  type text NOT NULL CHECK (type IN ('initiative', 'tax_category', 'tax_year', 'expense_category', 'domain', 'custom')),
  asana_project_id text,
  metadata jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_tags_type ON tags(type);
CREATE INDEX idx_tags_name ON tags(name);

CREATE TRIGGER trg_tags_updated_at
  BEFORE UPDATE ON tags
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- TABLE: taggables
-- =============================================================================
CREATE TABLE taggables (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tag_id uuid NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  taggable_type text NOT NULL CHECK (taggable_type IN ('entity', 'document', 'expense', 'asset')),
  taggable_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tag_id, taggable_type, taggable_id)
);

CREATE INDEX idx_taggables_tag ON taggables(tag_id);
CREATE INDEX idx_taggables_target ON taggables(taggable_type, taggable_id);

-- =============================================================================
-- VIEWS
-- =============================================================================
CREATE VIEW v_people AS SELECT * FROM entities WHERE type = 'person';
CREATE VIEW v_institutions AS SELECT * FROM entities WHERE type = 'institution';
CREATE VIEW v_businesses AS SELECT * FROM entities WHERE type = 'business';
CREATE VIEW v_properties AS SELECT * FROM entities WHERE type = 'property';

-- =============================================================================
-- ROW-LEVEL SECURITY
-- =============================================================================
ALTER TABLE entities ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE tags ENABLE ROW LEVEL SECURITY;
ALTER TABLE taggables ENABLE ROW LEVEL SECURITY;

-- Authenticated users (dashboard, future app)
CREATE POLICY "authenticated_full_access" ON entities
  FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "authenticated_full_access" ON documents
  FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "authenticated_full_access" ON tags
  FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "authenticated_full_access" ON taggables
  FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Service role (Python scripts via service_role key — bypasses RLS, but explicit policy is belt-and-suspenders)
CREATE POLICY "service_role_full_access" ON entities
  FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_full_access" ON documents
  FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_full_access" ON tags
  FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_full_access" ON taggables
  FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Anon role (fallback if publishable key used accidentally)
CREATE POLICY "anon_full_access" ON entities
  FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon_full_access" ON documents
  FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon_full_access" ON tags
  FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon_full_access" ON taggables
  FOR ALL TO anon USING (true) WITH CHECK (true);

COMMIT;
