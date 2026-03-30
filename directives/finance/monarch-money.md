*Last Edited: 2026-03-29*

# Monarch Money: Master Reference

**Purpose**: Master reference for Aaron's Monarch Money setup — accounts, categories, business/personal boundaries, and operational workflows.

**Applies to**: Aaron Melamed's Monarch Money account (personal-side only)

**Scope**: Monarch tracks personal finances. All four businesses (Itero, Keynote Capital, Homeowners First, Palisades Labs) are tracked in QuickBooks. Monarch is not for business accounting — it only sees money as it enters or leaves the personal side.

---

## Account Inventory

### Accounts in Monarch (20)

**Credit Cards**

| Account | Institution | Last 4 | Primary Use |
|---------|-------------|--------|-------------|
| Platinum Card® | American Express | 2001 | Primary personal spending |
| Citi Prestige Card | Citi | 1658 | Travel / premium |
| Ritz Carlton | Chase | 3738 | Travel |
| Freedom Unlimited | Chase | 8013 | Cashback |
| Chase Business United Mileage Plus | Chase | 5600 | Business travel |
| Amazon Business Prime Card | Amazon/Chase | 1001 | Business purchases |
| Ink Business Cash | Chase | 8075 | Business expenses |
| British Airways | Chase | 4276 | Travel |
| Bonvoy Amex Card | American Express | 9005 | Travel / hotels |
| Citi Prestige | Citi | 3041 | Secondary travel |
| BOA Alaska Airlines | Bank of America | 7547 | Travel |
| JetBlue ...3758 | Barclays | 3758 | Travel |
| Hyatt | Chase | 9034 | Travel / hotels |
| Freedom Flex | Chase | 6618 | Cashback |

**Checking**

| Account | Institution | Primary Use |
|---------|-------------|-------------|
| Investor Checking | Charles Schwab | Hub account — receives all income, sends all outbound transfers |
| A. MELAMED | Unknown | 4549 | Secondary checking |

**Savings**

| Account | Institution | Primary Use |
|---------|-------------|-------------|
| Marcus Savings | Goldman Sachs | High-yield savings |
| High Yield Savings Account | American Express | 9193 | High-yield savings |
| Personal Savings | Unknown | 9622 | Savings |

**Property**

| Account | Institution | Primary Use |
|---------|-------------|-------------|
| 1771 11th Ave | ProPay / manual | Rental property income tracking |

### Accounts Intentionally Excluded

| Account | Institution | Why Excluded |
|---------|-------------|--------------|
| Itero checking | Mercury | Business account — tracked in QuickBooks. Link temporarily if needed for inter-company loans (see Business Transaction Rules). |
| Palisades Labs accounts | Various | Business account — tracked in QuickBooks |
| Keynote / Homeowners First accounts | Various | Business account — tracked in QuickBooks |
| BBVA Mexico | BBVA | Plaid does not support Mexican banks. No connection possible. |
| Brokerage -8117 | Charles Schwab | Mixed-use (Mexico wires + investing). Including it would require constant manual categorization of every trade. |
| Coinbase | Coinbase | Only relevant in years with crypto trades. Add conditionally. |

---

## Category Taxonomy

**Source of truth**: `config/categorization_rules.yaml` — contains schedule_map (category → tax schedule) + learned auto-categorization rules. Used by `execution/finance/categorize.py` which pulls live from Monarch API. The tables below are a human-readable reference; the YAML is authoritative for code.

### Schedule E — Rental Property (8 categories)

All expenses and income related to 1771 11th Ave, San Francisco.

| Category | Notes |
|----------|-------|
| Rental Income | ProPay deposits into Investor Checking |
| Mortgage | New American Funding monthly payment |
| Property Tax | San Francisco property tax |
| 1771 - Water | Water utility |
| 1771 - Trash | Waste collection |
| 1771 - Maintenance  | Repairs and upkeep. **Note**: trailing space in Monarch data — must match exactly. |
| 1771 - Software | Property management software |
| 140 - Maintenance | Secondary property maintenance |

### Schedule C — Business Expenses (10 categories)

Deductible business operating expenses.

| Category | Notes |
|----------|-------|
| Office Supplies | General office supplies |
| Cell Phone | T-Mobile, Telcel (Mexico) — business portion |
| Dues & Subscriptions | Professional memberships, SaaS tools |
| Software | General business software |
| Business Utilities & Communication | Phone lines, communication tools |
| Postage & Shipping | Mailing, shipping |
| Keynote - Software | Software specific to Keynote Capital |
| Keynote - Other | Other Keynote Capital expenses |
| Keynote - Real Estate | Keynote real estate expenses |
| Itero - Software | Software specific to Itero |

### Schedule C — Home Office (3 categories)

Home office deduction — rent allocation + utilities for both US and Mexico offices.

| Category | Notes |
|----------|-------|
| Rent | Home office rent allocation |
| Internet & Cable | Home internet — business portion |
| Gas & Electric | Utilities — business portion |

### Estimated Payments (1 category)

| Category | Notes |
|----------|-------|
| Federal Tax | Quarterly estimated tax payments (1040-ES) |

### Reference — Income Reconciliation (5 categories)

Not directly deductible, but CPA needs these for reconciliation against 1099s and K-1s.

| Category | Notes |
|----------|-------|
| Interest Income | Bank/savings interest (matches 1099-INT forms) |
| Other Income | Miscellaneous income |
| Airbnb Income | Short-term rental income |
| Business Income | Distributions from Itero, Palisades Labs, Keynote |
| Special Sales Tax | Sales tax reference |

### Needs Review — Mixed Business/Personal (11 categories)

These contain a mix of deductible business expenses and personal spending. Each transaction must be individually triaged during annual tax prep.

| Category | Why It Needs Review |
|----------|-------------------|
| Restaurants | Business meals vs. personal dining |
| Financial Fees | May include deductible credit card annual fees |
| Financial & Legal Services | May include deductible professional fees |
| Miscellaneous | Catch-all — needs individual review |
| Uncategorized | Not yet categorized in Monarch |
| Check | Unknown purpose — needs review |
| Travel Other | May be business travel |
| Air Fare | May be business travel |
| Hotel | May be business travel |
| Car Rentals | May be business travel |
| Health Insurance | May be deductible depending on business structure |

### Personal — Excluded from Tax Package (47 categories)

Not deductible. Excluded entirely from the tax preparation workflow. These include:

Groceries, Taxi & Ride Shares, Shopping, Clothing, Entertainment & Recreation, Streaming, Music, Coffee Shops, Transfer, Credit Card Payment, Auto Payment, Loan Repayment, Buy Securities, Paychecks, Food Delivery, Ice Cream, Gas, Public Transit, Electronics, Personal, Personal Care, Fitness, Grappling, Spa & Massage, Hair, Nails, Pharmacy, Medical, Eyecare, Pets, Pet Other, Pet Accessories, Vetinary, Home Improvement, Guns & Ammunition, Sporting Goods, Alcohol & Bars, Scooters / Bikes, Shoes, Museums & Galleries, Education, Parking & Tolls, iTunes, Water, Charity, Airbnb Stay

### System Categories

These are Monarch internal categories that represent money movement, not spending:

| Category | Treatment |
|----------|-----------|
| Transfer | Hidden from budgets/cash flow by default. Recategorize Mexico wires manually (see Mexico Living section). |
| Credit Card Payment | Auto-detected. No action needed. |
| Auto Payment | Automatic bill payments. No action needed. |
| Buy Securities | Investment purchases. Not an expense. |
| Loan Repayment | Debt payments. Not an expense. |

---

## Business Transaction Rules

### Rule 1: Inter-Company Loans (Personal ↔ Business)

**Scenario**: Lending money from personal checking to a business (e.g., $15K from Investor Checking to Itero Mercury).

**How to handle**:
1. Link the business bank account (e.g., Mercury) to Monarch via Plaid
2. Exclude the account from budgets (Settings > Accounts > toggle off budget inclusion)
3. Exclude from the transactions feed (toggle off transaction visibility)
4. Mark the outflow/inflow pair as a **Transfer** between accounts
5. When the business repays, the reverse transfer appears automatically
6. Net worth stays accurate; budget is unaffected; no noise

**Why not just hide the transaction?** Net worth would show you $15K poorer than you are. The linked account preserves the full picture — money moved from checking to a receivable, not lost.

**When to unlink**: Once the loan is fully repaid and no further inter-company movement is expected, you can unlink the business account to reduce clutter.

### Rule 2: Business Distributions

**Scenario**: Itero, Palisades Labs, or Keynote Capital sends a distribution to Investor Checking.

**How to handle**: Categorize as **Business Income** (a reference category). This is not a deduction — the CPA needs it for reconciliation against K-1s and business tax returns.

**What NOT to do**: Don't categorize as "Transfer" — distributions are income, not money movement between your own accounts. Don't categorize as "Paychecks" — that's for W-2 wages (not applicable since 2025).

### Rule 3: Business Credit Cards

**Scenario**: Chase Business United Mileage Plus, Amazon Business Prime, and Ink Business Cash are business cards tracked in Monarch for visibility.

**How to handle**: Categorize expenses on these cards with the appropriate business prefix:
- Itero expenses → "Itero - Software" or general "Software", "Office Supplies", etc.
- Keynote expenses → "Keynote - Software", "Keynote - Other", "Keynote - Real Estate"
- Cross-business → use the most relevant category

**Why these are in Monarch**: Visibility into total spending across personal + business. QuickBooks tracks the business accounting; Monarch provides the unified cash flow view.

### Rule 4: K-1 Passthrough Income (Keynote / Homeowners First)

**Scenario**: Keynote Capital issues a K-1 showing passthrough income from Homeowners First.

**How to handle**: **Nothing in Monarch.** K-1 income is a tax reporting event, not a bank transaction. It appears on the tax return via the K-1 form from the entity's filing. The only Monarch-visible event is when Keynote actually distributes cash (→ Rule 2).

### Rule 5: Mixed-Use Expenses

**Scenario**: Restaurants, airfare, hotels, car rentals — could be business or personal.

**How to handle**: Categorize in the moment using your best judgment. During annual tax prep, the `/train-categories` skill uses the multi-signal categorization engine to auto-classify transactions. Ambiguous ones get presented for Aaron's review in batches.

**Business meal test**: Was the meal with a client, prospect, or business partner, and was business discussed? If yes → deductible at 50%. If it was just dinner out → personal.

### Rule 6: Rental Property (1771 11th Ave)

**Scenario**: Rental income and expenses for the San Francisco property.

**How to handle**:
- The **1771 11th Ave** account in Monarch tracks rental income (ProPay deposits)
- All **1771-prefixed categories** map to Schedule E automatically
- ProPay deposits appearing in Investor Checking → categorize as **Rental Income**
- Mortgage payment → **Mortgage** category
- Property tax → **Property Tax** category

---

## Mexico Living

Aaron lives in Mexico City. Money flows: Investor Checking → Schwab Brokerage -8117 → international wire → BBVA Mexico → peso spending.

Monarch sees the first leg as a "Transfer" to the brokerage, which is invisible in budgets. Mexico wires must be manually recategorized from "Transfer" to "Mexico Living" each month.

**Full workflow**: See `directives/finance/monarch-money-mexico-transfers.md`

---

## Active Monarch Rules

| Rule | Trigger | Action | Notes |
|------|---------|--------|-------|
| Venmo payments | Merchant contains `VENMO PAYMENT` + Account = Investor Checking | Category → Miscellaneous | Does NOT apply to `VENMO CASHOUT` (those stay as Transfer) |

**Do NOT create a rule for**: Brokerage transfers (mixed-use), business card expenses (vary too much), rental income (needs manual verification).

---

## Monthly Workflow

**Time**: ~15 minutes/month

1. **Review uncategorized transactions** — Open Transactions, filter by "Uncategorized". Assign proper categories. (33 uncategorized in 2025 — keep this at zero.)
2. **Recategorize Mexico wires** — Find new "Funds Transfer to Brokerage -8117" in Investor Checking, change to "Mexico Living" for actual wire transfers. (~1 min, see Mexico Living directive.)
3. **Spot-check business cards** — Review recent Chase Business / Amazon Business Prime / Ink Business Cash transactions. Ensure they have the right business-prefix category.
4. **Review large transactions** — Sort by amount, scan for anything miscategorized or unexpected.
5. **Verify credit card payments** — Confirm Credit Card Payment transactions match actual payments. Flag any discrepancies.

---

## Annual Tax-Season Workflow

1. **Run `/train-categories`** — pulls live from Monarch API, applies multi-signal categorization engine (Monarch rules + schedule map + merchant history + tap detection), presents batches for review
2. **Aaron reviews and gives feedback** — Claude auto-categorizes, Aaron corrects mistakes. Rules get tighter each batch. Dry-run before any Monarch writes.
3. **Run summary**: `python3 -m execution.finance.categorize --year {year}` — shows deductible transactions grouped by tax schedule with totals
4. **Aaron verifies totals** — scans the read-only summary, tells Claude what's wrong. Claude fixes in Monarch.
5. **CPA verification** — portal at `tax-portal/` shows the same summary + extracted PDF data for Jessica to verify and copy

---

## What NOT To Do

| Don't | Why |
|-------|-----|
| Track business operations in Monarch | That's QuickBooks. Monarch is personal-side only. |
| Create a manual BBVA Mexico account | Monarch has no multi-currency support. MXN amounts display as "$" with no conversion, creating misleading totals. |
| Auto-rule brokerage transfers | Schwab Brokerage -8117 is mixed-use (Mexico wires + investing). A rule would mis-categorize investment transfers as expenses. |
| Categorize inter-company loans as expenses | A loan is an asset (receivable), not spending. Link the business account and mark as transfer. |
| Ignore "Uncategorized" transactions | Every uncategorized transaction is a gap in your financial picture. Zero tolerance. |
| Duplicate K-1 income as a Monarch transaction | K-1 passthrough is a tax event, not a bank transaction. Only actual cash distributions appear in Monarch. |
| Create categories for one-off items | Use existing categories. If a new recurring pattern emerges, add to `config/categorization_rules.yaml` schedule_map first, then create in Monarch. |

---

## Edge Cases

- **New credit card added**: Add to Monarch via Plaid. Update the Account Inventory table in this directive. Default categorization rules apply — no special setup needed.
- **New recurring expense category needed**: First add to `config/categorization_rules.yaml` under the correct schedule in `schedule_map`, then create the category in Monarch. The YAML is the source of truth.
- **Trailing spaces in category names**: "1771 - Maintenance " has a trailing space in Monarch's data. The YAML and categorization engine account for this. Do not "fix" it in Monarch — it would break the match.
- **Duplicate transactions**: Monarch occasionally creates duplicates when Plaid re-syncs. Delete the duplicate manually.
- **Large one-time transfers**: Categorize by what the transfer actually is. A $15K loan to Itero is a transfer (Rule 1). A $10K Mexico wire is Mexico Living. Don't split across months.
- **Personal purchase on business card**: Categorize as the personal category it actually is (e.g., "Groceries" on Ink Business Cash). The card doesn't determine the category — the expense does.
- **Refunds**: Monarch usually auto-matches refunds. If it doesn't, categorize the refund under the same category as the original purchase (negative amount reduces the category total).
- **Business account linked temporarily (Rule 1)**: When unlinking, verify the loan is fully repaid first. Any outstanding balance disappears from net worth when the account is removed.

---

## References

### Config Files
- `config/categorization_rules.yaml` — Schedule map + learned auto-categorization rules (source of truth for code)
- `config/monarch_rules.yaml` — Aaron's 204 Monarch auto-categorization rules (extracted from Settings > Rules)
- `config/tax_config.yaml` — Per-year tax settings (active institutions, conditional items)
- `config/tax_documents_master.yaml` — Master checklist of all tax documents
- `config/categorization_audit_2025.yaml` — Audit log of all Monarch writes (rollback capable)

### Execution Tools
- `execution/finance/monarch_client.py` — Monarch API client (async, session-first auth)
- `execution/finance/categorize.py` — Multi-signal categorization engine (pulls live from Monarch)
- `execution/tax/match_files.py` — Matches downloaded tax documents to expected items
- `execution/tax/extract_pdf.py` — Google Document AI OCR for PDF extraction

### Related Directives
- `directives/finance/monarch-money-mexico-transfers.md` — Mexico living expense tracking (detailed workflow)
- `directives/tax/tax-preparation.md` — Full tax preparation SOP
- `directives/reference/tax_profile.md` — Complete tax situation (income sources, deductions, filing)
- `directives/reference/business_profiles.md` — Four-business portfolio details

### Monarch Money Limitations
- **No multi-currency**: USD and CAD only. No conversion engine.
- **Transfer = invisible**: Transfer category excluded from budgets and cash flow by design.
- **Plaid coverage**: No Mexico, limited international. Some US institutions have intermittent sync issues.
- **Manual on synced accounts**: Manual transactions on synced accounts do NOT change the synced balance.
- **Rule criteria**: Merchant (exact/contains), Original Statement, Amount (equals/greater/less/range), Account, Category.
- **Retroactive rules**: "Apply to existing transactions" checkbox updates matching historical transactions.
- **Bulk edit**: Web → "Edit multiple" button at top of transaction list. Mobile → checkbox icon.
