---
name: tax-status
description: "Check tax document collection status. Conditional-aware gap reporting using the master checklist as source of truth. Shows matched, missing, not-expected, and reference documents separately."
user-invocable: true
---

# Tax Status

*Last Edited: 2026-03-29*

Check document collection progress for a given tax year. Uses the master checklist as the single source of truth. Conditional items that are disabled show as "not expected" rather than gaps. Reference docs are informational only.

## Prerequisites

- `config/tax_documents_master.yaml` exists (master checklist)
- `config/tax_config.yaml` exists (per-year config with conditional flags)
- Tax archive directory: `tax_document_archive/{year}/`

## Workflow

### Step 1: Parse the Request

Extract the tax year from the user's request:
- "tax status 2025" → year 2025
- "tax status" → default to current year minus 1
- "what's missing for taxes" → default to current year minus 1

### Step 2: Check if Tax Year is Initialized

Read `config/tax_config.yaml` and check if the tax year has `initialized: true`.

**If not initialized → run setup:**

1. Read the master checklist at `config/tax_documents_master.yaml`
2. Ask the user which institutions are active this year
3. Ask which conditional items apply:
   - Receiving a W-2 this year? If yes, from which employer/PEO?
   - Crypto trades this year?
   - Any other conditional items?
4. Update `config/tax_config.yaml` with the answers
5. Seed expected documents:
   ```bash
   python3 -m execution.tax.seed_tax_year --year {year}
   ```
6. Confirm: "{N} expected documents seeded for tax year {year}."

**If already initialized → skip to Step 3.**

### Step 3: Run Conditional-Aware Match

Run the file matcher with dry-run to see results without side effects:
```bash
python3 -m execution.tax.match_files --year {year} --dry-run
```

The matcher loads `tax_config.yaml` to evaluate conditional items and returns four result sets: matched files, unmapped files, reference doc results, and skipped conditionals.

### Step 4: Status Report

Present results in four sections:

**MATCHED** — Documents found in the archive with filenames:
```
[x] Schwab 1099-B  →  schwab-1099-b-2025.pdf
[x] Betterment 1099-DIV  →  betterment-1099-div-2025.pdf
```

**MISSING** — Expected documents not yet in archive, with arrival dates:
```
[ ] Guideline 401k-5498  (expected: late Jan)
[ ] Coinbase 1099-MISC  (expected: mid-Feb)
```

**NOT EXPECTED** — Disabled conditionals with reasons:
```
[n/a] W-2  — no W-2 employment this year
[n/a] 1099-SA  — no HSA distributions
```

**REFERENCE** — Informational documents (not counted in gap totals):
```
[ref] Prior year return  →  2024-return-copy.pdf
[ref] Extension filing  →  not found
```

**UNMATCHED** — Archive files that don't match any checklist spec:
```
[?] mystery-document.pdf
[?] scan-20250301.pdf
```

Summary line: "X of Y expected documents collected. Z gaps remaining."
- Gap count excludes reference docs and disabled conditionals.

### Step 5: Next Actions

**If unmatched files exist:**
- Suggest: "Run `/ingest-tax-docs` to auto-identify unmatched files via OCR."

**If gaps remain:**
- Show what's missing with deadlines and portal hints where known.

**If collection is complete (zero gaps):**
- Suggest: "Run `/train-categories` to verify Monarch transaction categorization before CPA handoff."

## Error Handling

| Error | Fix |
|---|---|
| Archive directory missing | Create `tax_document_archive/{year}/` and instruct user to add files |
| Config not found | Verify `config/tax_config.yaml` and `config/tax_documents_master.yaml` exist |
| No documents seeded | Run Step 2 setup flow to initialize the tax year |
| Unmatched archive files | Run `/ingest-tax-docs` to auto-identify via OCR |

## Acceptance Checks

- Disabled conditionals show as "not expected" (never as "missing")
- Reference docs shown separately from the gap report (not counted in gap totals)
- Master checklist (`config/tax_documents_master.yaml`) is the source of truth — not prior year comparison

## Reference

- **Master checklist**: `config/tax_documents_master.yaml`
- **Per-year config**: `config/tax_config.yaml`
- **Archive location**: `tax_document_archive/{year}/`
- **Matcher**: `execution/tax/match_files.py`
