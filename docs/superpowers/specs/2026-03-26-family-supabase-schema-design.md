# Melamed Family Supabase Schema Design

*Last Edited: 2026-03-26*

## Purpose

Design the foundational Supabase (PostgreSQL) schema for the Melamed family operations platform. The immediate goal is a **tax document tracking MVP** that eliminates back-and-forth with the CPA by providing a pre-organized, gap-aware document package. The schema must support future expansion into contacts, finance, property, health, assets, and family management without rework.

## Context

- **Supabase project**: Already provisioned (`ehayjldbmacrwjegyjcz.supabase.co`), credentials in `.env`
- **Current state**: Tax documents stored as flat files in `tax_document_archive/{year}/`. No database schema exists.
- **CPA workflow pain point**: Aaron uploads a batch of docs, CPA identifies gaps, Aaron scrambles to find missing items. Each round of back-and-forth is billable time.
- **Asana integration**: Task/project management stays in Asana. The DB tracks initiatives and links to Asana project IDs — it does not replicate task management.
- **Architecture**: Follows the 3-layer pattern (Directives → Orchestration → Execution). This schema is the execution layer's data foundation.

## Design Decisions

### Unified Entity Model (vs. Separate Tables per Type)

All people, institutions, businesses, and government agencies live in one `entities` table with a `type` enum. This was chosen over a CRM-style `accounts` + `contacts` separation because:

- **One FK everywhere.** Every table that needs to reference "who" uses `entity_id`. No polymorphic joins.
- **Family life isn't account-based.** Schwab isn't an "account" with "contacts" under it — it's an institution that sends a 1099. The CRM hierarchy adds complexity without value here.
- **Type-specific fields** live in a `metadata` jsonb column, validated at the application layer (Pydantic), not the DB layer.
- **Postgres views** (`v_people`, `v_institutions`, `v_businesses`) provide the ergonomics of separate tables for querying.
- **Future relationships** (e.g., "Dr. Garcia works at CDMX Medical Group") handled by adding an `entity_relationships` join table — no schema redesign.

### Tags over Dedicated Initiative/Category Tables

Initiatives (Green Card, Kitchen Remodel), tax categories (Schedule E, deductible), and general classifications all use a single `tags` + `taggables` system. This was chosen because:

- Initiatives are just a *type* of tag with an optional `asana_project_id`.
- One polymorphic join table handles all cross-cutting concerns instead of separate linking tables per concept.
- An expense tagged `["green-card", "home-office", "deductible", "2024"]` captures initiative, category, tax treatment, and year in one mechanism.

### `tax_schedule` Column vs. Tax Category Tags

The `documents.tax_schedule` column holds the document's **primary** schedule mapping — "this 1099-B goes to Schedule D." Tags provide **cross-cutting classification** — a document can be tagged with multiple categories, initiatives, or years. The column answers "where does my CPA file this?"; the tags answer "what else is this related to?"

### Metadata-Only Document Tracking (MVP)

Documents are tracked by metadata — name, status, source, schedule mapping. Actual files stay in `tax_document_archive/` (referenced by `file_path`). Supabase Storage (`storage_url`) is a future addition that requires zero schema changes.

## Schema

### Table: `entities`

The universal "who" table. Powers contacts, institutions, businesses, family members.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `uuid` | PK, default `gen_random_uuid()` | |
| `type` | `text` | NOT NULL, CHECK IN ('person', 'institution', 'business', 'government', 'property') | Entity classification |
| `name` | `text` | NOT NULL, UNIQUE | Display name |
| `relationship` | `text` | nullable | Relationship to family: "brokerage", "CPA", "pediatrician", "spouse" |
| `email` | `text` | nullable | Primary email |
| `phone` | `text` | nullable | Primary phone |
| `address` | `jsonb` | nullable | `{street, city, state, zip, country}` |
| `metadata` | `jsonb` | default `'{}'` | Type-specific fields (see below) |
| `is_family` | `boolean` | default `false` | Quick filter for household members |
| `created_at` | `timestamptz` | default `now()` | |
| `updated_at` | `timestamptz` | default `now()` | |

**Metadata conventions by type:**

- `person`: `{birthday, notes, nationality}`
- `institution`: `{account_numbers: [...], website, institution_type}`
- `business`: `{ein, entity_type, workspace_path}`
- `government`: `{agency_type, jurisdiction}`
- `property`: `{address, property_type, purchase_date, purchase_price}`

**Indexes:**

- `idx_entities_type` on `type`
- `idx_entities_is_family` on `is_family` WHERE `is_family = true`
- `idx_entities_relationship` on `relationship`

**Views:**

- `v_people`: `SELECT * FROM entities WHERE type = 'person'`
- `v_institutions`: `SELECT * FROM entities WHERE type = 'institution'`
- `v_businesses`: `SELECT * FROM entities WHERE type = 'business'`
- `v_properties`: `SELECT * FROM entities WHERE type = 'property'`

### Table: `documents`

Universal document registry. Tax forms now, legal/medical/financial docs later.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `uuid` | PK, default `gen_random_uuid()` | |
| `name` | `text` | NOT NULL, UNIQUE | "2024 Schwab 1099-Composite" |
| `type` | `text` | NOT NULL, CHECK IN ('tax_form', 'receipt', 'legal', 'medical', 'financial', 'identification', 'other') | Document classification |
| `source_entity_id` | `uuid` | FK → `entities(id)`, nullable | Who sent/created it |
| `owner_entity_id` | `uuid` | FK → `entities(id)`, nullable | Who it belongs to (Aaron, Eugenia, joint) |
| `tax_year` | `smallint` | nullable | Tax year the document applies to |
| `tax_schedule` | `text` | nullable | "Schedule D", "Schedule E", "Schedule C", "Schedule A" |
| `form_number` | `text` | nullable | "1099-B", "W-2", "1098" |
| `status` | `text` | NOT NULL, CHECK IN ('expected', 'received', 'submitted', 'verified'), default `'expected'` | Document lifecycle |
| `file_path` | `text` | nullable | Local file path (MVP) |
| `storage_url` | `text` | nullable | Supabase Storage URL (future) |
| `notes` | `text` | nullable | |
| `metadata` | `jsonb` | default `'{}'` | Flexible: `{line_items, amounts, conditional_reason}` |
| `created_at` | `timestamptz` | default `now()` | |
| `updated_at` | `timestamptz` | default `now()` | |

**Indexes:**

- `idx_documents_tax_year` on `tax_year`
- `idx_documents_status` on `status`
- `idx_documents_tax_schedule` on `tax_schedule`
- `idx_documents_type` on `type`
- `idx_documents_source_entity` on `source_entity_id`
- `idx_documents_owner_entity` on `owner_entity_id`

### Table: `tags`

Unified classification system for initiatives, tax categories, and general labels.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `uuid` | PK, default `gen_random_uuid()` | |
| `name` | `text` | NOT NULL, UNIQUE | Slug: "green-card", "schedule-e", "deductible" |
| `display_name` | `text` | NOT NULL | Human-readable: "Green Card", "Schedule E" |
| `type` | `text` | NOT NULL, CHECK IN ('initiative', 'tax_category', 'tax_year', 'expense_category', 'domain', 'custom') | Tag classification |
| `asana_project_id` | `text` | nullable | Links initiative tags to Asana projects |
| `metadata` | `jsonb` | default `'{}'` | Type-specific: `{budget, target_date, status, description}` |
| `created_at` | `timestamptz` | default `now()` | |
| `updated_at` | `timestamptz` | default `now()` | |

**Indexes:**

- `idx_tags_type` on `type`
- `idx_tags_name` on `name`

### Table: `taggables`

Polymorphic join table connecting tags to any record.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `uuid` | PK, default `gen_random_uuid()` | |
| `tag_id` | `uuid` | FK → `tags(id)` ON DELETE CASCADE, NOT NULL | |
| `taggable_type` | `text` | NOT NULL, CHECK IN ('entity', 'document', 'expense', 'asset') | Target table name |
| `taggable_id` | `uuid` | NOT NULL | Target row ID |
| `created_at` | `timestamptz` | default `now()` | |

**Indexes:**

- `idx_taggables_tag` on `tag_id`
- `idx_taggables_target` on `(taggable_type, taggable_id)`
- UNIQUE constraint on `(tag_id, taggable_type, taggable_id)` — prevent duplicate tagging

### Trigger: `updated_at`

A shared trigger function applied to `entities`, `documents`, and `tags`:

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

Applied via `CREATE TRIGGER` on each table with `BEFORE UPDATE`.

### Row-Level Security

All tables enable RLS. MVP policy: all authenticated users have full access. Scoped per-user policies added when the family dashboard launches.

```sql
ALTER TABLE entities ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE tags ENABLE ROW LEVEL SECURITY;
ALTER TABLE taggables ENABLE ROW LEVEL SECURITY;

-- MVP: authenticated users can do everything
CREATE POLICY "authenticated_full_access" ON entities
  FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "authenticated_full_access" ON documents
  FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "authenticated_full_access" ON tags
  FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "authenticated_full_access" ON taggables
  FOR ALL TO authenticated USING (true) WITH CHECK (true);
```

## Seed Data (Tax MVP)

### Entities to Seed

| Name | Type | Relationship |
|------|------|-------------|
| Aaron Melamed | person | self |
| Eugenia Guadalupe Canul Celis | person | spouse |
| Itero | business | owned_business |
| Keynote Capital, LLC | business | owned_business |
| Homeowners First, LLC | business | owned_business |
| Palisades Labs | business | owned_business |
| Schwab | institution | brokerage |
| Betterment | institution | investment |
| Guideline | institution | retirement_401k |
| Goldman Sachs Marcus | institution | savings |
| American Express | institution | banking |
| Wells Fargo | institution | banking |
| Coinbase | institution | crypto |
| ProPay | institution | payment_processor |
| New American Funding | institution | mortgage_servicer |
| JustWorks | institution | payroll |
| State Street | institution | retirement |
| T-Mobile | institution | telecom |
| 1771 11th Ave, SF | property | rental_property |

### Tags to Seed

| Name | Display Name | Type |
|------|-------------|------|
| schedule-a | Schedule A (Itemized Deductions) | tax_category |
| schedule-b | Schedule B (Interest & Dividends) | tax_category |
| schedule-c | Schedule C (Business Income) | tax_category |
| schedule-d | Schedule D (Capital Gains) | tax_category |
| schedule-e | Schedule E (Rental/Passthrough) | tax_category |
| schedule-se | Schedule SE (Self-Employment Tax) | tax_category |
| form-8949 | Form 8949 (Sales of Capital Assets) | tax_category |
| deductible | Deductible Expense | expense_category |
| home-office | Home Office | expense_category |
| rental-expense | Rental Property Expense | expense_category |
| tax-2023 | Tax Year 2023 | tax_year |
| tax-2024 | Tax Year 2024 | tax_year |
| tax-2025 | Tax Year 2025 | tax_year |
| green-card | Green Card | initiative |

### Documents to Seed (2024 Expected)

Pre-populate based on the CPA checklist. Each row starts as `status: 'expected'`. Example subset:

| Name | Form | Source Entity | Tax Schedule | Conditional |
|------|------|--------------|-------------|-------------|
| 2024 JustWorks W-2 | W-2 | JustWorks | Schedule C | Yes — only if employed |
| 2024 Schwab 1099-Composite | 1099-Composite | Schwab | Schedule D | No |
| 2024 Betterment 1099-B/DIV | 1099-B | Betterment | Schedule D | No |
| 2024 Betterment FMV Statement | FMV | Betterment | Schedule D | No |
| 2024 Guideline 401k Statement | Year-End Statement | Guideline | N/A | No |
| 2024 State Street 1099-R | 1099-R | State Street | N/A | Yes — if distribution |
| 2024 Marcus 1099-INT | 1099-INT | Goldman Sachs Marcus | Schedule B | No |
| 2024 Amex 1099-INT | 1099-INT | American Express | Schedule B | No |
| 2024 Schwab 1099-INT | 1099-INT | Schwab | Schedule B | No |
| 2024 Wells Fargo 1099-INT | 1099-INT | Wells Fargo | Schedule B | Yes — if active |
| 2024 Mortgage 1098 | 1098 | New American Funding | Schedule A | No |
| 2024 ProPay 1099-K | 1099-K | ProPay | Schedule E | No |
| 2024 Health Insurance 1095 | 1095-C/1095-A | (varies) | N/A | Varies |
| 2024 Coinbase 1099 | 1099 | Coinbase | Schedule D | Yes — if trades |
| 2024 Rental Income Summary | CSV (self-prepared) | Aaron Melamed | Schedule E | No |
| 2024 Rental Expenses | CSV (self-prepared) | Aaron Melamed | Schedule E | No |
| 2024 Home Office Rent Allocation | CSV (self-prepared) | Aaron Melamed | Schedule C | No |
| 2024 Business Meals | CSV (self-prepared) | Aaron Melamed | Schedule C | No |
| 2024 Dues & Subscriptions | CSV (self-prepared) | Aaron Melamed | Schedule C | No |
| 2024 Credit Card Annual Fees | CSV (self-prepared) | Aaron Melamed | Schedule C | No |
| 2024 Cell Phone Expenses | CSV (self-prepared) | Aaron Melamed | Schedule C | No |
| 2024 Office Supplies | CSV (self-prepared) | Aaron Melamed | Schedule C | No |
| 2024 Utilities (Home Office) | CSV (self-prepared) | Aaron Melamed | Schedule C | No |

Conditional documents get `metadata: {conditional: true, condition: "only if employed that year"}`.

## Tax MVP Queries

Key queries this schema enables:

```sql
-- What's missing for 2024?
SELECT name, form_number, tax_schedule
FROM documents
WHERE tax_year = 2024 AND status = 'expected'
ORDER BY tax_schedule, name;

-- CPA package grouped by schedule
SELECT tax_schedule, array_agg(name ORDER BY name) as documents
FROM documents
WHERE tax_year = 2024 AND status IN ('received', 'submitted')
GROUP BY tax_schedule
ORDER BY tax_schedule;

-- All docs from a specific institution
SELECT d.name, d.status, d.tax_schedule
FROM documents d
JOIN entities e ON d.source_entity_id = e.id
WHERE e.name = 'Schwab' AND d.tax_year = 2024;

-- Everything tied to an initiative
SELECT d.name, d.type, d.status
FROM documents d
JOIN taggables t ON t.taggable_type = 'document' AND t.taggable_id = d.id
JOIN tags tg ON tg.id = t.tag_id
WHERE tg.name = 'green-card';
```

## Future Expansion Path

These tables bolt on without modifying the existing four:

| Table | When | Connects Via |
|-------|------|-------------|
| `entity_relationships` | Family CRM phase | `parent_entity_id`, `child_entity_id` → `entities` |
| `expenses` | Finance phase | `entity_id` → `entities`, tagged via `taggables` |
| `assets` | Asset tracking phase | `custodian_entity_id` → `entities`, tagged via `taggables` |
| `income_sources` | Finance phase | `entity_id` → `entities` |
| Supabase Storage bucket | File storage phase | `documents.storage_url` populated |

## Out of Scope

- Task management (Asana owns this)
- Tax calculations or form generation (CPA does this)
- Real-time financial data sync (Monarch Money handles budgeting)
- User authentication beyond Supabase defaults
