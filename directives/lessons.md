*Last Edited: 2026-03-30*

# Lessons Learned

Corrections and rules captured after errors. Review before starting similar tasks.

---

## 2026-03-29 — Transaction categorization review

**What went wrong:** The categorization engine auto-classified 5 transactions incorrectly because it treated all positive inflows as income and all merchant-name matches as business expenses.

**Specific errors:**

1. **Airbnb $1,729.11 classified as "Airbnb Income"** — was actually a refund on a personal Airbnb stay. The engine saw "Airbnb" + positive amount and assumed rental income. Rental income only comes through ProPay on the Investor Checking account.

2. **Citibank $6,655.98 classified as "Other Income"** — was a personal loan that Aaron loaned to Itero. Not income. Inflows from banks to personal accounts are transfers/loans, not income.

3. **Barclays $99 classified as "Other Income"** — not income. Inflows from card issuers are typically refunds, rewards, or credits.

4. **Zelle $90 classified as "Business Income"** — was an accidental payment someone sent Aaron. Not business income. Zelle inflows on personal accounts default to Transfer unless explicitly tagged.

5. **Barra Grana classified as "Business Utilities & Communication"** — is a restaurant in Mexico City. Mexico City restaurants are personal unless explicitly identified as a client/partner business meal.

**Rules to prevent recurrence:**

- **Positive inflows are NOT always income.** Refunds (Airbnb, IRS), loans (Citibank), rewards (Barclays), and accidental payments (Zelle) all appear as positive amounts. The engine must consider: (a) account type — personal vs business, (b) merchant context — is this a known income source?, (c) category sense — does "income" make sense for this merchant on this account?
- **Only known income channels count as income.** Rental income = ProPay on Investor Checking. Business income = Keynote distributions, client payments. Interest = bank interest payments. Everything else needs scrutiny.
- **Mexico City restaurants default to personal.** Only meals where business was explicitly discussed with clients/partners qualify as "Business Travel & Meals" (50% deductible). Restaurants in Mexico City are personal dining unless Aaron explicitly tags them.
- **One-off personal transactions can't be caught by rules.** When the engine sees an unmapped positive inflow, it should flag for review rather than auto-assigning to "Other Income" or "Business Income."

---

## 2026-03-29 — Monarch Money auth failures

**What went wrong:** `monarch_client.py` lost its session file, tried to login fresh, and Monarch rate-limited the attempt (returns 401/404 after 1-2 rapid login attempts). Subsequent retries all failed. Required manual intervention to copy a session file from a fallback location.

**Root cause:** The session file at `execution/.credentials/monarch_session` was missing (never created on a clean checkout or after credential directory cleanup). The `get_client()` function had no retry logic and no fallback session path.

**Fix applied:**
1. `get_client()` now checks both the primary path (`execution/.credentials/monarch_session`) AND the fallback path (`.mm/mm_session.pickle` — MonarchMoney's default). If fallback works, it copies to the primary location automatically.
2. Login retries with exponential backoff (3 attempts, 5s/10s/15s delays).
3. Clear error message on final failure explaining rate limiting.

**Rule:** Never run ad-hoc Monarch login scripts outside of `monarch_client.py`. They create session files at the wrong path and burn login attempts. Always use `get_client()` as the single entry point.

---

## 2026-03-29 — Filename patterns are fragile

**What went wrong:** Institutions change their PDF export naming year-over-year. AMEX dropped "1099" from their filename in 2025. Goldman Sachs completely changed their format from `Goldman Sachs 2024 1099-INT.pdf` to `Tax_1099INT_2025_8823_...`. Betterment dropped their prefix.

**Rule:** Always review and update filename patterns in `config/tax_documents_master.yaml` each January when new docs arrive. Never assume last year's patterns still work.

---

## 2026-03-29 — Multi-account specs need disambiguation

**What went wrong:** Betterment has two accounts with different 15-digit IDs in FMV filenames. A single spec matched multiple files with no way to distinguish which account was which.

**Rule:** When a spec can match multiple files from the same institution, use `multi_account: true` + `account_pattern` on the spec to extract a suffix (e.g., last 5 digits of account ID). Current DB contract is single-file-per-spec; multi-account is rename-only, not DB-tracked.

---

## 2026-03-29 — Use OCR to identify documents, not user questions

**What went wrong:** Files arrived with unfamiliar names and the agent asked the user to manually identify them instead of reading the PDF content.

**Rule:** When files arrive with unrecognized names, read the PDF content (OCR or Vision) to identify institution, form type, and tax year. Don't ask the user to manually identify files — that's what the tools are for.

---

## 2026-03-29 — Read PDFs to identify the actual IRS form number

**What went wrong:** Documents were named with generic labels like "FMV", "Supplemental", "1099" instead of the actual IRS form they relate to. The Betterment FMV turned out to be a Form 5498 IRA year-end statement. The Coinbase 1099 was specifically a 1099-MISC. Generic labels make it harder for the CPA to know what she's looking at.

**Rule:** When adding a new document spec to `tax_documents_master.yaml`, read the actual PDF to identify the specific IRS form number it relates to. Use that form number in `form_number` (e.g., "5498-FMV" not "FMV", "1099-MISC" not "1099", "1099-Supplemental" not "Supplemental"). The filename should tell the CPA exactly what IRS form the document feeds into.

---

## 2026-03-29 — Engine must not blindly trust Monarch categories

**What went wrong:** Two transactions were miscategorized in Monarch, and the categorization engine accepted them without question:
1. "Raiadrogasilsa Rio De Janeir Bra" (a Brazilian pharmacy) was categorized as "Gas & Electric" → passed through to home office utilities.
2. "Zelle" $140 payment was categorized as "140 - Maintenance" (wrong property) → passed through to Schedule E.

The engine's Signal 2 (schedule map) trusts Monarch's existing category. If Monarch confidently assigns a wrong category, the engine passes it through without checking whether the merchant plausibly matches.

**Fix applied:** Added Signal 7 (plausibility checks) with three sub-checks:
1. **Home office utility whitelist** — Gas & Electric / Internet & Cable must be from known merchants (Naturgymexi, Telmex, Izzi, Verizon, etc.)
2. **Generic payment platform detection** — Zelle/Venmo/PayPal as merchant name in income/ambiguous categories → flag
3. **Foreign country code detection** — merchant names ending in country codes (Bra, Arg, etc.) assigned to home office → flag

All checks set `needs_review = True` without auto-recategorizing. Config-driven via `plausibility` section in `categorization_rules.yaml`.

**Rule:** When adding new categories or merchants to the schedule map, also update the plausibility whitelist. The engine should never silently pass through a merchant that obviously doesn't belong in a category.

---

## 2026-03-29 — K-1s and business entity tax forms are handled outside this workspace

**What went wrong:** Flagged K-1s from Keynote Capital as missing from the personal tax archive. K-1s are handled directly between the CPA and Keynote's accounting — they never flow through this workspace.

**Rule:** Don't track K-1s in `tax_documents_master.yaml`. Keynote Capital is a passthrough entity but its K-1 is handled during Keynote accounting, which is done separately with the CPA. Itero and Palisades Labs are NOT passthrough entities and paid no income in 2025. Itero will eventually pay Aaron a salary (future W-2). Property taxes and health insurance premiums are covered by Monarch transaction data — no separate forms needed for either.

---

## 2026-03-29 — PEO splits employer identity

**What went wrong:** W-2 came from PEO (JustWorks) while 1095-C came from the actual employer (Orum). Using a single `employer` field caused mismatches.

**Rule:** Use separate parameterized fields: `employer_name` for W-2 (the PEO that issues the form) and `employer_1095c_name` for 1095-C (the actual employer). These are different entities when a PEO is involved.

---

## 2026-03-29 — plaidName fallback needed at all raw-read points

**What went wrong:** The categorization engine reads merchant names at three separate points: `monarch_rule_matches()`, `is_tap_transaction()`, and `classify_transaction()`. Only one point had the `plaidName` fallback. When `merchantName` was garbled (common with Mexico City tap transactions), the other two points received garbage input and made wrong decisions.

**Fix applied:** Added `plaidName` fallback at all 3 raw-read points. Also added `plaid_name` field to JSON API output and expanded rows on the triage dashboard so the original Plaid name is always visible for review.

**Rule:** When a transaction object has multiple name fields (merchantName, plaidName, originalName), every function that reads the merchant name must apply the same fallback chain. Never assume one entry point handles it for all downstream logic.

---

## 2026-03-29 — Single exit point for classify_transaction()

**What went wrong:** `classify_transaction()` had multiple early `return` statements. When Signal 7 (plausibility checks) was added at the end, transactions that returned early from Signals 1-6 bypassed plausibility entirely. A Brazilian pharmacy categorized as "Gas & Electric" slipped through because Signal 2 returned before Signal 7 could flag it.

**Fix applied:** Refactored to accumulate a result object and return once at the end. All signals run in sequence, and plausibility checks always execute regardless of which signal determined the category.

**Rule:** Classification functions with post-processing steps (plausibility, CPA notes, confidence scoring) must use a single exit point. Never early-return from a classifier when downstream checks need to run on every result.

---

## 2026-03-29 — Modal deployment must pass all parameters to helper functions

**What went wrong:** `modal_app.py` called `build_json_output()` without the `cpa_notes` parameter. CPA notes worked locally but disappeared on the Modal deployment. The endpoint returned JSON with no notes column.

**Fix applied:** Added `cpa_notes` parameter passthrough in `modal_app.py`.

**Rule:** When deploying a local script as a serverless endpoint, diff every function call against the local invocation to verify all parameters are passed. Serverless wrappers silently drop features when optional parameters are omitted.

---

## 2026-03-29 — Reimbursed expenses are Transfers, not Schedule C

**What went wrong:** Expenses reimbursed by Keynote or Itero were initially categorized under Schedule C business expenses. This double-counts the deduction -- the expense lives on the entity's books, not Aaron's personal return.

**Fix applied:** Created "Reimbursed by Keynote" and "Reimbursed by Itero" categories in Monarch under the Transfers group (net-worth neutral). Unreimbursed items stay in "Keynote - X" categories on Schedule C.

**Rule:** When Aaron fronts an expense for a business entity and gets reimbursed, move it to "Reimbursed by [Entity]" (Transfer). Only unreimbursed business expenses belong on Schedule C. The litmus test: did money come back to Aaron? If yes, it's a transfer, not a deduction.

---

## 2026-03-29 — Credit Card Annual Fees net to zero with AMEX reimbursements

**What went wrong:** Credit Card Annual Fees were on a tax schedule, but AMEX reimburses annual fee costs through airline credits and other statement credits. The net is approximately zero and not meaningful for the CPA.

**Fix applied:** Moved "Credit Card Annual Fees" from schedule to personal (excluded). Added comment in `categorization_rules.yaml` explaining the rationale.

**Rule:** Before adding a category to a tax schedule, check whether offsetting credits/reimbursements make the net amount immaterial. Categories that net to zero create noise for the CPA without tax benefit.
