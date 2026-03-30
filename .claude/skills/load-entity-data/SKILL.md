---
name: load-entity-data
description: Load business entity financial data (QBO export JSON) into Supabase for the CPA verify tab. Use when the user says "load entity data", "put Keynote/DemandDraft data into verify", "load QBO data", or after running keynote_tax_export.py.
user-invocable: true
---

# Load Entity Data

Loads a QBO tax summary JSON into Supabase as document records with extracted fields. The `/verify` page renders them automatically alongside PDF-extracted forms and Monarch data.

## Prerequisites

- `SUPABASE_PROJECT_URL` and `SUPABASE_SERVICE_ROLE_KEY` in `.env`
- QBO export JSON exists at `tax_document_archive/{year}/{entity}_tax_summary_{year}.json`
- Entity seeded in Supabase `entities` table (run `execution/db/seed.py` if not)

## Workflow

### Step 1: Parse the Request

Extract parameters:
- **Entity**: "Keynote Capital" (default), or another business entity name
- **Year**: Extract from request, or default to current year minus 1

### Step 2: Check the JSON Export Exists

```bash
ls tax_document_archive/{year}/keynote_tax_summary_{year}.json
```

If missing, tell the user to run the QBO export first:
```bash
python3 -m execution.keynote_tax_export --year {year}
```

### Step 3: Run the Load Script

```bash
python3 -m execution.tax.load_qbo_to_supabase --year {year}
```

This creates 3 document records in Supabase:
1. **P&L Summary** (Schedule E) — income, expense breakdown, net income
2. **Distributions to Aaron** (Schedule E) — guaranteed payments, profit share, clearing
3. **Interest Income** (Schedule B) — bank interest by account

### Step 4: Report Results

Show the user:
- Number of documents loaded and field counts
- Any validation warnings (disputed fields)
- Remind them to check `/verify`

If the script exits nonzero, there are validation mismatches. The data is still loaded but affected fields are marked `disputed` — tell the user which fields need review.

### Step 5: Verify (Optional)

If the user wants confirmation, query Supabase:
```python
from execution.db.client import get_client
client = get_client()
result = client.table('documents').select('name, status, tax_schedule').like('name', f'{year} Keynote%').execute()
for doc in result.data:
    print(f"{doc['name']} | {doc['status']} | {doc['tax_schedule']}")
```

## Error Handling

| Error | Fix |
|---|---|
| `FileNotFoundError: QBO export not found` | Run `python3 -m execution.keynote_tax_export --year {year}` first |
| `RuntimeError: Entity not found in Supabase` | Run `python3 -c "from execution.db.seed import main; main()"` to seed entities |
| Exit code 1 with validation warnings | Data is loaded but some fields are `disputed` — review on `/verify` |

## Reference

- Load script: `execution/tax/load_qbo_to_supabase.py`
- QBO export script: `execution/keynote_tax_export.py`
- Supabase queries: `execution/db/queries.py` (`upsert_document`, `mark_document_extracted`)
- Verify page: `tax-portal/src/app/verify/page.tsx`
