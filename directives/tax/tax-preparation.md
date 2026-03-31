*Last Edited: 2026-03-30 14:00*

# Tax Preparation — Step-by-Step Playbook

Annual tax prep pipeline for Aaron Melamed. Run January through April. Goal: deliver a clean, verified tax package to CPA Jessica with minimal billable hours.

**Who uses this document:**
- **Aaron** — to know what to do, when, and which skills to run
- **Claude** — to execute each step correctly when Aaron invokes a skill

---

## Quick Reference

| Resource | Location |
|----------|----------|
| Master checklist (all expected documents) | `config/tax_documents_master.yaml` |
| Year config (conditionals, institutions) | `config/tax_config.yaml` |
| Tax document archive | `tax_document_archive/{year}/` |
| Categorization rules | `config/categorization_rules.yaml` |
| Deduction patterns | `config/deduction_patterns.yaml` |
| Institution portal URLs | `config/institution_portals.yaml` |
| Extraction prompts (Vision) | `config/extraction_prompts/` |
| Monarch audit log | `config/categorization_audit_{year}.yaml` |
| Supabase tracking | `documents` table (status: expected → received → extracted → verified) |
| Tax portal | Vercel — `/triage` (transactions) and `/verify` (documents + extracted data) |
| CPA | Jessica — email + client portal |
| Lessons learned | `directives/lessons.md` |

---

## The Pipeline at a Glance

```
JANUARY                          FEBRUARY — MARCH                         APRIL
─────────                        ────────────────                         ─────
Step 1: Seed the year            Step 3: Download documents (you)         Step 6: Extract form data
Step 2: Check for early docs     Step 4: Ingest & rename documents        Step 7: Load entity data
                                 Step 5: Categorize transactions          Step 8: Hunt for deductions
                                    ↻ Repeat Steps 3-4 as docs arrive    Step 9: Verify everything
                                                                          Step 10: Deliver to CPA
```

---

## Step 1: Seed the Tax Year

> **When:** Early January
> **Skill:** `/seed-tax-project`
> **Time:** ~5 minutes

This initializes everything for the new tax year. Run it once.

**What it does:**
1. Asks you to confirm which conditional items apply this year:
   - Receiving a W-2? From which employer?
   - Employer-provided health coverage (1095-C)?
   - Crypto trades on Coinbase?
   - Guideline 401k contributions?
   - ProPay issued a 1099-K?
   - Schwab Bank interest above 1099-INT threshold?
2. Updates `config/tax_config.yaml` with this year's settings
3. Refreshes institution portal URLs via Tavily (login pages change)
4. Seeds expected documents into Supabase (one row per expected form)
5. Creates an Asana project with a download task for each institution, including portal links and click-paths

**Prerequisites:** Supabase and Asana credentials in `.env`

**You're done when:** Asana shows a project like "2025 Tax Documents" with tasks for each institution.

---

## Step 2: Check for Early Documents

> **When:** Mid-January (some institutions release docs early)
> **Skill:** `/prep-tax-package`
> **Time:** ~1 minute

Run the gap checker to see if anything has already arrived.

**What it does:**
- Scans `tax_document_archive/{year}/` against the master checklist
- Reports four categories:
  - **Matched** — document found in archive
  - **Missing** — expected but not yet downloaded
  - **Not Expected** — conditional items you disabled in Step 1 (with reason)
  - **Reference** — informational docs (prior year returns, etc.) shown separately

**Prerequisites:** Step 1 complete (year seeded)

**You're done when:** You see the gap report and know what's still outstanding. Most things will be "Missing" in January — that's normal.

---

## Step 3: Download Documents from Institutions

> **When:** January through March, as institutions release forms
> **Who:** You (Aaron) — manual downloads
> **Time:** 5-10 minutes per institution

This is the one manual step. You log into each institution's portal and download your tax documents.

**How to work through it:**
1. Open your Asana project from Step 1 — each task has the portal URL and click-path
2. Log in, download the PDF
3. Drop it into `tax_document_archive/{year}/` — filename doesn't matter yet (Step 4 handles renaming)
4. Check off the Asana task
5. Repeat as documents become available through March

**Typical document timeline:**
| When | What arrives |
|------|-------------|
| Late January | 1099-INTs (banks), 1099-DIVs, 1098 (mortgage) |
| Mid February | 1099-Composites (Schwab, Betterment), 1099-Ks |
| Late February | W-2s (if applicable), 1095-Cs |
| March | Corrected/amended forms, stragglers |

**Tip:** Run `/prep-tax-package` anytime to see what's still missing.

---

## Step 4: Ingest & Rename Documents

> **When:** After each batch of downloads (repeat as needed)
> **Skill:** `/ingest-tax-docs`
> **Time:** ~3 minutes per batch

This auto-identifies and renames whatever you dropped into the archive.

**What it does:**
1. Scans for files that don't match the canonical naming pattern
2. **Pattern matching first** (fast, free) — matches filenames against `tax_documents_master.yaml`
3. **OCR fallback** for unrecognized files — reads the PDF content via Google Document AI to identify institution, form type, year, and account number
4. Presents matches for your review:
   - **High confidence** — auto-renames (with your approval)
   - **Medium/low confidence** — shows what it thinks, asks you to confirm
5. Renames files to canonical format (e.g., `2025_schwab_1099-composite.pdf`)
6. Uploads renamed files to Supabase Storage
7. Shows updated gap report

**Safety:** Dry-run by default. A rollback manifest is written before any renames. You explicitly approve before anything changes.

**Prerequisites:** Step 1 complete. Google Document AI credentials in `.env`.

**Naming rules:**
| Type | Pattern | Example |
|------|---------|---------|
| Institutional | `{year}_{institution}_{form}.pdf` | `2025_schwab_1099-composite.pdf` |
| Multi-account | `{year}_{institution}_{form}_{last5}.pdf` | `2025_betterment_5498-fmv_43197.pdf` |
| Self-prepared | `{year}_self_{category}.{ext}` | `2025_self_rental-income.csv` |
| Reference | `{year}_ref_{type}.{ext}` | `2024_ref_filed-return.pdf` |

**You're done when:** All files in the archive have canonical names, and `/prep-tax-package` shows the documents as "Matched."

---

## Step 5: Categorize Transactions

> **When:** March — once most transactions for the tax year are posted
> **Skill:** `/train-categories`
> **Time:** 20-40 minutes (iterative batches, spread across sessions)

This is the big one. The categorization engine pulls all transactions from Monarch Money and classifies them for tax schedules.

**What it does:**
1. Pulls transactions for the tax year from Monarch
2. Runs the 7-signal classification engine:
   - Signal 1: Monarch's own rules (204 rules in `monarch_rules.yaml`)
   - Signal 2: Schedule map (`categorization_rules.yaml` — maps categories to tax schedules)
   - Signal 3: Account type (business card vs. personal card)
   - Signal 4: Recurring patterns (same merchant + amount monthly)
   - Signal 5: Historical consistency (merchant always → same category)
   - Signal 6: Tap detection (garbled Mexico City merchant names via Mercado Pago/Apple Pay)
   - Signal 7: Plausibility checks (utility whitelist, generic payment detection, foreign merchant flags)
3. Presents batches of transactions that need review
4. You approve, correct, or skip each batch
5. Approved changes are applied to Monarch and logged to the audit file

**Safety:** Dry-run by default. Every change logged to `config/categorization_audit_{year}.yaml`. Rollback available.

**Prerequisites:** Monarch credentials in `.env`. Best to wait until March so most transactions have posted.

**Key rules to remember:**
- Mexico City restaurants default to **personal** unless explicitly tagged as business meal
- Reimbursed expenses go to "Reimbursed by Keynote/Itero" (Transfers) — not Schedule C
- Keynote Income in Monarch is reference only — the K-1 is the tax document
- Credit card annual fees are personal (AMEX reimburses via credits, net ≈ zero)

**You're done when:** The `/triage` page in the tax portal shows clean schedule breakdowns with no obviously miscategorized transactions.

---

## Step 6: Extract Form Data

> **When:** April — after all documents collected
> **Skill:** `/extract-tax-forms`
> **Time:** ~10 minutes (mostly automated)

Extracts the actual numbers from your tax PDFs so they can be verified against Monarch totals.

**What it does:**
1. For each institutional PDF in the archive:
   - **Pass 1:** Google Document AI OCR extracts raw text
   - **Pass 2:** Claude Vision reads the PDF with form-specific prompts and extracts structured fields (box numbers, dollar amounts, descriptions)
2. **Reconciliation** compares the two passes field-by-field:
   - Both agree → `verified` (green)
   - Disagree → `disputed` (red — you must resolve)
   - Only one source → `single_source` (yellow)
3. Stores results in Supabase for the `/verify` page

**Prerequisites:** Steps 1-4 complete (documents collected and renamed). Google Document AI credentials in `.env`.

**Available extraction prompts:** 1098, 1099-B/DIV, 1099-Composite, 1099-INT, 1099-K
**Not yet built:** 1099-MISC, 5498-FMV (will need to be created when these forms are first extracted)

**You're done when:** Supabase has extracted data for all institutional documents, and disputed fields are resolved.

---

## Step 7: Load Entity Data

> **When:** April — after Keynote Capital (and any other entity) QBO exports are ready
> **Skill:** `/load-entity-data`
> **Time:** ~2 minutes

Loads business entity financials from QuickBooks Online into Supabase so the `/verify` page can show them alongside PDF extractions and Monarch data.

**What it does:**
1. Reads the QBO export JSON from `tax_document_archive/{year}/{entity}_tax_summary_{year}.json`
2. Creates 3 document records in Supabase per entity:
   - P&L Summary (→ Schedule E)
   - Distributions to Aaron (→ Schedule E)
   - Interest Income (→ Schedule B)
3. Cross-validates QBO totals

**How to generate the QBO export:**
- Run `execution/keynote_tax_export.py` from this workspace (it reads from the Keynote workspace's QBO client)
- Output lands in `tax_document_archive/{year}/keynote-capital_tax_summary_{year}.json`

**Prerequisites:** QBO export JSON exists. Supabase credentials in `.env`. Entity must be seeded in Supabase (Step 1 handles this).

**You're done when:** The `/verify` page shows Keynote Capital's P&L, distributions, and interest alongside the other tax documents.

---

## Step 8: Hunt for Missed Deductions

> **When:** April — after categorization is mostly complete (Step 5)
> **Skill:** `/hunt-deductions`
> **Time:** ~15 minutes

Proactively finds deductions hiding in the wrong categories.

**What it does:**
1. **Training phase:** Learns deduction patterns from months you've already verified (the "training window" — typically the most recently categorized months)
2. **Hunting phase:** Scans unverified months for transactions that match deduction patterns but are currently categorized as personal or wrong category
3. Presents candidates in batches for your review
4. Approved recategorizations applied to Monarch and logged

**Modes:**
- Default: train + hunt
- `--train-only`: learn patterns without making changes
- `--hunt-only`: hunt using existing patterns from `config/deduction_patterns.yaml`

**Safety:** Dry-run by default. Audit trail on all changes.

**What it catches:**
- Hardware store purchases that should be "1771 - Maintenance" (rental property)
- Software subscriptions that should be on Schedule C
- Business meals miscategorized as personal dining
- Office supplies on the wrong card

**What to watch for:**
- 1771 11th Ave SF is Aaron's rental. Hardware stores, contractors → "1771 - Maintenance"
- 140 E 40th St is parents' property — NOT Aaron's deduction
- Only unreimbursed expenses are deductible. If Keynote/Itero paid Aaron back, it's a Transfer

**You're done when:** The deduction sweep is complete and you're satisfied no significant deductions are hiding in personal categories.

---

## Step 9: Verify Everything

> **When:** April — after Steps 5-8
> **Where:** Tax portal (`/triage` and `/verify` pages)
> **Time:** 30-60 minutes (manual review)

This is your final quality check before delivering to the CPA.

**Transaction verification (`/triage` page):**
1. Open the `/triage` page in the tax portal
2. Review each tax schedule:
   - **Schedule B** — Interest and dividend income. Cross-check against 1099-INT/DIV extracted values.
   - **Schedule C** — Business income and expenses. Verify no personal expenses leaked in.
   - **Schedule C - Meals** — 50% deductible. Verify these are actual business meals.
   - **Schedule C - Home Office** — Rent, internet, utilities. Verify Mexico City allocation.
   - **Schedule E** — Rental income (ProPay) and expenses (1771 11th Ave). Verify against property management records.
   - **Self-Employed Deduction** — Health insurance (Cigna). Verify premiums match.
3. Look for red flags: unusually large categories, merchants that don't belong, missing months

**Document verification (`/verify` page):**
1. Open the `/verify` page
2. Review each extracted document:
   - Green (verified) fields: both OCR and Vision agree — spot-check a few
   - Red (disputed) fields: must resolve — open the PDF and confirm the correct value
   - Yellow (single source) fields: only one extraction method got a value — verify manually
3. Check the Keynote Capital entity data (P&L, distributions, interest) against QBO
4. Mark each document as reviewed using the checkboxes

**You're done when:** All schedules look correct, all disputed fields are resolved, and you're confident the numbers match reality.

---

## Step 10: Deliver to CPA

> **When:** April — after Step 9
> **Skill:** `/deliver-to-cpa` *(not yet built)*
> **Time:** TBD

**Current process (manual):**
1. Print/export the `/triage` page (transaction summaries by schedule)
2. Print/export the `/verify` page (document extractions with verified values)
3. Collect all PDFs from `tax_document_archive/{year}/`
4. Send to Jessica via her client portal or email

**Planned automation (MVP):**
- Generate a PDF cover document grouped by tax schedule
- Include extracted values, Monarch totals, and source document references
- Block generation if any disputed fields remain unresolved
- Completeness check: all expected documents received, all required fields extracted

---

## Repeatable Loops

Some steps repeat throughout the season. Here's when to re-run:

| Trigger | What to run |
|---------|-------------|
| New documents downloaded | Step 4 (`/ingest-tax-docs`) → Step 2 (`/prep-tax-package`) |
| Want to check progress | Step 2 (`/prep-tax-package`) |
| New Monarch transactions posted | Step 5 (`/train-categories`) |
| Categorization mostly done | Step 8 (`/hunt-deductions`) |
| QBO export updated | Step 7 (`/load-entity-data`) |
| Before sending to CPA | Step 9 (verify in portal) |

---

## Scope Exclusions

These items are explicitly **outside** this pipeline:

| Item | Reason |
|------|--------|
| **K-1s** | Handled via Keynote Capital accounting, directly with CPA. "Keynote Income" in Monarch is reference-only — the K-1 is the tax document, not bank deposits. Do NOT put on Schedule C. |
| **Reimbursed expenses** | In Monarch: "Reimbursed by Keynote" / "Reimbursed by Itero" under Transfers (net-worth neutral). Expense lives on entity's books. Only unreimbursed items are deductible on Aaron's return. |
| **FEIE / Form 2555** | Aaron's income sources don't qualify for the Foreign Earned Income Exclusion. |
| **FBAR / Form 8938** | Foreign account balances are under reporting thresholds. |
| **Itero / Palisades Labs income** | Not passthrough entities. No income paid to Aaron (as of 2025 tax year — revisit annually). |

---

## Not Yet Supported

- `/deliver-to-cpa` skill (Step 10 — planned as PDF cover doc MVP)
- Extraction prompts for 1099-MISC and 5498-FMV
- Amended/corrected 1099 handling (current workaround: replace file, re-extract)
- Mid-year institution changes
- Automated year rollover of `TAX_YEAR` in tax portal (currently hardcoded — must update in code each January)

---

## Appendix A: Tools Reference

| Tool | Location | Purpose |
|------|----------|---------|
| `rename_docs.py` | `execution/tax/` | Canonical filename renaming. Flags: `--apply`, `--rollback` |
| `match_files.py` | `execution/tax/` | Conditional-aware gap reporting. Flag: `--dry-run` |
| `identify_pdf.py` | `execution/tax/` | OCR-based PDF classifier (institution, form, year, account) |
| `extract_pdf.py` | `execution/tax/` | Google Document AI OCR extraction |
| `upload_to_storage.py` | `execution/tax/` | Upload PDFs to Supabase Storage |
| `seed_tax_year.py` | `execution/tax/` | Seed expected documents into Supabase |
| `load_qbo_to_supabase.py` | `execution/tax/` | Load QBO entity data into Supabase |
| `asana_tasks.py` | `execution/tax/` | Create Asana project with download tasks + portal links |
| `checklist.py` | `execution/tax/` | Print document status by schedule |
| `models.py` | `execution/tax/` | Pydantic data models (specs, extraction, reconciliation) |
| `categorize.py` | `execution/finance/` | 7-signal transaction classifier |
| `hunt_deductions.py` | `execution/finance/` | Deduction pattern learner and hunter |
| `monarch_client.py` | `execution/finance/` | Monarch Money API client (session management, retry logic) |
| `modal_app.py` | `execution/finance/` | Modal serverless deployment wrapper |
| `keynote_tax_export.py` | `execution/` | Cross-workspace QBO export for Keynote Capital |

## Appendix B: Configuration Files

| File | Purpose | When to update |
|------|---------|---------------|
| `config/tax_documents_master.yaml` | Master checklist — all institutions, forms, filename patterns | **Every January** (institutions change export naming annually) |
| `config/tax_config.yaml` | Per-year conditionals and parameterized names | Step 1 (once per year) |
| `config/categorization_rules.yaml` | Schedule map + learned categorization rules | Grows during Step 5 (train-categories adds rules) |
| `config/deduction_patterns.yaml` | Learned deduction patterns (persists across years) | Grows during Step 8 (hunt-deductions adds patterns) |
| `config/monarch_rules.yaml` | 204 Monarch auto-categorization rules | Rarely — only if Monarch rule logic changes |
| `config/institution_portals.yaml` | Portal URLs + click-paths | Step 1 (Tavily refresh) |
| `config/extraction_prompts/` | Per-form Claude Vision prompts | When new form types need extraction |
| `config/categorization_audit_{year}.yaml` | Audit log of all Monarch changes | Auto-written by Steps 5 and 8 |

## Appendix C: Naming Conventions

All files in `tax_document_archive/{year}/` follow strict naming. Slugs are lowercase, hyphen-separated. Parenthetical qualifiers stripped (e.g., "Schwab (brokerage)" → `schwab`).

**Always use the specific IRS form number** — read the PDF if unsure. Examples: `5498-fmv` not `fmv`, `1099-misc` not `1099`, `1099-supplemental` not `supplemental`.

## Appendix D: Lessons Learned (Key Pitfalls)

These are recurring issues. Review before each tax season.

1. **Filename patterns break every year.** AMEX dropped "1099" in 2025. Goldman Sachs and Betterment changed formats. Update `tax_documents_master.yaml` every January.
2. **Reimbursed expenses are not deductions.** If Keynote/Itero paid Aaron back, it's a Transfer, not Schedule C. Litmus test: did money come back? Yes = Transfer.
3. **Mexico City tap transactions have garbled merchant names.** Mercado Pago / Apple Pay on Mexican terminals produce garbage. The engine uses `plaidName` fallback, but ~5% still need manual review.
4. **Mexico City restaurants default to personal.** Only business meals where business was explicitly discussed count as 50% deductible.
5. **Credit card annual fees net to zero.** AMEX reimburses via airline credits and statement credits. Categorized as personal (excluded).
6. **Use OCR to identify documents.** Never ask Aaron to manually identify an unfamiliar file. Read the PDF content.
7. **Read PDFs for actual IRS form numbers.** Institutions use generic labels ("FMV", "Supplemental"). The filename must use the real IRS form number.
8. **Modal redeploy required after config changes.** `categorization_rules.yaml` is baked into the Modal image. Always redeploy after changes.
9. **Entity income ≠ personal income.** Keynote's bank interest and P&L belong on the entity return. Only distributions TO Aaron belong on the personal return.
