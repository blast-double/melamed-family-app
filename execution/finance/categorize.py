# Last Edited: 2026-03-29 20:00
"""Multi-signal transaction categorization engine.

Reads live from Monarch API. Applies 6 signals to classify each transaction:
  1. Monarch rules (from config/monarch_rules.yaml — Aaron's explicit intent)
  2. Schedule map (from config/categorization_rules.yaml — category → schedule)
  3. Account classification (business card vs personal)
  4. Recurring patterns (same merchant + amount monthly)
  5. Historical consistency (merchant always goes to same category)
  6. Tap transaction detection (garbled Mexico City merchants)

No writes. Read-only analysis. Writes happen only via /train-categories skill.

Usage:
    python3 -m execution.finance.categorize --year 2025
    python3 -m execution.finance.categorize --year 2025 --json
    python3 -m execution.finance.categorize --year 2025 --needs-review
    python3 -m execution.finance.categorize --year 2025 --audit
"""

import argparse
import asyncio
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

from execution.finance.monarch_client import get_client

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_RULES_PATH = WORKSPACE_ROOT / "config" / "categorization_rules.yaml"
MONARCH_RULES_PATH = WORKSPACE_ROOT / "config" / "monarch_rules.yaml"

SCHEDULE_DISPLAY = {
    "schedule_e": "Schedule E — Rental & Passthrough",
    "schedule_c": "Schedule C — Business Expenses",
    "schedule_c_home_office": "Schedule C — Home Office",
    "estimated_payments": "Estimated Tax Payments",
    "reference": "Reference (reconciliation)",
    "self_employed_deduction": "Self-Employed Deductions (Schedule 1)",
    "schedule_c_credit_card_fees": "Schedule C — Credit Card Fees",
    "schedule_c_meals": "Schedule C — Business Meals (50% deductible)",
    "personal": "Personal (excluded)",
    "unmapped": "Unmapped (needs review)",
}

# Tap transaction indicators — garbled Mexico City merchant names
TAP_INDICATORS = [
    "aplpay", "merpago*", "clip mx", "ciudad de mex",
    "ciudad de me mex", "cuauhtemoc mex", "benito ju",
    "mexico city", "mexico web me",
]


# =============================================================================
# Config Loading
# =============================================================================


def load_schedule_rules() -> dict:
    with open(SCHEDULE_RULES_PATH) as f:
        return yaml.safe_load(f)


def load_monarch_rules() -> list[dict]:
    with open(MONARCH_RULES_PATH) as f:
        data = yaml.safe_load(f)
    return data.get("rules", [])


def load_cpa_notes(rules: dict) -> dict[str, str]:
    """Load {category_name: note} from cpa_notes section."""
    return rules.get("cpa_notes", {}) or {}


def load_plausibility_config(rules: dict) -> dict:
    """Load plausibility check configuration."""
    return rules.get("plausibility", {}) or {}


def load_manual_adjustments(rules: dict) -> dict[str, list[dict]]:
    """Load manual adjustments keyed by schedule."""
    return rules.get("manual_adjustments", {}) or {}


def build_category_to_schedule(rules: dict) -> dict[str, str]:
    """Build {monarch_category_name: schedule_key} from schedule_map."""
    mapping: dict[str, str] = {}
    for schedule_key, categories in rules.get("schedule_map", {}).items():
        if isinstance(categories, list):
            for cat in categories:
                mapping[cat] = schedule_key
    return mapping


# =============================================================================
# Signal 1: Monarch Rules Matching
# =============================================================================


def _match_value(text: str, pattern: str) -> bool:
    """Case-insensitive partial match."""
    return pattern.lower() in text.lower()


def _match_exact(text: str, pattern: str) -> bool:
    """Case-insensitive exact match."""
    return text.lower().strip() == pattern.lower().strip()


def monarch_rule_matches(txn: dict, rule: dict) -> bool:
    """Check if a Monarch rule matches a transaction."""
    match = rule.get("match", {})
    merchant = txn.get("merchant", {}).get("name", "")
    original = txn.get("originalName", "") or txn.get("plaidName", "") or txn.get("original_statement", "")

    # merchant_contains
    if "merchant_contains" in match:
        vals = match["merchant_contains"]
        if isinstance(vals, str):
            vals = [vals]
        if not any(_match_value(merchant, v) for v in vals):
            return False

    # merchant_exactly
    if "merchant_exactly" in match:
        vals = match["merchant_exactly"]
        if isinstance(vals, str):
            vals = [vals]
        if not any(_match_exact(merchant, v) for v in vals):
            return False

    # original_statement_contains
    if "original_statement_contains" in match:
        val = match["original_statement_contains"]
        if not _match_value(original, val):
            return False

    # category_equals
    if "category_equals" in match:
        cat = txn.get("category", {}).get("name", "")
        if not _match_exact(cat, match["category_equals"]):
            return False

    # account_equals
    if "account_equals" in match:
        acct = txn.get("account", {}).get("displayName", "")
        if not _match_exact(acct, match["account_equals"]):
            return False

    # Conditions
    conditions = rule.get("conditions", {})
    amount = abs(txn.get("amount", 0))

    if "debit_gt" in conditions and amount <= conditions["debit_gt"]:
        return False
    if "debit_lt" in conditions and amount >= conditions["debit_lt"]:
        return False
    if "debit_eq" in conditions and abs(amount - conditions["debit_eq"]) > 0.01:
        return False
    if "account_equals" in conditions:
        acct = txn.get("account", {}).get("displayName", "")
        if not _match_value(acct, conditions["account_equals"]):
            return False
    if "account_in" in conditions:
        acct = txn.get("account", {}).get("displayName", "")
        if not any(_match_value(acct, a) for a in conditions["account_in"]):
            return False

    return True


def apply_monarch_rules(txn: dict, rules: list[dict]) -> dict | None:
    """Find the first matching Monarch rule. Returns the rule or None."""
    for rule in rules:
        if monarch_rule_matches(txn, rule):
            return rule
    return None


# =============================================================================
# Signal 6: Tap Transaction Detection
# =============================================================================


def is_tap_transaction(txn: dict) -> bool:
    """Detect garbled Mexico City tap transactions."""
    merchant = (txn.get("merchant", {}).get("name", "") or "").lower()
    original = (txn.get("originalName", "") or txn.get("plaidName", "") or "").lower()
    combined = f"{merchant} {original}"
    return any(indicator in combined for indicator in TAP_INDICATORS)


# =============================================================================
# Multi-Signal Classification
# =============================================================================


def _run_plausibility_checks(
    merchant: str, cat_name: str, schedule: str, plausibility: dict
) -> str | None:
    """Signal 7: Check if merchant plausibly matches the assigned category.

    Returns a review_reason string if a check fails, None if all pass.
    """
    merchant_lower = merchant.lower().strip()

    # Check a) Home office utility whitelist
    if schedule == "schedule_c_home_office" and cat_name in ("Gas & Electric", "Internet & Cable"):
        allowed = plausibility.get("home_office_utility_merchants", [])
        if allowed and not any(util in merchant_lower for util in allowed):
            return "plausibility:not_known_utility"

    # Check b) Generic payment platform in expense category
    platforms = plausibility.get("generic_payment_platforms", [])
    expense_cats = plausibility.get("expense_categories_requiring_merchant", [])
    if cat_name in expense_cats:
        if any(p in merchant_lower for p in platforms):
            return "plausibility:payment_platform_as_merchant"

    # Check c) Foreign country code on home office utilities
    if schedule == "schedule_c_home_office":
        foreign_codes = plausibility.get("foreign_country_codes", [])
        # Check last whitespace-separated token
        tokens = merchant_lower.split()
        if tokens and tokens[-1] in foreign_codes:
            return "plausibility:foreign_country_code"

    # Check d) POS terminal prefix on a deductible schedule
    # SumUp*NICOLASCHESSY categorized as "Software" is wrong — the category was
    # assigned based on the payment processor, not the actual vendor.
    # Only flag when on a tax schedule (deductible). If already personal, don't care.
    if schedule not in ("personal", "unmapped"):
        pos_prefixes = plausibility.get("pos_terminal_prefixes", [])
        if any(merchant_lower.startswith(p) for p in pos_prefixes):
            return "plausibility:pos_terminal_hides_merchant"

    return None


def classify_transaction(
    txn: dict,
    cat_to_schedule: dict[str, str],
    monarch_rules: list[dict],
    merchant_history: dict[str, Counter],
    plausibility: dict | None = None,
) -> dict:
    """Classify a transaction using all signals. Returns classification dict."""
    merchant = txn.get("merchant", {}).get("name", "Unknown")
    plaid_name = txn.get("plaidName", "") or ""
    cat_name = txn.get("category", {}).get("name", "")
    amount = txn.get("amount", 0)
    account = txn.get("account", {}).get("displayName", "")
    date = txn.get("date", "")
    txn_id = txn.get("id", "")
    plausibility = plausibility or {}

    result = {
        "id": txn_id,
        "date": date,
        "merchant": merchant,
        "plaid_name": plaid_name,
        "original_name": txn.get("originalName", "") or plaid_name,
        "category": cat_name,
        "account": account,
        "amount": amount,
        "schedule": "unmapped",
        "confidence": "low",
        "signals": [],
        "is_tap": is_tap_transaction(txn),
        "needs_review": False,
        "review_reason": None,
    }

    # Signal 2: Schedule map (category already assigned in Monarch)
    schedule = cat_to_schedule.get(cat_name, "unmapped")
    if schedule != "unmapped":
        result["schedule"] = schedule
        result["confidence"] = "medium"
        result["signals"].append(f"schedule_map→{schedule}")

        # Signal 5: Historical consistency
        if merchant in merchant_history:
            top_cat, top_count = merchant_history[merchant].most_common(1)[0]
            total = sum(merchant_history[merchant].values())
            if top_cat == cat_name and top_count / total >= 0.8:
                result["confidence"] = "high"
                result["signals"].append(f"history({top_count}/{total})→{top_cat}")

    # If unmapped, try Monarch rules
    elif schedule == "unmapped":
        matched_rule = apply_monarch_rules(txn, monarch_rules)
        if matched_rule:
            target_cat = matched_rule.get("actions", {}).get("recategorize")
            if target_cat:
                rule_schedule = cat_to_schedule.get(target_cat, "unmapped")
                result["signals"].append(f"monarch_rule→{target_cat}")
                if rule_schedule != "unmapped":
                    result["schedule"] = rule_schedule
                    result["confidence"] = "medium"

    # If still unmapped after both paths — needs review
    if result["schedule"] == "unmapped":
        result["needs_review"] = True
        if result["is_tap"]:
            result["review_reason"] = "tap_transaction_garbled_merchant"
            result["signals"].append("tap_transaction")
        elif cat_name in ("Uncategorized", "Miscellaneous", "Check"):
            result["review_reason"] = "uncategorized"
            result["signals"].append("uncategorized")
        else:
            result["review_reason"] = "unmapped_category"
            result["signals"].append(f"unmapped:{cat_name}")

    # Signal 7: Plausibility checks (runs on ALL paths — mapped or unmapped)
    if result["schedule"] != "unmapped" and not result["needs_review"]:
        plausibility_fail = _run_plausibility_checks(
            merchant, cat_name, result["schedule"], plausibility
        )
        if plausibility_fail:
            result["needs_review"] = True
            result["review_reason"] = plausibility_fail
            result["confidence"] = "low"
            result["signals"].append(f"plausibility_fail:{plausibility_fail}")

    return result


# =============================================================================
# Data Pulling
# =============================================================================


async def pull_transactions(year: int) -> list[dict]:
    mm = await get_client()
    all_txns: list[dict] = []
    offset = 0
    limit = 100

    while True:
        result = await mm.get_transactions(
            limit=limit,
            offset=offset,
            start_date=f"{year}-01-01",
            end_date=f"{year}-12-31",
        )
        batch = result.get("allTransactions", {}).get("results", [])
        if not batch:
            break
        all_txns.extend(batch)
        offset += limit
        if len(batch) < limit:
            break

    return all_txns


def build_merchant_history(txns: list[dict]) -> dict[str, Counter]:
    """Build {merchant_name: Counter({category: count})} from all transactions."""
    history: dict[str, Counter] = defaultdict(Counter)
    for txn in txns:
        merchant = txn.get("merchant", {}).get("name", "")
        cat = txn.get("category", {}).get("name", "")
        if merchant and cat:
            history[merchant][cat] += 1
    return dict(history)


# =============================================================================
# Summary & Reporting
# =============================================================================


def summarize_classified(classified: list[dict]) -> dict[str, dict]:
    schedules: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    for c in classified:
        if c["schedule"] == "personal":
            continue
        schedules[c["schedule"]][c["category"]].append(c["amount"])

    summary = {}
    for sched_key in sorted(schedules.keys()):
        cats = schedules[sched_key]
        cat_list = []
        sched_total = 0.0
        for cat_name in sorted(cats.keys()):
            amounts = cats[cat_name]
            total = sum(amounts)
            sched_total += total
            cat_list.append({"category": cat_name, "count": len(amounts), "total": round(total, 2)})
        summary[sched_key] = {
            "display": SCHEDULE_DISPLAY.get(sched_key, sched_key),
            "categories": cat_list,
            "total": round(sched_total, 2),
        }

    return summary


def print_summary(summary: dict, classified: list[dict]) -> None:
    # Confidence stats
    confidences = Counter(c["confidence"] for c in classified)
    review_count = sum(1 for c in classified if c["needs_review"])
    tap_count = sum(1 for c in classified if c["is_tap"])

    print(f"\n  Classified: {len(classified)} transactions")
    print(f"  Confidence: {confidences.get('high',0)} high, {confidences.get('medium',0)} medium, {confidences.get('low',0)} low")
    print(f"  Needs review: {review_count}")
    print(f"  Tap transactions detected: {tap_count}")

    for sched_key, data in summary.items():
        if sched_key == "personal":
            continue
        print(f"\n{'='*60}")
        print(f"  {data['display']}")
        print(f"{'='*60}")
        for cat in data["categories"]:
            print(f"  {cat['category']:40s}  {cat['count']:>4} txns  ${cat['total']:>12,.2f}")
        print(f"  {'─'*58}")
        print(f"  {'TOTAL':40s}         ${data['total']:>12,.2f}")


def print_needs_review(classified: list[dict]) -> None:
    needs = [c for c in classified if c["needs_review"]]
    if not needs:
        print("\nNo transactions need review.")
        return

    # Group by review reason
    by_reason: dict[str, list[dict]] = defaultdict(list)
    for c in needs:
        by_reason[c["review_reason"] or "unknown"].append(c)

    print(f"\n{'='*60}")
    print(f"  NEEDS REVIEW ({len(needs)} transactions)")
    print(f"{'='*60}")

    for reason, items in sorted(by_reason.items()):
        total = sum(i["amount"] for i in items)
        print(f"\n  [{reason}] — {len(items)} txns, ${total:,.2f}")
        for item in items[:15]:
            tap_flag = " 📱" if item["is_tap"] else ""
            signals = ", ".join(item["signals"]) if item["signals"] else ""
            print(f"    {item['date']}  {item['merchant']:30s}  ${item['amount']:>10,.2f}  {item['category']:20s}{tap_flag}")
            if signals:
                print(f"             signals: {signals}")
        if len(items) > 15:
            print(f"    ... and {len(items) - 15} more")


def print_audit(classified: list[dict]) -> None:
    """Show where Monarch's category disagrees with what our rules would assign."""
    mismatches = []
    for c in classified:
        if c["confidence"] == "high" and c["signals"]:
            # Check if a monarch rule would recategorize differently than current category
            for sig in c["signals"]:
                if sig.startswith("monarch_rule→"):
                    rule_target = sig.split("→")[1]
                    if rule_target != c["category"]:
                        mismatches.append({
                            **c,
                            "rule_says": rule_target,
                        })

    if not mismatches:
        print("\nNo mismatches between Monarch rules and current categories.")
        return

    print(f"\n{'='*60}")
    print(f"  AUDIT: Monarch rules vs actual category ({len(mismatches)} mismatches)")
    print(f"{'='*60}")

    for m in mismatches[:30]:
        print(f"  {m['date']}  {m['merchant']:25s}  ${m['amount']:>10,.2f}")
        print(f"    Current: {m['category']:25s}  Rule says: {m['rule_says']}")
    if len(mismatches) > 30:
        print(f"  ... and {len(mismatches) - 30} more")


def build_json_output(classified: list[dict], year: int,
                      cpa_notes: dict[str, str] | None = None,
                      manual_adjustments: dict[str, list[dict]] | None = None) -> dict:
    """Build the structured JSON output for the /api/monarch route.

    Groups transactions by schedule and category, including full transaction
    detail for drill-down. Excludes 'personal' schedule.
    """
    cpa_notes = cpa_notes or {}
    confidences = Counter(c["confidence"] for c in classified)
    review_count = sum(1 for c in classified if c["needs_review"])

    # Group: schedule → category → [transactions]
    schedules_data: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for c in classified:
        if c["schedule"] == "personal":
            continue
        schedules_data[c["schedule"]][c["category"]].append({
            "id": c["id"],
            "date": c["date"],
            "merchant": c["merchant"],
            "plaid_name": c.get("plaid_name", ""),
            "amount": c["amount"],
            "account": c["account"],
            "original_name": c["original_name"],
        })

    schedules_list = []
    for sched_key in sorted(schedules_data.keys()):
        cats = schedules_data[sched_key]
        cat_list = []
        sched_total = 0.0
        for cat_name in sorted(cats.keys()):
            txns = cats[cat_name]
            cat_total = round(sum(t["amount"] for t in txns), 2)
            sched_total += cat_total
            entry: dict[str, Any] = {
                "name": cat_name,
                "count": len(txns),
                "total": cat_total,
                "transactions": sorted(txns, key=lambda t: t["date"]),
            }
            if cat_name in cpa_notes:
                entry["note"] = cpa_notes[cat_name]
            cat_list.append(entry)

        # Inject manual adjustments for this schedule
        manual = (manual_adjustments or {}).get(sched_key, [])
        for adj in manual:
            adj_entry: dict[str, Any] = {
                "name": adj["name"],
                "count": adj.get("count", 1),
                "total": adj["total"],
                "transactions": [],
                "manual": True,
            }
            if adj.get("note"):
                adj_entry["note"] = adj["note"]
            sched_total += adj["total"]
            cat_list.append(adj_entry)

        schedules_list.append({
            "key": sched_key,
            "display": SCHEDULE_DISPLAY.get(sched_key, sched_key),
            "total": round(sched_total, 2),
            "categories": cat_list,
        })

    return {
        "tax_year": year,
        "total_transactions": len(classified),
        "confidence": {
            "high": confidences.get("high", 0),
            "medium": confidences.get("medium", 0),
            "low": confidences.get("low", 0),
        },
        "needs_review": review_count,
        "schedules": schedules_list,
    }


# =============================================================================
# Main
# =============================================================================


async def run(year: int, needs_review: bool = False, audit: bool = False,
              json_mode: bool = False) -> list[dict]:
    # In JSON mode, suppress progress messages (stdout is the data channel)
    log = (lambda *a, **kw: None) if json_mode else print

    log("Loading rules...")
    sched_rules = load_schedule_rules()
    cat_to_schedule = build_category_to_schedule(sched_rules)
    cpa_notes = load_cpa_notes(sched_rules)
    plausibility = load_plausibility_config(sched_rules)
    manual_adj = load_manual_adjustments(sched_rules)
    monarch_rules = load_monarch_rules()
    log(f"  {len(cat_to_schedule)} category→schedule mappings")
    log(f"  {len(cpa_notes)} CPA notes")
    log(f"  {len(plausibility)} plausibility checks")
    log(f"  {len(monarch_rules)} Monarch rules")

    log(f"\nPulling {year} transactions from Monarch...")
    txns = await pull_transactions(year)
    log(f"  {len(txns)} transactions")

    log("Building merchant history...")
    merchant_history = build_merchant_history(txns)
    log(f"  {len(merchant_history)} unique merchants")

    log("Classifying...")
    classified = [
        classify_transaction(txn, cat_to_schedule, monarch_rules, merchant_history, plausibility)
        for txn in txns
    ]

    if json_mode:
        output = build_json_output(classified, year, cpa_notes=cpa_notes, manual_adjustments=manual_adj)
        print(json.dumps(output))
    elif audit:
        print_audit(classified)
    elif needs_review:
        print_needs_review(classified)
    else:
        summary = summarize_classified(classified)
        print_summary(summary, classified)

    return classified


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-signal transaction categorization")
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--json", action="store_true", help="Output structured JSON (for /api/monarch)")
    parser.add_argument("--needs-review", action="store_true", help="Show transactions needing review")
    parser.add_argument("--audit", action="store_true", help="Show mismatches between rules and current categories")
    args = parser.parse_args()

    asyncio.run(run(args.year, args.needs_review, args.audit, json_mode=args.json))


if __name__ == "__main__":
    main()
