---
name: seed-tax-project
description: "Initialize a new tax year. Confirms active institutions and conditional items, updates config, refreshes portal data via Tavily, seeds Supabase, and creates an Asana project with download tasks."
user-invocable: true
---

# Setup Tax Year

Initialize a new tax year: confirm conditional items and institutions, update config, refresh portal data, seed Supabase, and create an Asana project with download tasks.

## Prerequisites

- `ASANA_PAT` set in `.env`
- `SUPABASE_PROJECT_URL` and `SUPABASE_SERVICE_ROLE_KEY` set in `.env`
- `config/tax_documents_master.yaml` exists (master checklist)
- `config/tax_config.yaml` exists (per-year config)

## Workflow

### Step 1: Parse the Request

Extract the tax year from the user's request:
- "setup tax year for 2025" → year 2025
- "set up my tax year" → default to current year minus 1

### Step 2: Ask Clarifying Questions

Use AskUserQuestion to confirm the year's setup:

**Question 1:** Which conditional items apply this year?
- Receiving a W-2? (If yes, from which employer/PEO?)
- Receiving employer health coverage? (1095-C) — If yes, who issues the 1095-C? (employer_1095c_name may differ from employer/PEO name)
- Crypto trades on Coinbase this year?
- ProPay issuing 1099-K this year? (may be below reporting threshold)
- Schwab Bank above 1099-INT reporting threshold?
- Guideline 401k contributions this year?

**Question 2:** Confirm parameterized institutions:
- Who is the loan servicer this year? (default: New American Funding)

**Question 3:** Any new institutions to add?
- If yes, add them to `config/tax_documents_master.yaml` before proceeding.

### Step 3: Update Config

Write the user's answers to `config/tax_config.yaml`:
- Set `initialized: true` for the tax year
- Set `conditional_items` based on answers:
  ```yaml
  conditional_items:
    employer_w2: true/false
    employer_1095c: true/false
    coinbase_1099: true/false
    coinbase_gainloss: true/false
    coinbase_transaction_history: true/false
    propay_1099k: true/false
    schwab_bank: true/false
    guideline_401k: true/false
  ```
- Set `parameterized_institutions` based on answers:
  ```yaml
  parameterized_institutions:
    employer_name: "..."       # W-2 issuer (PEO)
    employer_1095c_name: "..." # 1095-C issuer (may differ from PEO)
    loan_servicer_name: "..."
  ```

### Step 4: Refresh Portal Data (Tavily)

Check `config/institution_portals.yaml`. For each active institution:
- If `last_verified` date is **after December 31 of the tax year**, the data is fresh — skip.
- If stale or missing, refresh using Tavily:

**For each institution needing refresh:**
1. Call `tavily_search` with: `"{institution_name} tax documents {form_number} download portal {filing_year}"` (basic depth, 3 results)
2. Review the results to find the portal URL and click-path
3. Update the institution's entry in `config/institution_portals.yaml` with:
   - `portal_url` — the direct URL to the tax center
   - `click_path` — numbered steps to download the document
   - `expected_format` — PDF or CSV
   - `last_verified` — today's date

**For Monarch Money:** Refresh the `monarch_money_export` entry if stale.

Write the updated portal data to `config/institution_portals.yaml`.

### Step 5: Seed Documents in Supabase

Run the year-agnostic seeder:
```bash
python3 -m execution.tax.seed_tax_year --year {year}
```

### Step 6: Create Asana Project

Check if an Asana project for this year already exists. If so, ask the user whether to delete and recreate or skip.

Create the enriched project:
```bash
python3 -m execution.tax.asana_tasks --year {year}
```

### Step 7: Display Results

Show:
- Asana project URL (clickable)
- Task count and section count
- Table of institutions with their portal URLs
- Any institutions that were refreshed via Tavily

## Acceptance Checks

- Config updated with correct conditionals for the year
- Supabase seeded with expected document count matching master checklist
- Asana project created with correct task count

## Error Handling

| Error | Fix |
|---|---|
| `ASANA_PAT` not set | Add to `.env` — get token from https://app.asana.com/0/my-apps |
| Tavily search returns no useful results | Fall back to generic portal instructions; flag for manual review |
| Asana project already exists for this year | Ask user: delete and recreate, or keep existing |
| Institution portal URL changed | Tavily refresh will pick up the new URL; update `institution_portals.yaml` |
| New institution not in master YAML | Add it to `config/tax_documents_master.yaml` first, then re-run |

## Reference

- **Master checklist**: `config/tax_documents_master.yaml`
- **Per-year config**: `config/tax_config.yaml`
- **Portal cache**: `config/institution_portals.yaml`
- **Asana task creator**: `execution/tax/asana_tasks.py`
- **Document seeder**: `execution/tax/seed_tax_year.py`
- **Directive**: `directives/tax/tax-preparation.md`
