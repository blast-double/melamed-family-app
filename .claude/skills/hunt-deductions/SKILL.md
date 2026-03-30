---
name: hunt-deductions
description: Scan Monarch transactions for missed deductions and miscategorized expenses. Uses a verified training window to learn what's deductible, then hunts for similar patterns in unverified months. Presents batches for review, applies to Monarch with audit trail.
user-invocable: true
---

# Hunt for Missed Deductions

Proactive deduction finder. Uses a verified training window (manually categorized months) to learn deduction patterns, then scans unverified months for transactions that should be deductible but are hiding in personal categories — or are deductible but in the wrong category.

**Safety: Same as /train-categories — dry-run by default, audited, rollback available.**

## Prerequisites

- `MONARCH_EMAIL`, `MONARCH_PASSWORD`, `MONARCH_MFA_SECRET_KEY` in `.env`
- `execution/finance/monarch_client.py` — Monarch API client
- `execution/finance/categorize.py` — categorization engine
- `execution/finance/hunt_deductions.py` — deduction hunter (this skill's engine)
- `config/categorization_rules.yaml` — schedule map
- `config/deduction_patterns.yaml` — learned deduction patterns (persisted across years)

## Invocation

```
/hunt-deductions 2025
/hunt-deductions 2025 --train-only     # just learn patterns, don't hunt
/hunt-deductions 2025 --hunt-only      # hunt using existing patterns, skip training
```

## Workflow

### Step 1: Train — Learn from Verified Months

Pull transactions from the verified training window. Build a deduction profile:

```
Training window: Nov 2025 — Mar 2026

Learned patterns:
  1771 Property Expenses:
    The Home Depot     → "1771 - Maintenance "   (2 occurrences, avg $1,297)
    Zelle (>$100)      → "1771 - Maintenance "   (4 occurrences, avg $288)
    Lowe's             → "1771 - Maintenance "   (1 occurrence, $45)

  Business (Schedule C):
    Adobe              → "Software"               (3 occurrences, avg $55)
    Zoom               → "Software"               (1 occurrence, $15)

  NOT Deductible (learned negatives):
    Uber Eats          → personal (Food Delivery)
    Alaska Airlines    → personal (Air Fare, unless tagged business)
    Hotels             → personal (unless tagged business)
```

Training data captures:
- **Merchant → category mapping** with the CORRECT target category (not Monarch's default)
- **Account context** — which card/account the charge hits
- **Amount ranges** — to distinguish $50 Home Depot (supplies) from $1,900 Home Depot (appliance)
- **Negative patterns** — merchants Aaron deliberately left in personal

Patterns are saved to `config/deduction_patterns.yaml` and persist across tax years.

### Step 2: Hunt — Scan Unverified Months

Scan Jan - Oct 2025 (the unverified period). For each personal transaction, check:

1. **Merchant match**: Same merchant appeared as deductible in training window
2. **Category mismatch**: Transaction is in a generic category (Home Improvement, Shopping) but training says it should be a specific deductible category (1771 - Maintenance)
3. **Property signals**: Hardware stores, contractors, maintenance vendors near known property addresses
4. **Business signals**: Software, professional services, business travel paid from personal cards

### Step 3: Present Batches

Group candidates by deduction type and present ONE batch at a time:

```
=== BATCH 1: Property Expenses (1771 11th Ave) ===

Training says Home Depot → "1771 - Maintenance "
Found 2 transactions in Jan-Oct currently in "Home Improvement" (personal):

  2025-07-31  The Home Depot   $-680.76   Home Improvement  Freedom Unlimited
  2025-11-08  The Home Depot   $-1,913.98 Home Improvement  Freedom Unlimited

Action: Recategorize both to "1771 - Maintenance "? [yes/no/skip/split]
```

Aaron's options per batch:
- **yes** — recategorize all in batch
- **no** — leave all as personal
- **split** — some are deductible, some aren't (Aaron specifies which)
- **skip** — come back to this batch later
- **reclassify** — deductible but different category than suggested

### Step 4: Apply Changes

For confirmed batches:
1. Call `mm.update_transaction(txn_id, category_id=new_id)` for each
2. Log to `config/categorization_audit_{year}.yaml`
3. Update `config/deduction_patterns.yaml` with any new patterns from Aaron's feedback
4. Show updated dashboard totals

### Step 5: Summary

After all batches reviewed, show:
```
Deduction Hunt Summary:
  Property (1771):    +$2,595  (2 txns moved from personal)
  Business (Sched C): +$340    (4 txns moved from personal)
  Skipped:            12 txns  (Aaron reviewed, left as personal)

Updated Schedule E total: -$3,926 (was -$1,331)
```

## Property Context

| Property | Address | Owner | Tax Schedule |
|----------|---------|-------|-------------|
| 1771 11th Ave | San Francisco, CA 94122 | Aaron | Schedule E |
| 140 E 40th St | New York, NY | Aaron's parents | NOT Aaron's deduction |

Hardware store purchases, contractor payments, and maintenance vendors default to 1771 unless Aaron specifies otherwise. 140 E 40th expenses are Aaron's parents' responsibility.

## Pattern File Format

`config/deduction_patterns.yaml`:

```yaml
# Last Updated: YYYY-MM-DD
# Learned from verified training windows. Persists across tax years.
# Each pattern: merchant → target category + metadata

training_windows:
  - start: "2025-11-01"
    end: "2026-03-31"
    year: 2025

patterns:
  # Property expenses (1771 11th Ave, SF 94122)
  - merchant_contains: "home depot"
    target_category: "1771 - Maintenance "
    target_schedule: schedule_e
    confidence: high
    source: training_2025
    note: "Hardware/appliance purchases for rental property"

  - merchant_contains: "lowe"
    target_category: "1771 - Maintenance "
    target_schedule: schedule_e
    confidence: high
    source: training_2025

  # Negative patterns (confirmed personal)
  - merchant_contains: "uber eats"
    target_category: null  # personal, not deductible
    confidence: high
    source: training_2025
    note: "Personal food delivery"

  - merchant_contains: "alaska airlines"
    target_category: null  # personal travel unless tagged
    confidence: medium
    source: training_2025
    note: "Personal travel — only deductible if specific business trip"
```

## Integration with /train-categories

These two skills complement each other:
- `/train-categories` — fixes what's already on tax schedules (wrong categories, unmapped)
- `/hunt-deductions` — finds what's missing (deductible transactions hiding in personal)

Run `/train-categories` first to clean up existing categorizations, then `/hunt-deductions` to find what was missed.

## Error Handling

| Error | Action |
|-------|--------|
| No training window data | Ask Aaron which months are verified |
| Merchant appears in both deductible and personal in training | Flag as ambiguous, present both examples to Aaron |
| Pattern file doesn't exist | Create from scratch using training window |
| Monarch rate limit | Retry with backoff (handled by monarch_client.py) |
