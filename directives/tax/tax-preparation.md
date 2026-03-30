*Last Edited: 2026-03-29*

# Tax Preparation — Annual Workflow

6-phase skill pipeline. Run January → April each year. Goal: deliver a clean, pre-extracted tax package to the CPA with minimal billable hours.

---

## Overview

| Item | Value |
|------|-------|
| **Master checklist** | `config/tax_documents_master.yaml` |
| **Per-year config** | `config/tax_config.yaml` |
| **Archive** | `tax_document_archive/{year}/` |
| **DB tracking** | Supabase `documents` table (expected → received → extracted → submitted → verified) |
| **CPA** | Jessica. Interaction via email + client portal. |

---

## The 6 Skills

| # | Skill | Phase | When | Status |
|---|-------|-------|------|--------|
| 1 | `/setup-tax-year` | Setup | January | Update existing `/seed-tax-project` |
| 2 | `/ingest-tax-docs` | Collection | Jan–Mar (repeat) | **Build new** |
| 3 | `/tax-status` | Collection | Anytime | Update existing `/prep-tax-package` |
| 4 | `/train-categories` | Categorization | Mar–Apr | Working |
| 5 | `/extract-tax-forms` | Extraction | April | **Build new** |
| 6 | `/deliver-to-cpa` | Delivery | April | **Build new** (MVP: PDF, no portal) |

---

## Phase 1: Setup (January)

**Skill:** `/setup-tax-year {year}`

1. Confirm active institutions and conditional items for the year:
   - Receiving a W-2? From which employer/PEO?
   - PEO situation? (separate `employer_name` for W-2 vs `employer_1095c_name` for 1095-C)
   - Crypto trades? (Coinbase 1099, gain/loss, transaction history)
   - Guideline 401k contributions?
   - ProPay 1099-K issued?
   - Schwab Bank above 1099-INT threshold?
2. Update `config/tax_config.yaml` with the year's settings
3. Refresh portal data via Tavily (stale entries in `config/institution_portals.yaml`)
4. Seed expected documents into Supabase (`seed_tax_year.py`)
5. Create Asana project with download tasks + portal links (`asana_tasks.py`)

**Tools:** `seed_tax_year.py`, `asana_tasks.py`, Tavily

---

## Phase 2: Document Collection (January — March)

**Skills:** `/ingest-tax-docs {year}`, `/tax-status {year}`

### Ingestion (`/ingest-tax-docs`)

Aaron downloads PDFs from institution portals and drops them into `tax_document_archive/{year}/`.

1. Scan archive for un-renamed files (not matching canonical pattern)
2. Pattern match first (fast, no OCR cost) via `rename_docs.py`
3. For remaining unmatched PDFs, run OCR identification via `identify_pdf.py`
4. **High confidence** → auto-rename. **Medium/low** → present to user, leave unrenamed until confirmed
5. Always dry-run first. Rollback manifest written before any renames applied.
6. Show updated gap status via `match_files.py --dry-run`

**Tools:** `rename_docs.py`, `identify_pdf.py`, `match_files.py`

### Status (`/tax-status`)

Conditional-aware gap reporting. Master checklist is the source of truth.

- **Matched:** documents found in archive
- **Missing:** expected documents not yet in archive
- **Not expected:** disabled conditional items (with reason)
- **Reference:** informational docs shown separately (not in gap count)

**Tools:** `match_files.py`, `checklist.py`

---

## Phase 3: Transaction Categorization (March — April)

**Skill:** `/train-categories`

Multi-signal categorization engine pulls live from Monarch Money and classifies transactions using 7 signals:

1. Monarch rules (`config/monarch_rules.yaml` — 204 rules)
2. Schedule map (`config/categorization_rules.yaml`)
3. Account type (business vs personal card)
4. Recurring patterns (same merchant + amount monthly)
5. Historical consistency (merchant always → same category)
6. Tap detection (garbled Mexico City merchants)
7. Plausibility checks (utility whitelist, generic payment detection, foreign merchant flags)

**Training loop:** Present batches → Aaron gives feedback → rules tighten → dry-run → explicit approval → audit logged → rollback available.

**Safety:** All Monarch writes are dry-run by default. Every change logged to `config/categorization_audit_{year}.yaml`.

**Tools:** `monarch_client.py`, `categorize.py`

---

## Phase 4: PDF Extraction (April)

**Skill:** `/extract-tax-forms {year}`

For each institutional PDF in the archive:

1. **Google Document AI OCR** extracts raw text (`extract_pdf.py`)
2. **Claude Vision** reads the PDF and extracts structured fields using form-specific prompts (`config/extraction_prompts/`)
3. **Reconciliation** compares OCR and Vision field-by-field:
   - Both agree → `verified`
   - Disagree → `disputed` (flagged for review)
   - Only one source → `single_source`
4. Results stored in Supabase `documents.metadata`

**Extraction prompts available:** 1098, 1099-B/DIV, 1099-Composite, 1099-INT, 1099-K

**Extraction prompts needed:** 1099-MISC, 5498-FMV

**Tools:** `extract_pdf.py`, extraction prompts, Supabase

---

## Phase 5: Verification (April)

Aaron reviews two things:

1. **Transaction totals** — run categorization summary, scan schedule-by-schedule
2. **Extracted PDF values** — review extracted fields, resolve any disputed values

---

## Phase 6: CPA Delivery (April)

**Skill:** `/deliver-to-cpa {year}`

**MVP (no portal dependency):**
1. Generate PDF cover document grouped by tax schedule (`CoverDocument` model)
2. Verify completeness: all expected docs received, all required fields extracted
3. **Block on unresolved disputed fields** — won't generate if disputes remain
4. Output: PDF cover doc + completeness report

**Deferred:** Tax portal web app for interactive CPA verification.

### Metadata Contract (Extraction → Delivery)

`documents.metadata` in Supabase:
```json
{
  "extraction_status": "complete | partial | failed",
  "fields": [
    {
      "label": "Box 1 - Interest income",
      "value": "2960.31",
      "confidence": "verified | disputed | single_source",
      "ocr_value": "2960.31",
      "vision_value": "2960.31",
      "schedule_line": "Schedule B, Part I"
    }
  ],
  "disputed_count": 0,
  "extracted_at": "2026-04-01T10:00:00"
}
```

Maps to the existing `ReconciliationResult` model in `execution/tax/models.py`.

---

## Tools Reference

| Tool | Location | Purpose |
|------|----------|---------|
| Rename docs | `execution/tax/rename_docs.py` | Canonical filenames. Dry-run default, `--apply`, `--rollback` |
| Match files | `execution/tax/match_files.py` | Conditional-aware gap reporting |
| Identify PDF | `execution/tax/identify_pdf.py` | OCR classifier — institution, form, year, account |
| OCR extraction | `execution/tax/extract_pdf.py` | Google Document AI |
| Seeder | `execution/tax/seed_tax_year.py` | Seed expected docs into Supabase |
| Asana tasks | `execution/tax/asana_tasks.py` | Create Asana project with portal links |
| Checklist | `execution/tax/checklist.py` | Status report by schedule |
| Monarch client | `execution/finance/monarch_client.py` | Async Monarch Money API |
| Categorization | `execution/finance/categorize.py` | Multi-signal transaction classifier |

## Configuration Reference

| File | Purpose |
|------|---------|
| `config/tax_documents_master.yaml` | Master checklist — institutional, self-prepared, reference specs |
| `config/tax_config.yaml` | Per-year setup — conditionals, parameterized names |
| `config/categorization_rules.yaml` | Schedule map + learned rules |
| `config/monarch_rules.yaml` | 204 Monarch auto-categorization rules |
| `config/institution_portals.yaml` | Portal URLs + click-paths (Tavily-refreshed) |
| `config/extraction_prompts/` | Per-form Claude Vision prompts (5 templates) |
| `config/categorization_audit_{year}.yaml` | Monarch write audit log |

---

## Naming Conventions

All files in `tax_document_archive/{year}/` follow strict naming:

| Type | Pattern | Example |
|------|---------|---------|
| Institutional | `{year}_{institution-slug}_{form-slug}.pdf` | `2025_schwab_1099-composite.pdf` |
| Self-prepared | `{year}_self_{category-slug}.{ext}` | `2025_self_rental-income.csv` |
| Reference | `{year}_ref_{type-slug}.{ext}` | `2024_ref_filed-return.pdf` |

Slugs: lowercase, hyphen-separated. Parenthetical qualifiers stripped (e.g., "Schwab (brokerage)" → `schwab`).

**Multi-account:** When a spec has `multi_account: true`, last 5 digits of account number appended: `2025_betterment_5498-fmv_43197.pdf`

**Form numbers:** Always use the specific IRS form number, not generic labels. Read the PDF to identify it. (e.g., `5498-fmv` not `fmv`, `1099-misc` not `1099`, `1099-supplemental` not `supplemental`)

---

## Scope Exclusions

| Item | Why excluded |
|------|-------------|
| K-1s | Handled via Keynote Capital accounting, directly with CPA. "Keynote Income" in Monarch is reference-only — K-1 is the tax document, not bank deposits. Do NOT put on Schedule C. |
| Reimbursed expenses | In Monarch: "Reimbursed by Keynote" / "Reimbursed by Itero" under Transfers group (net-worth neutral). Excluded from all tax schedules — expense lives on entity's books. Unreimbursed items stay in "Keynote - X" categories on Schedule C. |
| Property taxes | Covered by Monarch transaction data |
| Health insurance premiums | Covered by Monarch transaction data |
| Itero / Palisades Labs income | Not passthrough entities. No income paid in 2025. |
| FEIE / Form 2555 | Aaron's income doesn't qualify |
| FBAR / Form 8938 | Foreign accounts under reporting thresholds |

---

## Not Yet Supported

- Amended/corrected 1099s (current process: replace file, re-extract)
- Mid-year institution changes
- Tax portal web app (Phase 5-6 verification UI)

---

## Lessons Reference

Implementation pitfalls and corrections: `directives/lessons.md`

Key lessons: filename patterns are fragile year-over-year, PEO splits employer identity, use OCR to identify docs (don't ask user), read PDFs for actual IRS form numbers.
