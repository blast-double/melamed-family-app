---
name: train-categories
description: Iterative training loop for Monarch Money transaction categorization. Pulls live transactions, presents batches for review, learns rules from feedback, and applies changes to Monarch with dry-run safety and audit logging.
user-invocable: true
---

# Train Transaction Categories

Iterative training loop to categorize Monarch Money transactions for tax preparation. Reads live from Monarch, presents batches for Aaron's review, captures rules from feedback, and pushes approved changes back to Monarch.

**Safety: All writes are dry-run by default. Every change is audited. Rollback is always available.**

## Prerequisites

- `MONARCH_EMAIL`, `MONARCH_PASSWORD`, `MONARCH_MFA_SECRET_KEY` in `.env`
- `execution/finance/monarch_client.py` — Monarch API client (built)
- `execution/finance/categorize.py` — categorization logic (built)
- `config/categorization_rules.yaml` — schedule map + learned rules

## Workflow

### Step 1: Pull Current State

Run the read-only summary to see where things stand:

```bash
python3 -m execution.finance.categorize --year {year}
```

Show Aaron the schedule-oriented totals and the unmapped count. This is the starting point.

### Step 2: Show Needs-Review Batch

Run with `--needs-review` to see unmapped/ambiguous transactions:

```bash
python3 -m execution.finance.categorize --year {year} --needs-review
```

Present ONE category group at a time to Aaron (e.g., "Here are 31 Uncategorized transactions"). Don't dump all 408 at once.

### Step 3: Aaron Gives Feedback

Aaron tells you what to do with the batch. Examples:
- "The Apple charges are all personal App Store purchases"
- "The Cigna ones are health insurance — deductible"
- "The $150 checks are property management payments for 1771"
- "SOHO LUDLOW is my apartment rent deposit — personal"

### Step 4: Capture Rules

Based on Aaron's feedback, add rules to `config/categorization_rules.yaml`:

```yaml
rules:
  - match: { merchant_contains: "APPLE", account_contains: "Freedom Unlimited" }
    set_category: "iTunes"
    schedule: personal
    confidence: high
    learned_from: "batch_1_{date}"
```

Rules use these match criteria:
- `merchant_contains` — partial match on merchant name (case-insensitive)
- `original_name_contains` — partial match on original statement
- `account_contains` — partial match on account name
- `category_is` — exact match on current Monarch category
- `amount_gt` / `amount_lt` — amount range filters

### Step 5: Dry-Run Proposed Changes

Show Aaron what WOULD change in Monarch if the rules were applied:

```
DRY RUN — Proposed changes for 31 Uncategorized transactions:
  ✓ 20 Apple charges → iTunes (personal)
  ✓ 2 Check Paid → 1771 - Maintenance (Schedule E)
  ? 9 remaining — still need categorization

Apply these changes to Monarch? [yes/no]
```

**NEVER apply without explicit "yes" from Aaron.**

### Step 6: Apply + Audit (only after approval)

For each approved change:
1. Call `mm.update_transaction(transaction_id, category_id=new_category_id)` via the Monarch API
2. Log the change to `config/categorization_audit_{year}.yaml`:

```yaml
batches:
  - batch_id: "batch_1_2025-03-29"
    applied_at: "2026-03-29T10:00:00"
    changes:
      - transaction_id: "abc123"
        old_category: "Uncategorized"
        old_category_id: "166133957812984541"
        new_category: "iTunes"
        new_category_id: "166167555901198855"
```

3. Report: "Applied 20 changes. Audit logged."

### Step 7: Next Batch

Move to the next unmapped category group. Repeat steps 2-6.

As rules accumulate, fewer transactions need review each round. By batch 3-4, most new transactions should auto-resolve.

### Step 8: Verify Final State

After all batches are done, re-run the summary:

```bash
python3 -m execution.finance.categorize --year {year}
```

The unmapped count should be 0 (or near 0). Schedule totals should look correct. Aaron scans for anything off.

## Rollback

If a batch was wrong:

1. Read `config/categorization_audit_{year}.yaml`
2. For each change in the batch, call `mm.update_transaction(transaction_id, category_id=old_category_id)`
3. Log the rollback as a new audit entry

## Tavily Merchant Research

For unknown merchants, use Tavily to research what the business is:

```
tavily_search: "SOHO LUDLOW INC New York what is this business"
```

Then categorize based on the result. Always present the finding to Aaron before acting.

## Error Handling

| Error | Fix |
|---|---|
| Monarch auth failed | Check `.env` credentials, delete stale session at `execution/.credentials/monarch_session` |
| Category ID not found | Run `mm.get_transaction_categories()` to refresh the ID list |
| Transaction already categorized | Show current category, ask Aaron if override is intended |
| Rollback fails | Log the failure, present the audit entry for manual resolution in Monarch web |

## Reference

- **Monarch client**: `execution/finance/monarch_client.py`
- **Categorization logic**: `execution/finance/categorize.py`
- **Rules**: `config/categorization_rules.yaml`
- **Audit log**: `config/categorization_audit_{year}.yaml`
- **Schedule map**: `config/categorization_rules.yaml` → `schedule_map` section
