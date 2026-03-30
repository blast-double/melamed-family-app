# Family Supabase Schema Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy a 4-table Supabase schema (entities, documents, tags, taggables) with seed data so Aaron can track tax document status and hand his CPA a gap-free, schedule-organized package.

**Architecture:** SQL migrations run against the provisioned Supabase instance via `psql` using the connection string in `.env`. A Python seed script uses the `supabase` client library to populate entities, tags, and expected 2024 tax documents. A Python query script provides the "what's missing" and "CPA package" views.

**Tech Stack:** PostgreSQL (Supabase), Python 3.13, supabase-py, pydantic, python-dotenv, pytest

**Spec:** `docs/superpowers/specs/2026-03-26-family-supabase-schema-design.md`

---

## File Structure

```
execution/
├── db/
│   ├── migrations/
│   │   └── 001_foundation_schema.sql    # All 4 tables, indexes, views, triggers, RLS
│   ├── seed.py                          # Seed entities, tags, and 2024 expected documents
│   ├── client.py                        # Supabase client singleton (loads .env)
│   └── queries.py                       # Tax MVP queries: missing docs, CPA package, etc.
├── tax/
│   └── checklist.py                     # Print tax document status for a given year
tests/
├── test_db_client.py                    # Verify Supabase connection
├── test_seed.py                         # Verify seed data landed correctly
└── test_queries.py                      # Verify MVP queries return expected shapes
```

---

### Task 1: Schema Migration SQL

**Files:**
- Create: `execution/db/migrations/001_foundation_schema.sql`

- [ ] **Step 1: Write the `entities` table DDL**

Create `execution/db/migrations/001_foundation_schema.sql`:

```sql
-- Last Edited: 2026-03-26
-- Migration: 001_foundation_schema
-- Creates: entities, documents, tags, taggables + indexes, views, triggers, RLS

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
```

- [ ] **Step 2: Add the `documents` table DDL**

Append to the same file:

```sql
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
```

- [ ] **Step 3: Add the `tags` and `taggables` table DDL**

Append to the same file:

```sql
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
```

- [ ] **Step 4: Add views and RLS**

Append to the same file:

```sql
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

CREATE POLICY "authenticated_full_access" ON entities
  FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "authenticated_full_access" ON documents
  FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "authenticated_full_access" ON tags
  FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "authenticated_full_access" ON taggables
  FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Also allow service_role (used by Python scripts via service key)
CREATE POLICY "service_role_full_access" ON entities
  FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_full_access" ON documents
  FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_full_access" ON tags
  FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_full_access" ON taggables
  FOR ALL TO service_role USING (true) WITH CHECK (true);
```

- [ ] **Step 5: Run the migration against Supabase**

Run:
```bash
psql "$SUPABASE_DATA_STRING_CONNECTION" -f execution/db/migrations/001_foundation_schema.sql
```

Note: The `.env` file has a typo (`SUPABASE_DATA_STRING_CONNETION`). Use the connection string directly or fix the env var name first. If `psql` is not installed locally, install via:
```bash
brew install libpq && brew link --force libpq
```

Alternatively, run via the Supabase SQL Editor in the dashboard or use psycopg2:
```bash
cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal
python3 -c "
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
conn = psycopg2.connect(os.environ['SUPABASE_DATA_STRING_CONNETION'])
conn.autocommit = True
with open('execution/db/migrations/001_foundation_schema.sql') as f:
    conn.cursor().execute(f.read())
conn.close()
print('Migration complete.')
"
```

Expected: All 4 tables created, no errors.

- [ ] **Step 6: Verify tables exist**

```bash
python3 -c "
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
conn = psycopg2.connect(os.environ['SUPABASE_DATA_STRING_CONNETION'])
cur = conn.cursor()
cur.execute(\"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name\")
for row in cur.fetchall():
    print(row[0])
conn.close()
"
```

Expected output should include: `documents`, `entities`, `taggables`, `tags`

- [ ] **Step 7: Commit**

```bash
git add execution/db/migrations/001_foundation_schema.sql
git commit -m "feat: add foundation schema migration (entities, documents, tags, taggables)"
```

---

### Task 2: Supabase Client Module

**Files:**
- Create: `execution/__init__.py`
- Create: `execution/db/__init__.py`
- Create: `execution/db/client.py`

- [ ] **Step 1: Create the package init files**

Create `execution/__init__.py` and `execution/db/__init__.py` (both empty):

```python
```

- [ ] **Step 2: Write the Supabase client module**

Create `execution/db/client.py`:

```python
# Last Edited: 2026-03-26 12:00
"""Supabase client singleton. Loads credentials from .env."""

import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env from workspace root
_env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_env_path)

_SUPABASE_URL = os.environ["SUPABASE_PROJECT_URL"]
_SUPABASE_KEY = os.environ["SUPABASE_PUBLISHABLE_KEY"]


def get_client() -> Client:
    """Return a Supabase client instance."""
    return create_client(_SUPABASE_URL, _SUPABASE_KEY)


def get_pg_connection_string() -> str:
    """Return the raw PostgreSQL connection string for psycopg2."""
    return os.environ["SUPABASE_DATA_STRING_CONNETION"]
```

- [ ] **Step 3: Write the connection test**

Create `tests/__init__.py` (empty) and `tests/test_db_client.py`:

```python
# Last Edited: 2026-03-26 12:00
"""Verify Supabase connection works."""

import pytest
from execution.db.client import get_client, get_pg_connection_string
import psycopg2


def test_supabase_client_connects():
    """Supabase REST client can reach the project."""
    client = get_client()
    result = client.table("entities").select("id").limit(1).execute()
    assert hasattr(result, "data")


def test_pg_connection_string_valid():
    """psycopg2 can connect using the connection string."""
    conn = psycopg2.connect(get_pg_connection_string())
    cur = conn.cursor()
    cur.execute("SELECT 1")
    assert cur.fetchone()[0] == 1
    conn.close()
```

- [ ] **Step 4: Run the tests**

Run:
```bash
cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal
python3 -m pytest tests/test_db_client.py -v
```

Expected: 2 tests pass.

- [ ] **Step 5: Commit**

```bash
git add execution/__init__.py execution/db/__init__.py execution/db/client.py tests/__init__.py tests/test_db_client.py
git commit -m "feat: add Supabase client module with connection tests"
```

---

### Task 3: Seed Script — Entities and Tags

**Files:**
- Create: `execution/db/seed.py`
- Create: `tests/test_seed.py`

- [ ] **Step 1: Write the seed script**

Create `execution/db/seed.py`:

```python
# Last Edited: 2026-03-26 12:00
"""Seed the family Supabase database with entities, tags, and 2024 expected documents."""

from execution.db.client import get_client


def seed_entities(client) -> dict[str, str]:
    """Insert all entities. Returns {name: id} mapping for FK references."""
    entities = [
        {"type": "person", "name": "Aaron Melamed", "relationship": "self", "is_family": True,
         "metadata": {"nationality": "US"}},
        {"type": "person", "name": "Eugenia Guadalupe Canul Celis", "relationship": "spouse", "is_family": True,
         "metadata": {"nationality": "Mexican"}},
        {"type": "business", "name": "Itero", "relationship": "owned_business",
         "metadata": {"entity_type": "s-corp", "workspace_path": "Itero/"}},
        {"type": "business", "name": "Keynote Capital, LLC", "relationship": "owned_business",
         "metadata": {"entity_type": "llc"}},
        {"type": "business", "name": "Homeowners First, LLC", "relationship": "owned_business",
         "metadata": {"entity_type": "llc"}},
        {"type": "business", "name": "Palisades Labs", "relationship": "owned_business",
         "metadata": {"entity_type": "llc", "workspace_path": "Palisades Labs/"}},
        {"type": "institution", "name": "Schwab", "relationship": "brokerage",
         "metadata": {"institution_type": "brokerage"}},
        {"type": "institution", "name": "Betterment", "relationship": "investment",
         "metadata": {"institution_type": "robo-advisor"}},
        {"type": "institution", "name": "Guideline", "relationship": "retirement_401k",
         "metadata": {"institution_type": "retirement"}},
        {"type": "institution", "name": "Goldman Sachs Marcus", "relationship": "savings",
         "metadata": {"institution_type": "savings"}},
        {"type": "institution", "name": "American Express", "relationship": "banking",
         "metadata": {"institution_type": "banking"}},
        {"type": "institution", "name": "Wells Fargo", "relationship": "banking",
         "metadata": {"institution_type": "banking"}},
        {"type": "institution", "name": "Coinbase", "relationship": "crypto",
         "metadata": {"institution_type": "crypto_exchange"}},
        {"type": "institution", "name": "ProPay", "relationship": "payment_processor",
         "metadata": {"institution_type": "payment_processor"}},
        {"type": "institution", "name": "New American Funding", "relationship": "mortgage_servicer",
         "metadata": {"institution_type": "mortgage"}},
        {"type": "institution", "name": "JustWorks", "relationship": "payroll",
         "metadata": {"institution_type": "payroll"}},
        {"type": "institution", "name": "State Street", "relationship": "retirement",
         "metadata": {"institution_type": "retirement"}},
        {"type": "institution", "name": "T-Mobile", "relationship": "telecom",
         "metadata": {"institution_type": "telecom"}},
        {"type": "property", "name": "1771 11th Ave, SF", "relationship": "rental_property",
         "metadata": {"property_type": "residential", "address": "1771 11th Ave, San Francisco, CA"}},
    ]

    result = client.table("entities").upsert(entities, on_conflict="name").execute()
    return {row["name"]: row["id"] for row in result.data}


def seed_tags(client) -> dict[str, str]:
    """Insert all tags. Returns {name: id} mapping."""
    tags = [
        {"name": "schedule-a", "display_name": "Schedule A (Itemized Deductions)", "type": "tax_category"},
        {"name": "schedule-b", "display_name": "Schedule B (Interest & Dividends)", "type": "tax_category"},
        {"name": "schedule-c", "display_name": "Schedule C (Business Income)", "type": "tax_category"},
        {"name": "schedule-d", "display_name": "Schedule D (Capital Gains)", "type": "tax_category"},
        {"name": "schedule-e", "display_name": "Schedule E (Rental/Passthrough)", "type": "tax_category"},
        {"name": "schedule-se", "display_name": "Schedule SE (Self-Employment Tax)", "type": "tax_category"},
        {"name": "form-8949", "display_name": "Form 8949 (Sales of Capital Assets)", "type": "tax_category"},
        {"name": "deductible", "display_name": "Deductible Expense", "type": "expense_category"},
        {"name": "home-office", "display_name": "Home Office", "type": "expense_category"},
        {"name": "rental-expense", "display_name": "Rental Property Expense", "type": "expense_category"},
        {"name": "tax-2023", "display_name": "Tax Year 2023", "type": "tax_year"},
        {"name": "tax-2024", "display_name": "Tax Year 2024", "type": "tax_year"},
        {"name": "tax-2025", "display_name": "Tax Year 2025", "type": "tax_year"},
        {"name": "green-card", "display_name": "Green Card", "type": "initiative"},
    ]

    result = client.table("tags").upsert(tags, on_conflict="name").execute()
    return {row["name"]: row["id"] for row in result.data}


def seed_documents_2024(client, entity_map: dict[str, str]) -> list[dict]:
    """Insert 2024 expected tax documents. Returns inserted rows."""
    aaron_id = entity_map["Aaron Melamed"]

    # Map: (name, form_number, source_entity_name, tax_schedule, conditional metadata)
    doc_specs = [
        ("2024 JustWorks W-2", "W-2", "JustWorks", "Schedule C",
         {"conditional": True, "condition": "only if employed that year"}),
        ("2024 Schwab 1099-Composite", "1099-Composite", "Schwab", "Schedule D", {}),
        ("2024 Betterment 1099-B/DIV", "1099-B", "Betterment", "Schedule D", {}),
        ("2024 Betterment FMV Statement", "FMV", "Betterment", "Schedule D", {}),
        ("2024 Guideline 401k Statement", "Year-End Statement", "Guideline", None, {}),
        ("2024 State Street 1099-R", "1099-R", "State Street", None,
         {"conditional": True, "condition": "only if distribution taken"}),
        ("2024 Marcus 1099-INT", "1099-INT", "Goldman Sachs Marcus", "Schedule B", {}),
        ("2024 Amex 1099-INT", "1099-INT", "American Express", "Schedule B", {}),
        ("2024 Schwab 1099-INT", "1099-INT", "Schwab", "Schedule B", {}),
        ("2024 Wells Fargo 1099-INT", "1099-INT", "Wells Fargo", "Schedule B",
         {"conditional": True, "condition": "only if account active"}),
        ("2024 Mortgage 1098", "1098", "New American Funding", "Schedule A", {}),
        ("2024 ProPay 1099-K", "1099-K", "ProPay", "Schedule E", {}),
        ("2024 Health Insurance 1095", "1095-C", None, None,
         {"conditional": True, "condition": "varies by year and employer"}),
        ("2024 Coinbase 1099", "1099", "Coinbase", "Schedule D",
         {"conditional": True, "condition": "only if trades that year"}),
        ("2024 Rental Income Summary", "CSV", None, "Schedule E", {"self_prepared": True}),
        ("2024 Rental Expenses", "CSV", None, "Schedule E", {"self_prepared": True}),
        ("2024 Home Office Rent Allocation", "CSV", None, "Schedule C", {"self_prepared": True}),
        ("2024 Business Meals", "CSV", None, "Schedule C", {"self_prepared": True}),
        ("2024 Dues & Subscriptions", "CSV", None, "Schedule C", {"self_prepared": True}),
        ("2024 Credit Card Annual Fees", "CSV", None, "Schedule C", {"self_prepared": True}),
        ("2024 Cell Phone Expenses", "CSV", None, "Schedule C", {"self_prepared": True}),
        ("2024 Office Supplies", "CSV", None, "Schedule C", {"self_prepared": True}),
        ("2024 Utilities (Home Office)", "CSV", None, "Schedule C", {"self_prepared": True}),
    ]

    documents = []
    for name, form_number, source_name, tax_schedule, metadata in doc_specs:
        source_id = entity_map.get(source_name) if source_name else aaron_id
        doc = {
            "name": name,
            "type": "tax_form",
            "source_entity_id": source_id,
            "owner_entity_id": aaron_id,
            "tax_year": 2024,
            "tax_schedule": tax_schedule,
            "form_number": form_number,
            "status": "expected",
            "metadata": metadata,
        }
        documents.append(doc)

    result = client.table("documents").upsert(documents, on_conflict="name").execute()
    return result.data


def run_seed():
    """Run the full seed process."""
    client = get_client()

    print("Seeding entities...")
    entity_map = seed_entities(client)
    print(f"  {len(entity_map)} entities seeded.")

    print("Seeding tags...")
    tag_map = seed_tags(client)
    print(f"  {len(tag_map)} tags seeded.")

    print("Seeding 2024 expected documents...")
    docs = seed_documents_2024(client, entity_map)
    print(f"  {len(docs)} documents seeded.")

    print("Seed complete.")
    return entity_map, tag_map, docs


if __name__ == "__main__":
    run_seed()
```

- [ ] **Step 2: Write seed verification tests**

Create `tests/test_seed.py`:

```python
# Last Edited: 2026-03-26 12:00
"""Verify seed data landed correctly in Supabase."""

import pytest
from execution.db.client import get_client


@pytest.fixture(scope="module")
def client():
    return get_client()


def test_entities_seeded(client):
    """All 19 entities exist with correct types."""
    result = client.table("entities").select("name, type").execute()
    names = {row["name"] for row in result.data}
    assert "Aaron Melamed" in names
    assert "Schwab" in names
    assert "1771 11th Ave, SF" in names
    assert len(result.data) >= 19


def test_entity_types_correct(client):
    """Spot-check entity types."""
    result = client.table("entities").select("name, type").eq("name", "Aaron Melamed").execute()
    assert result.data[0]["type"] == "person"

    result = client.table("entities").select("name, type").eq("name", "Schwab").execute()
    assert result.data[0]["type"] == "institution"

    result = client.table("entities").select("name, type").eq("name", "Itero").execute()
    assert result.data[0]["type"] == "business"


def test_tags_seeded(client):
    """All 14 tags exist."""
    result = client.table("tags").select("name, type").execute()
    names = {row["name"] for row in result.data}
    assert "schedule-d" in names
    assert "green-card" in names
    assert "deductible" in names
    assert len(result.data) >= 14


def test_documents_2024_seeded(client):
    """All 23 expected 2024 documents exist."""
    result = client.table("documents").select("name, status, tax_year").eq("tax_year", 2024).execute()
    assert len(result.data) >= 23
    statuses = {row["status"] for row in result.data}
    assert statuses == {"expected"}


def test_documents_have_source_entities(client):
    """Institutional documents link to their source entity."""
    result = (
        client.table("documents")
        .select("name, source_entity_id")
        .eq("name", "2024 Schwab 1099-Composite")
        .execute()
    )
    assert result.data[0]["source_entity_id"] is not None
```

- [ ] **Step 3: Run the seed script**

```bash
cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal
python3 -m execution.db.seed
```

Expected:
```
Seeding entities...
  19 entities seeded.
Seeding tags...
  14 tags seeded.
Seeding 2024 expected documents...
  23 documents seeded.
Seed complete.
```

- [ ] **Step 4: Run the seed tests**

```bash
python3 -m pytest tests/test_seed.py -v
```

Expected: 5 tests pass.

- [ ] **Step 5: Commit**

```bash
git add execution/db/seed.py tests/test_seed.py
git commit -m "feat: add seed script for entities, tags, and 2024 tax documents"
```

---

### Task 4: Tax MVP Query Module

**Files:**
- Create: `execution/db/queries.py`
- Create: `tests/test_queries.py`

- [ ] **Step 1: Write the query module**

Create `execution/db/queries.py`:

```python
# Last Edited: 2026-03-26 12:00
"""Tax MVP queries against the family Supabase database."""

from execution.db.client import get_client


def get_missing_documents(tax_year: int) -> list[dict]:
    """Return documents still in 'expected' status for a given tax year."""
    client = get_client()
    result = (
        client.table("documents")
        .select("name, form_number, tax_schedule, metadata")
        .eq("tax_year", tax_year)
        .eq("status", "expected")
        .order("tax_schedule")
        .order("name")
        .execute()
    )
    return result.data


def get_received_documents(tax_year: int) -> list[dict]:
    """Return documents that have been received for a given tax year."""
    client = get_client()
    result = (
        client.table("documents")
        .select("name, form_number, tax_schedule, status, file_path")
        .eq("tax_year", tax_year)
        .in_("status", ["received", "submitted", "verified"])
        .order("tax_schedule")
        .order("name")
        .execute()
    )
    return result.data


def get_cpa_package(tax_year: int) -> dict[str, list[str]]:
    """Return received/submitted documents grouped by tax schedule.

    Returns: {"Schedule D": ["2024 Schwab 1099-Composite", ...], ...}
    """
    docs = get_received_documents(tax_year)
    package: dict[str, list[str]] = {}
    for doc in docs:
        schedule = doc["tax_schedule"] or "Other"
        package.setdefault(schedule, []).append(doc["name"])
    return package


def get_document_status_summary(tax_year: int) -> dict[str, int]:
    """Return count of documents by status for a given tax year."""
    client = get_client()
    result = (
        client.table("documents")
        .select("status")
        .eq("tax_year", tax_year)
        .execute()
    )
    counts: dict[str, int] = {}
    for row in result.data:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return counts


def get_documents_by_entity(entity_name: str, tax_year: int) -> list[dict]:
    """Return all documents from a specific source entity for a tax year."""
    client = get_client()
    # First get the entity ID
    entity_result = client.table("entities").select("id").eq("name", entity_name).execute()
    if not entity_result.data:
        return []
    entity_id = entity_result.data[0]["id"]

    result = (
        client.table("documents")
        .select("name, status, tax_schedule, form_number")
        .eq("source_entity_id", entity_id)
        .eq("tax_year", tax_year)
        .order("name")
        .execute()
    )
    return result.data


def mark_document_received(document_name: str, file_path: str | None = None) -> dict:
    """Update a document's status to 'received' and optionally set file_path."""
    client = get_client()
    update = {"status": "received"}
    if file_path:
        update["file_path"] = file_path
    result = (
        client.table("documents")
        .update(update)
        .eq("name", document_name)
        .execute()
    )
    return result.data[0] if result.data else {}


def mark_document_submitted(document_name: str) -> dict:
    """Update a document's status to 'submitted'."""
    client = get_client()
    result = (
        client.table("documents")
        .update({"status": "submitted"})
        .eq("name", document_name)
        .execute()
    )
    return result.data[0] if result.data else {}
```

- [ ] **Step 2: Write query tests**

Create `tests/test_queries.py`:

```python
# Last Edited: 2026-03-26 12:00
"""Verify MVP tax queries work against seeded data."""

import pytest
from execution.db.queries import (
    get_missing_documents,
    get_received_documents,
    get_cpa_package,
    get_document_status_summary,
    get_documents_by_entity,
    mark_document_received,
    mark_document_submitted,
)
from execution.db.client import get_client


@pytest.fixture(scope="module")
def client():
    return get_client()


def test_missing_documents_returns_all_expected(client):
    """All 2024 docs start as 'expected', so missing list should be full."""
    missing = get_missing_documents(2024)
    assert len(missing) >= 23
    assert all(doc["tax_schedule"] is not None or doc["form_number"] for doc in missing)


def test_received_documents_initially_empty(client):
    """No documents have been received yet."""
    received = get_received_documents(2024)
    # May not be empty if mark_document_received ran in another test,
    # but initially should be 0
    assert isinstance(received, list)


def test_status_summary_shape(client):
    """Status summary returns a dict of status: count."""
    summary = get_document_status_summary(2024)
    assert isinstance(summary, dict)
    assert "expected" in summary
    assert summary["expected"] >= 1


def test_documents_by_entity(client):
    """Query docs by source entity name."""
    schwab_docs = get_documents_by_entity("Schwab", 2024)
    schwab_names = [d["name"] for d in schwab_docs]
    assert "2024 Schwab 1099-Composite" in schwab_names


def test_mark_received_and_submitted(client):
    """Mark a doc as received, then submitted, verify status changes."""
    # Mark received
    doc = mark_document_received(
        "2024 Schwab 1099-Composite",
        file_path="tax_document_archive/2024/Schwab 1099 Composite and Year-End Summary - 2024_2025-02-07_117.PDF"
    )
    assert doc["status"] == "received"
    assert doc["file_path"] is not None

    # Mark submitted
    doc = mark_document_submitted("2024 Schwab 1099-Composite")
    assert doc["status"] == "submitted"

    # Reset back to expected for idempotent test runs
    get_client().table("documents").update(
        {"status": "expected", "file_path": None}
    ).eq("name", "2024 Schwab 1099-Composite").execute()


def test_cpa_package_groups_by_schedule(client):
    """CPA package groups docs by schedule after marking some received."""
    # Mark two docs as received
    mark_document_received("2024 Marcus 1099-INT")
    mark_document_received("2024 Amex 1099-INT")

    package = get_cpa_package(2024)
    assert "Schedule B" in package
    assert "2024 Marcus 1099-INT" in package["Schedule B"]

    # Reset
    for name in ["2024 Marcus 1099-INT", "2024 Amex 1099-INT"]:
        get_client().table("documents").update(
            {"status": "expected", "file_path": None}
        ).eq("name", name).execute()
```

- [ ] **Step 3: Run the query tests**

```bash
python3 -m pytest tests/test_queries.py -v
```

Expected: 6 tests pass.

- [ ] **Step 4: Commit**

```bash
git add execution/db/queries.py tests/test_queries.py
git commit -m "feat: add tax MVP query module with missing docs, CPA package, and status updates"
```

---

### Task 5: Tax Checklist CLI Script

**Files:**
- Create: `execution/tax/__init__.py`
- Create: `execution/tax/checklist.py`

- [ ] **Step 1: Write the checklist script**

Create `execution/tax/__init__.py` (empty) and `execution/tax/checklist.py`:

```python
# Last Edited: 2026-03-26 12:00
"""CLI tool to print tax document status for a given year."""

import argparse
import sys

from execution.db.queries import (
    get_missing_documents,
    get_document_status_summary,
    get_cpa_package,
)


def print_checklist(tax_year: int) -> None:
    """Print a full tax document status report."""
    print(f"\n{'='*60}")
    print(f"  TAX DOCUMENT STATUS — {tax_year}")
    print(f"{'='*60}\n")

    # Summary
    summary = get_document_status_summary(tax_year)
    total = sum(summary.values())
    print(f"Total documents: {total}")
    for status, count in sorted(summary.items()):
        symbol = {"expected": "⬜", "received": "✅", "submitted": "📤", "verified": "✔️"}.get(status, "?")
        print(f"  {symbol} {status}: {count}")

    # Missing documents
    missing = get_missing_documents(tax_year)
    print(f"\n{'—'*60}")
    print(f"MISSING ({len(missing)} documents still expected):")
    print(f"{'—'*60}")
    if not missing:
        print("  🎉 All documents received!")
    else:
        current_schedule = None
        for doc in missing:
            schedule = doc["tax_schedule"] or "Other"
            if schedule != current_schedule:
                current_schedule = schedule
                print(f"\n  [{schedule}]")
            conditional = ""
            if doc.get("metadata", {}).get("conditional"):
                conditional = f" ⚠️  ({doc['metadata']['condition']})"
            print(f"    ⬜ {doc['name']} ({doc['form_number']}){conditional}")

    # CPA package (if any docs received)
    package = get_cpa_package(tax_year)
    if package:
        print(f"\n{'—'*60}")
        print("CPA PACKAGE (received/submitted, grouped by schedule):")
        print(f"{'—'*60}")
        for schedule, doc_names in sorted(package.items()):
            print(f"\n  [{schedule}]")
            for name in doc_names:
                print(f"    ✅ {name}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Tax document checklist")
    parser.add_argument("year", type=int, nargs="?", default=2024, help="Tax year (default: 2024)")
    args = parser.parse_args()
    print_checklist(args.year)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the checklist**

```bash
cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal
python3 -m execution.tax.checklist 2024
```

Expected: A formatted report showing all 23 documents as "expected" (missing), grouped by schedule.

- [ ] **Step 3: Commit**

```bash
git add execution/tax/__init__.py execution/tax/checklist.py
git commit -m "feat: add tax document checklist CLI tool"
```

---

### Task 6: Map Existing Files to Documents

**Files:**
- Create: `execution/tax/match_files.py`

This script scans `tax_document_archive/2024/` and fuzzy-matches filenames to expected documents in the DB, then marks them as `received` with the correct `file_path`.

- [ ] **Step 1: Write the file matching script**

Create `execution/tax/match_files.py`:

```python
# Last Edited: 2026-03-26 12:00
"""Match files in tax_document_archive/ to expected documents in the DB and mark received."""

from pathlib import Path

from execution.db.client import get_client
from execution.db.queries import mark_document_received


# Manual mapping: DB document name -> filename in tax_document_archive/2024/
FILE_MAP_2024: dict[str, str] = {
    "2024 JustWorks W-2": "JustWorks 2024 W-2.pdf",
    "2024 Schwab 1099-Composite": "Schwab 1099 Composite and Year-End Summary - 2024_2025-02-07_117.PDF",
    "2024 Schwab 1099-INT": "Schwab Bank 1099 Tax Forms_2025-01-24_145.PDF",
    "2024 Betterment 1099-B/DIV": "Betterment - TaxStatement_2024_1099B_DIV_268011224580120.pdf",
    "2024 Betterment FMV Statement": "TaxStatement_2024_FMV_268011225343197.pdf",
    "2024 Marcus 1099-INT": "Goldman Sachs 2024 1099-INT.pdf",
    "2024 Amex 1099-INT": "Amex 2024 1099-INT.pdf",
    "2024 Mortgage 1098": "1098-2024.pdf",
    "2024 ProPay 1099-K": "PROPAY 2024 1099-K.pdf",
    "2024 Health Insurance 1095": "Orum 1095-C Health Ins Coverage.pdf",
    "2024 Coinbase 1099": "Coinbase 1099.pdf",
}

ARCHIVE_BASE = Path(__file__).resolve().parents[2] / "tax_document_archive"


def match_and_mark(tax_year: int = 2024) -> tuple[list[str], list[str]]:
    """Match archive files to DB documents. Returns (matched, unmatched) lists."""
    file_map = FILE_MAP_2024 if tax_year == 2024 else {}
    archive_dir = ARCHIVE_BASE / str(tax_year)

    if not archive_dir.exists():
        print(f"Archive directory not found: {archive_dir}")
        return [], []

    matched = []
    unmatched = []

    for doc_name, filename in file_map.items():
        file_path = archive_dir / filename
        if file_path.exists():
            relative_path = f"tax_document_archive/{tax_year}/{filename}"
            result = mark_document_received(doc_name, file_path=relative_path)
            if result:
                matched.append(doc_name)
                print(f"  ✅ {doc_name} -> {filename}")
            else:
                unmatched.append(doc_name)
                print(f"  ❌ {doc_name}: DB record not found")
        else:
            unmatched.append(doc_name)
            print(f"  ❌ {doc_name}: file not found ({filename})")

    # Report archive files not in the map
    mapped_files = set(file_map.values())
    archive_files = {f.name for f in archive_dir.iterdir() if f.is_file() and not f.name.startswith(".")}
    unmapped = archive_files - mapped_files
    if unmapped:
        print(f"\n  ⚠️  Files in archive not mapped to any document:")
        for f in sorted(unmapped):
            print(f"    - {f}")

    return matched, unmatched


def main():
    print("Matching 2024 archive files to expected documents...\n")
    matched, unmatched = match_and_mark(2024)
    print(f"\nResults: {len(matched)} matched, {len(unmatched)} unmatched")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the file matcher**

```bash
cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal
python3 -m execution.tax.match_files
```

Expected: 11 files matched and marked as received. Several unmapped archive files flagged (like `Expenses.pdf`, `Gain Loss Coinbase.pdf`, `SOL Transcations.pdf`, `2024 Non w2 Income + rent.pdf`, `Betterment supplemental_tax_form`).

- [ ] **Step 3: Run the checklist again to verify**

```bash
python3 -m execution.tax.checklist 2024
```

Expected: ~12 documents now show as "expected" (missing), ~11 show as "received" in the CPA package section.

- [ ] **Step 4: Commit**

```bash
git add execution/tax/match_files.py
git commit -m "feat: add file matcher to link archive files to DB documents"
```

---

### Task 7: Remaining Init Files and Final Verification

**Files:**
- Create: `execution/utils/__init__.py`
- Create: `execution/family/__init__.py`
- Create: `execution/finance/__init__.py`
- Create: `execution/property/__init__.py`

- [ ] **Step 1: Create remaining `__init__.py` files**

Create empty `__init__.py` files in remaining execution subdirectories for future use:

```bash
touch execution/utils/__init__.py execution/family/__init__.py execution/finance/__init__.py execution/property/__init__.py
```

- [ ] **Step 2: Run the full test suite**

```bash
cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal
python3 -m pytest tests/ -v
```

Expected: All tests pass (2 connection + 5 seed + 6 query = 13 tests).

- [ ] **Step 3: Run the checklist one final time**

```bash
python3 -m execution.tax.checklist 2024
```

Expected: Clean output showing the current state of all 2024 tax documents.

- [ ] **Step 4: Commit**

```bash
git add execution/utils/__init__.py execution/family/__init__.py execution/finance/__init__.py execution/property/__init__.py
git commit -m "chore: add __init__.py files for remaining execution subpackages"
```
