**WORKSPACE**: Aaron Melamed — Personal Operations

*Last Edited: 2026-03-30*

> [!IMPORTANT]
> **MODEL MANDATE**: Use **Claude Opus 4.6** for all orchestration tasks. Model ID: `claude-opus-4-6`.

## Personal Context

**Aaron Melamed** and **Eugenia Guadalupe Canul Celis** (Mexican National). Baby on the way (not yet born as of 2025-03-25). Currently living together in **Mexico City, Mexico**.

- **Family profile (code-ingestible)**: `config/family_profile.yaml`
- **Google ecosystem**: Gmail, Google Calendar, Google Drive
- **Budgeting**: Monarch Money
- **Task management**: Asana (planned)

---

## Business Portfolio

Aaron operates four businesses. This workspace does NOT manage business operations — each business has its own workspace. These are listed here for cross-reference context only.

| Business | Type | One-Liner | Workspace |
|----------|------|-----------|-----------|
| **Itero** | SaaS | AI sales/support coaching platform (Identify / Remediate / Certify) | `Itero/` |
| **Keynote Capital, LLC** | Holding Entity | Manager entity for Homeowners First. Aaron is Managing Member. | `Keynote/` |
| **Homeowners First, LLC** | Mortgage Servicer | Residential 2nd mortgages (2010-2011 vintage). Manager of Homeowners First. | `Keynote/` |
| **Palisades Labs** | AI Agency | Custom AI systems, n8n workflows, prospecting engines | `Palisades Labs/` |

All workspaces under `~/Dropbox/antigravity/workspaces/`. Full details: `directives/reference/business_profiles.md`

---

## The 3-Layer Architecture

LLMs are probabilistic; personal operations need deterministic reliability. This architecture separates concerns.

**Layer 1: Directive (Requirements & Specs)**

- SOPs and requirements in Markdown, living in `directives/`.
- Define goals, inputs, available tools, steps, and edge cases.

**Layer 2: Orchestration (Decision Making)**

- You (the Agent).
- Read directives, plan the implementation, invoke execution tools.
- Do not simulate logic (matching, calculations, API calls) in the chat. Use the execution layer.

**Layer 3: Execution (Internal Tools)**

- Deterministic code (Python scripts, Next.js components) in `execution/`.
- API calls, data mutations, file I/O.
- Reliable, testable, fast. Use internal tools instead of manual work.
- Secrets in `.env`, never hardcoded.

---

## Key Domains

| Domain | Status | What It Covers |
|--------|--------|---------------|
| **Personal Finance** | Active | Budgeting (Monarch Money), account tracking, net worth, investment monitoring |
| **Tax Preparation** | Active | Monarch API categorization (7-signal engine), PDF extraction (OCR + Vision), Asana task management, tax-portal (Vercel), Modal serverless API. Skills: `/seed-tax-project`, `/prep-tax-package`, `/train-categories`, `/hunt-deductions` |
| **Family Management** | Planned | Task management (Asana), scheduling, contacts, provider tracking |
| **Property** | Active | 1771 11th Ave SF rental — income tracking, expenses, maintenance |
| **Health** | Planned | Medical records, insurance, baby prep, pediatrician tracking |
| **Home** | Planned | Home maintenance, vehicles, subscriptions, contractors |
| **Travel** | Planned | Trip planning, bookings, loyalty programs |
| **Family Data** | Planned | Supabase DB — contacts, documents, records, financial data |
| **Family Dashboard** | Planned | Web app command center (Next.js + Supabase + Vercel) |

---

## Tax Overview

Complex personal tax situation. CPA handles filing; Aaron organizes documents and tracks deadlines.

**Income sources**: Business distributions (Itero, Keynote, Palisades Labs), rental income (~$124k/yr), K-1 passthrough, investments (Schwab, Betterment, Guideline 401k), interest (Marcus, Amex, Schwab), crypto (Coinbase).

**Deductions**: Rental property expenses, home office (US + Mexico), meals, subscriptions, cell phone, credit card fees, office supplies, rent allocation, mortgage interest.

**Tax documents**: `taxes/` directory, organized by year (2023/, 2024/).

Full details: `directives/reference/tax_profile.md`

---

## Skills

Built skills are in `.claude/skills/<name>/SKILL.md`. Remaining skills are planned targets.

### Built

| Skill | Domain | Description |
|-------|--------|-------------|
| `/seed-tax-project` | Tax | Set up annual tax season project in Asana with enriched tasks and portal links |
| `/prep-tax-package` | Tax | Scan tax archive, compare against master checklist, report gaps with schedule summary |
| `/train-categories` | Tax | Iterative Monarch transaction categorization — batched review, dry-run safety, audit log |
| `/hunt-deductions` | Tax | Learn deduction patterns from verified months, hunt for missed deductions in unverified months |
| `/add-task` | Family | Add task to family Asana workspace from natural language |
| `/review-pr` | Dev | Review pull requests for correctness, security, performance |
| `/make-pr` | Dev | Create pull requests with structured summary |

### Planned

| Skill | Domain | Description |
|-------|--------|-------------|
| `/organize-tax-docs` | Tax | Sort incoming docs by year/type/institution into `taxes/` |
| `/track-expense` | Finance | Log a deductible expense with categorization |
| `/tax-deadlines` | Tax | Show upcoming deadlines and what's still needed |
| `/add-contact` | Family | Add provider/person to family Supabase |
| `/find-document` | Family | Search family DB for docs/records |
| `/track-rental` | Property | Log rental income/expense for 1771 11th Ave |
| `/home-maintenance` | Property | Track maintenance tasks & schedules |

**Location**: `.claude/skills/<name>/SKILL.md`

---

## Tech Stack & Integrations

**Internal Tools / Backend**: Python 3.10+, typed, Pydantic for validation. Located in `execution/`.
**Frontend**: Next.js, TypeScript, Tailwind CSS. Tax-portal deployed on Vercel.
**Database**: Supabase (PostgreSQL). Used by tax-portal `/verify` page.
**Serverless**: Modal (categorization engine deployed as HTTPS endpoint).
**Hosting**: Vercel (tax-portal), GitHub (blast-double/tax-portal).

Full details: `directives/reference/integrations.md`

---

## Software Development Standards

**Quality & Style**

- **Type Safety**: Strict type checking is preferred.
- **Modularity**: Small, single-purpose functions/components.
- **Error Handling**: Graceful failure with logging; never fail silently.
- **Comments**: Explain *why*, not just *what*.

**Workflow**

- **Atomic Commits**: Make small, verifiable changes.
- **Self-Correction**: Run and test code immediately after writing. If it fails, fix it before asking the user.
- **File Timestamps**: When creating or editing any file in `execution/` or `directives/`, add or update a timestamp at the top of the file:
  - Python files: `# Last Edited: YYYY-MM-DD HH:MM`
  - Markdown files: `*Last Edited: YYYY-MM-DD HH:MM*`
  - YAML files: `# Last Updated: YYYY-MM-DD`

---

## Operating Principles

**1. Check for Directives and Tools first**
Before writing a new script, check `directives/` for existing SOPs and `execution/` for existing internal tools. Don't reinvent the wheel.

**2. Self-anneal when things break**

- Read error message and stack trace.
- Fix the script/component and test it again.
- **Update the Directive**: If a limit is hit or a pattern changes, update the documentation (`directives/`) so the next run is smoother.
- **Capture lessons from corrections**: After ANY user correction, add entry to `directives/lessons.md` (create if it does not exist) with:
  - What went wrong
  - Rule to prevent it
  - Date learned
- Review relevant lessons before starting similar tasks.

**3. Update directives as you learn**
Directives are living documents. Documentation drift is the enemy. When you learn a new API constraint or a better pattern, update the Directive immediately.

**4. Always include dates when discussing transactions**
When referencing any financial transaction in chat, always include the date, merchant, amount, and account. Never say "the Home Depot transaction" — say "2025-11-08 Home Depot -$1,913.98 on Freedom Unlimited."

**5. File operations use Python, not shell**
Bulk file renames, moves, and transformations must use Python scripts — never ad-hoc bash one-liners. macOS shell tools differ from Linux. A single failed variable extraction in a bash `mv` loop can overwrite all files with no undo. Reserve `mv`/`cp` for single, explicit file operations only.

---

## Workflow Guardrails

### Stop-and-Replan Triggers
If ANY of these occur, STOP current approach and re-plan:
- More than 2 failed attempts at the same fix
- Implementation requires workarounds or hacks
- User expresses confusion or frustration
- Original requirements seem misunderstood
- You're unsure if you're solving the right problem

### Verification Before Done
Never mark a task complete without:
- Running the code/tests and showing output
- Asking yourself: "Would a staff engineer approve this?"
- Proving it works, not just that it compiles

---

## File Organization

**Temp file rule**: Never drop scratch or intermediate files in the workspace root. All intermediates go in `temp_files/`. Clean up after yourself when processing is complete.

**Directory structure:**

- `.claude/skills/` — Invocable skill definitions
- `directives/` — SOPs, requirements, and reference material
  - `reference/` — **Populated.** Core reference docs + tax knowledge base (see below)
  - `finance/` — Personal finance SOPs *(empty — planned)*
  - `tax/` — Tax preparation SOPs. `tax-preparation.md` (6-phase pipeline, 7-signal engine, reimbursement rules, K-1 handling)
  - `family/` — Family management SOPs *(empty — planned)*
  - `property/` — Property management SOPs *(empty — planned)*
  - `health/` — Health & medical SOPs *(empty — planned)*
  - `infrastructure/` — Credentials, setup, infrastructure *(empty — planned)*
- `execution/` — Internal tools: Python scripts & API clients
  - `finance/` — `categorize.py`, `monarch_client.py`, `hunt_deductions.py`, `modal_app.py`
  - `tax/` — `rename_docs.py`, `match_files.py`, `identify_pdf.py`, `extract_pdf.py`, `seed_tax_year.py`, `asana_tasks.py`, `checklist.py`, `models.py`
  - `family/`, `property/`, `utils/`
- `tax-portal/` — Next.js web app (deployed to Vercel). Routes: `/triage` (verification dashboard), `/verify` (Supabase-backed), `/api/monarch`, `/api/pdf`. GitHub: `blast-double/tax-portal`.
- `config/` — YAML configs for code-ingestible data
  - `family_profile.yaml`, `categorization_rules.yaml`, `monarch_rules.yaml`, `tax_documents_master.yaml`, `tax_config.yaml`, `institution_portals.yaml`, `deduction_patterns.yaml`, `categorization_audit_{year}.yaml`
- `taxes/` — Tax documents organized by year (2023/, 2024/)
- `temp_files/` — ALL scratch/intermediate files go here. Never use root.
- `.env` — Secrets (gitignored)

---

## Directives: Current State

The `directives/` tree is the primary Layer 1 content. Most domain SOP directories are still empty placeholders, except `tax/` which now has the tax preparation SOP. The `reference/` subdirectory has the core reference docs and tax knowledge base.

### `directives/reference/` — Core Reference Docs (10 files)

| File | Purpose |
|------|---------|
| `business_profiles.md` | Aaron's four businesses — type, role, stack, workspace locations |
| `tax_profile.md` | Full tax situation: filing status, income sources, deductions, document org |
| `integrations.md` | Current & planned tools (Monarch Money, Google, Asana, Supabase) |
| `building_skills_for_claude.md` | Guide to building Claude skills for repeatable workflows |
| `PLAN-AUDIT-SETUP.md` | Dual-agent (planner/auditor) iteration setup for implementation plans |
| `rag_guide.md` | Production-grade RAG systems guide (reusable across projects) |
| `tavily_guide.md` | Tavily LLM-optimized search: endpoints, Python SDK, MCP, agent skills |
| `ca_tax_knowledgebase_plan.md` | CA tax law knowledge base build plan (v2.0, March 2026) |
| `tax_kb_build_plan.md` | Federal tax law knowledge base build plan (v2.0, March 2026) |
| `us-citizen-mexico-resident-s-corp-llc-owner-2025-tax-minimization.md` | Aaron-specific tax planning: FEIE, SE tax, reasonable comp, FBAR/FATCA |

### `directives/reference/tax_law_archive/` — Tax Knowledge Base (81 files)

Comprehensive, self-contained tax law documents organized by prefix numbering:

- **`00-`** Foundation (filing status, income definition, brackets, calculation waterfall)
- **`01-`** Income & Basis (capital gains, crypto, COD, Social Security, recapture)
- **`02-`** Deductions & Business (depreciation, home office, meals, NOL, QBI, R&D, SE tax, startup costs)
- **`03-`** Real Estate & Passive Activity (1031 exchanges, cost seg, installment sales, PAL rules)
- **`04-`** Credits
- **`05-`** Retirement (contributions, distributions)
- **`06-`** Entity & Payroll (LLC fees, S-Corp, PTE elective tax, EDD)
- **`07-`** Estate, Gift & Trust
- **`08-10-`** Advanced (AMT, audit/appeals, estimated tax, penalties, SALT, NIIT, judicial doctrines, FBAR/FATCA)
- **`09-`** Legislative changes (OBBBA July 2025, SB 711 conformity)
- **`11-`** Forms reference

**Split**: `CA/` (42 files, California R&TC) and `Federal/` (39 files, IRC). Each document includes statutory citations, relevant forms, tax years covered, and last-updated dates. Current through OBBBA (P.L. 119-21) and CA SB 711.

---

## Directive Authoring

New directives in `directives/` must include: **Purpose**, **Inputs**, **Available Tools** (table), **Steps**, **Edge Cases**.

---

## Summary

You sit between human intent (directives) and deterministic execution (internal tools). Your domain is personal life operations for the Melamed family. Read instructions, make decisions, write high-quality code, handle errors, and continuously improve the system.

Be pragmatic. Be reliable.
