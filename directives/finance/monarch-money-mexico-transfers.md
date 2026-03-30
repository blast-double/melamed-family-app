*Last Edited: 2026-03-27*

# Monarch Money: Mexico Living Expenses & Transfer Categorization

**Purpose**: Fix three blind spots in Monarch Money that cause Mexico living costs and Venmo payments to be invisible in budgets and cash flow reports.

**Applies to**: Aaron Melamed's Monarch Money account

---

## Background

Aaron lives in Mexico City. The money flow to fund Mexico living is:

```
Investor Checking (Schwab) → Brokerage -8117 (Schwab) → International Wire → BBVA Mexico → Peso spending
```

Monarch sees money leave Investor Checking as a "Transfer" to the brokerage, but:
- The brokerage is **mixed-use** (Mexico wires + investing), so not all transfers are Mexico spending
- BBVA Mexico is **not connected** (Plaid doesn't support Mexico)
- Monarch has **no multi-currency support** — it only handles USD/CAD

This means Mexico living costs are excluded from budgets and cash flow reports because "Transfer" transactions are hidden from those views.

Similarly, Venmo payments default to "Transfer" but are expenses to third parties.

---

## Step 1: Create "Mexico Living" Expense Category

### Desktop (web)

1. Navigate to **Settings > Categories**
2. Scroll to the **Expenses** section
3. Click **Create Category**
4. Choose an icon (flag or house emoji)
5. Name: **Mexico Living**
6. Confirm the group — use an existing Expenses group (e.g., "Home") or create a custom "International" group
7. Leave **"Exclude this category from the budget"** toggled **OFF** — this must appear in the budget
8. Leave **"Make this category a monthly rollover"** OFF
9. Click **Save**

### Mobile

1. Tap your profile icon > **Settings > Categories**
2. Find the Expenses group
3. Tap the **+** icon > **Add a category**
4. Name: **Mexico Living**, pick an emoji
5. Type of category: **Expense**
6. Group: appropriate Expenses group
7. Save

---

## Step 2: Recategorize Past Brokerage-to-Mexico Transfers (One-Time)

The brokerage is mixed-use, so you must manually identify which "Funds Transfer to Brokerage -8117" transactions were for Mexico wires vs. investments.

### Desktop (web)

1. Go to the **Transactions** page
2. Use the **search bar** to search: `Funds Transfer` or `Brokerage -8117`
3. Filter by **Account**: **Investor Checking**
4. Review the results — identify which transfers were for Mexico wires (you know which ones you wired to BBVA)
5. Click the **"Edit multiple"** button (top of transaction list)
6. Check the boxes next to the Mexico-wire transactions
7. Change category from **Transfer** → **Mexico Living**
8. Save

### If editing one at a time

1. Click on the transaction
2. Click the **Category** field
3. Change from **Transfer** to **Mexico Living**
4. A "Create rule" widget may appear — **do NOT create a rule** (mixed-use means we can't auto-categorize all brokerage transfers)

### What to look for

- **Original statement**: `Funds Transfer to Brokerage -8117`
- **Account**: `Investor Checking`
- Amounts vary — $1,500/month is typical for recurring wires, plus occasional larger amounts

---

## Step 3: Ongoing Monthly Workflow

**Time**: ~1 minute per month

Each time a new wire to Mexico goes through:

1. Open Monarch → **Transactions**
2. Find the new "Funds Transfer to Brokerage -8117" transaction in Investor Checking
3. Click it → change category to **Mexico Living**
4. **Do NOT create a rule** — the brokerage is mixed-use

**Tip**: Set a monthly calendar reminder to review Investor Checking transfers and recategorize the Mexico wires.

---

## Step 4: Create Venmo Transaction Rule

Venmo payments to third parties are expenses, not transfers. This rule defaults them to an expense category so they appear in your budget.

### Desktop (web)

1. Go to **Settings > Rules**
2. Click **Create rule**
3. Under **"If transaction matches"** set these criteria:
   - **Merchant**: select **Contains** → type `VENMO PAYMENT`
   - **Account**: select **Investor Checking**
4. Under **"Then apply these updates"**:
   - **Category**: select **Miscellaneous** (or another general expense category you prefer)
5. Click the **"Preview changes"** tab to see which existing transactions will be affected
6. Check the box: **"Apply # changes to existing transactions"** — this retroactively recategorizes all past Venmo payments
7. Click **Save**

### Why this works

- The rule only targets `VENMO PAYMENT` (outbound payments to people) — not `VENMO CASHOUT` (money returning to your bank)
- VENMO CASHOUT transactions should remain as **Transfer** — they're your own money moving back
- After applying: future Venmo payments auto-categorize as Miscellaneous instead of being hidden in Transfer
- You can still recategorize individual Venmo payments to more specific categories (dining, services, etc.) during monthly reviews

---

## What NOT To Do

| Don't | Why |
|-------|-----|
| Create a manual BBVA Mexico account | Monarch has no multi-currency support. MXN amounts display as "$" with no conversion, creating misleading totals and a confusing net worth calculation |
| Try to connect BBVA via Plaid | Mexico is not a supported Plaid region. Will fail. |
| Track individual peso transactions | Too much manual work for no payoff. The wire amount IS your Mexico spending figure. |
| Create an auto-rule for brokerage transfers | The account is mixed-use (wires + investing). A rule would mis-categorize investment transfers as expenses. |
| Recategorize Venmo CASHOUT | Those are legitimate transfers — your own money returning from Venmo to your bank |

---

## Reference

### Accounts

| Account | Platform | Role in Monarch |
|---------|----------|-----------------|
| Investor Checking | Schwab | Hub account — receives income, sends to brokerage. Synced. |
| Brokerage -8117 | Schwab | Pass-through for international wires + investing. **Not in Monarch.** |
| BBVA Mexico | BBVA | Receives USD wire, holds pesos. **Not in Monarch.** |

### Transaction Patterns

| Original Statement | Current Category | Correct Category |
|-------------------|-----------------|-----------------|
| `Funds Transfer to Brokerage -8117` (Mexico wire) | Transfer | **Mexico Living** |
| `Funds Transfer to Brokerage -8117` (investing) | Transfer | Transfer (no change) |
| `VENMO PAYMENT` (outbound) | Transfer | **Miscellaneous** (or specific expense) |
| `VENMO CASHOUT` (inbound) | Transfer | Transfer (no change) |

### Monarch Money Limitations

- **No multi-currency**: all amounts display as "$" with no conversion engine. Only USD and CAD recommended.
- **Transfer = invisible**: the Transfer category is excluded from budget and cash flow reports by design.
- **Rule criteria**: Merchant (exact/contains), Original Statement, Amount (equals/greater/less/range), Account, Category.
- **Retroactive rules**: "Apply to existing transactions" checkbox updates matching historical transactions.
- **Bulk edit**: Web → "Edit multiple" button at top of transaction list. Mobile → checkbox icon.
- **Manual on synced accounts**: manual transactions added to synced accounts do NOT change the synced balance.

---

## Edge Cases

- **Large one-time transfers**: If you wire a large lump sum (e.g., $10k+) to Mexico that covers several months, categorize the full amount as Mexico Living in the month it left Investor Checking. Don't try to split it across months.
- **Brokerage refund / wire return**: If a wire fails and money returns from brokerage to checking (`Funds Transfer from Brokerage -8117`), categorize it as Transfer (or negative Mexico Living if you had already recategorized the outbound).
- **Venmo for business**: If any Venmo payments are business expenses (Palisades Labs, Itero, etc.), recategorize those from Miscellaneous to the appropriate business expense category.
