# Last Edited: 2026-03-29 23:00
"""Deduction hunter — learns from verified months, hunts in unverified months.

Scans personal transactions for missed deductions using patterns learned from
a manually-categorized training window. Outputs candidate batches grouped by
deduction type for interactive review.

Usage:
    python3 -m execution.finance.hunt_deductions --year 2025 --train
    python3 -m execution.finance.hunt_deductions --year 2025 --hunt
    python3 -m execution.finance.hunt_deductions --year 2025  # both
"""

import argparse
import asyncio
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from execution.finance.categorize import (
    build_category_to_schedule,
    load_schedule_rules,
    pull_transactions,
    classify_transaction,
    load_monarch_rules,
    build_merchant_history,
    load_plausibility_config,
)

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
PATTERNS_PATH = WORKSPACE_ROOT / "config" / "deduction_patterns.yaml"
SCHEDULE_RULES_PATH = WORKSPACE_ROOT / "config" / "categorization_rules.yaml"

# Merchants Monarch normalizes to a generic name, losing real vendor identity.
# Use plaid_name for these instead.
GARBLED_MERCHANTS = {"ciudad de mexico"}

# Training window — manually categorized period
DEFAULT_TRAINING_WINDOWS = {
    2025: {"start": "2025-11-01", "end": "2026-03-31"},
}


def load_patterns() -> dict:
    """Load learned deduction patterns from YAML."""
    if PATTERNS_PATH.exists():
        with open(PATTERNS_PATH) as f:
            return yaml.safe_load(f) or {}
    return {"training_windows": [], "patterns": []}


def save_patterns(data: dict) -> None:
    """Save deduction patterns to YAML."""
    with open(PATTERNS_PATH, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=120)
    print(f"  Patterns saved to {PATTERNS_PATH}")


def _in_training_window(txn_date: str, window: dict) -> bool:
    """Check if a transaction date falls within the training window."""
    return window["start"] <= txn_date <= window["end"]


def _in_hunt_window(txn_date: str, window: dict) -> bool:
    """Check if a transaction date is OUTSIDE the training window (hunt target)."""
    return txn_date < window["start"]


async def train(year: int) -> dict:
    """Learn deduction patterns from the verified training window.

    Returns the patterns dict (also saves to disk).
    """
    window = DEFAULT_TRAINING_WINDOWS.get(year)
    if not window:
        print(f"No training window configured for {year}")
        return load_patterns()

    print(f"Training from verified window: {window['start']} to {window['end']}")

    # Pull and classify all transactions
    sched_rules = load_schedule_rules()
    cat_to_schedule = build_category_to_schedule(sched_rules)
    monarch_rules = load_monarch_rules()
    plausibility = load_plausibility_config(sched_rules)

    print("Pulling transactions...")
    txns = await pull_transactions(year)
    merchant_history = build_merchant_history(txns)

    classified = [
        classify_transaction(txn, cat_to_schedule, monarch_rules, merchant_history, plausibility)
        for txn in txns
    ]

    # Filter to training window only
    training_txns = [c for c in classified if _in_training_window(c["date"], window)]
    print(f"  {len(training_txns)} transactions in training window")

    # Build merchant → category profiles
    # Deductible: anything NOT in 'personal' or 'unmapped' schedule
    # Personal: anything in 'personal' schedule
    merchant_profiles: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "deductible_categories": Counter(),
        "personal_categories": Counter(),
        "amounts": [],
        "accounts": set(),
    })

    for c in training_txns:
        merchant = c["merchant"].lower().strip()
        # Use plaid_name for garbled merchants to get real vendor identity
        if merchant in GARBLED_MERCHANTS:
            merchant = c.get("plaid_name", merchant).lower().strip()
        if not merchant or merchant == "unknown":
            continue

        profile = merchant_profiles[merchant]
        if c["schedule"] == "personal":
            profile["personal_categories"][c["category"]] += 1
        elif c["schedule"] != "unmapped":
            profile["deductible_categories"][c["category"]] += 1
            profile["amounts"].append(c["amount"])
            profile["accounts"].add(c["account"])

    # Build patterns from profiles
    patterns_data = load_patterns()
    existing_merchants = {p.get("merchant_contains", "").lower() for p in patterns_data.get("patterns", [])}

    new_patterns = []
    negative_patterns = []

    for merchant, profile in sorted(merchant_profiles.items()):
        if merchant in existing_merchants:
            continue  # Already have a pattern for this merchant

        deductible = profile["deductible_categories"]
        personal = profile["personal_categories"]

        if deductible and not personal:
            # Consistently deductible
            top_cat = deductible.most_common(1)[0][0]
            schedule = cat_to_schedule.get(top_cat, "unknown")
            new_patterns.append({
                "merchant_contains": merchant,
                "target_category": top_cat,
                "target_schedule": schedule,
                "confidence": "high" if sum(deductible.values()) >= 2 else "medium",
                "source": f"training_{year}",
                "occurrences": sum(deductible.values()),
                "avg_amount": round(sum(profile["amounts"]) / len(profile["amounts"]), 2) if profile["amounts"] else 0,
            })
        elif personal and not deductible:
            # Consistently personal — negative pattern
            top_cat = personal.most_common(1)[0][0]
            if sum(personal.values()) >= 2:  # Only save if seen multiple times
                negative_patterns.append({
                    "merchant_contains": merchant,
                    "target_category": None,
                    "confidence": "high",
                    "source": f"training_{year}",
                    "note": f"Personal: {top_cat}",
                })
        elif deductible and personal:
            # Mixed — flag as ambiguous
            top_deductible = deductible.most_common(1)[0][0]
            new_patterns.append({
                "merchant_contains": merchant,
                "target_category": top_deductible,
                "target_schedule": cat_to_schedule.get(top_deductible, "unknown"),
                "confidence": "low",
                "source": f"training_{year}",
                "note": f"Ambiguous: also appears as personal ({personal.most_common(1)[0][0]})",
                "occurrences": sum(deductible.values()),
            })

    # Update patterns file
    if "patterns" not in patterns_data:
        patterns_data["patterns"] = []
    if "training_windows" not in patterns_data:
        patterns_data["training_windows"] = []

    # Add training window if not already recorded
    if not any(w.get("start") == window["start"] for w in patterns_data["training_windows"]):
        patterns_data["training_windows"].append({
            "start": window["start"],
            "end": window["end"],
            "year": year,
        })

    patterns_data["patterns"].extend(new_patterns)
    patterns_data["patterns"].extend(negative_patterns)
    save_patterns(patterns_data)

    # Report
    print(f"\n  Learned {len(new_patterns)} deductible patterns, {len(negative_patterns)} negative patterns")
    if new_patterns:
        print(f"\n  Deductible patterns:")
        for p in sorted(new_patterns, key=lambda x: x.get("target_schedule", "")):
            cat = p["target_category"]
            n = p.get("occurrences", "?")
            print(f"    {p['merchant_contains']:30s} → {cat:30s} ({n} occurrences)")

    return patterns_data


async def hunt(year: int) -> list[dict]:
    """Hunt for missed deductions in unverified months using learned patterns.

    Returns list of candidate batches.
    """
    window = DEFAULT_TRAINING_WINDOWS.get(year)
    if not window:
        print(f"No training window configured for {year}")
        return []

    patterns_data = load_patterns()
    patterns = patterns_data.get("patterns", [])
    if not patterns:
        print("No patterns loaded. Run --train first.")
        return []

    # Build lookups
    deductible_patterns = [p for p in patterns if p.get("target_category")]
    negative_merchants = {p["merchant_contains"].lower() for p in patterns if not p.get("target_category")}

    print(f"Hunting with {len(deductible_patterns)} deductible patterns, {len(negative_merchants)} negatives")

    # Pull and classify
    sched_rules = load_schedule_rules()
    cat_to_schedule = build_category_to_schedule(sched_rules)
    monarch_rules = load_monarch_rules()
    plausibility = load_plausibility_config(sched_rules)

    print("Pulling transactions...")
    txns = await pull_transactions(year)
    merchant_history = build_merchant_history(txns)

    classified = [
        classify_transaction(txn, cat_to_schedule, monarch_rules, merchant_history, plausibility)
        for txn in txns
    ]

    # Filter to hunt window (unverified months only)
    hunt_txns = [c for c in classified if _in_hunt_window(c["date"], window)]
    personal_txns = [c for c in hunt_txns if c["schedule"] == "personal"]
    print(f"  {len(hunt_txns)} transactions in hunt window, {len(personal_txns)} personal")

    # Also find miscategorized deductions (on a schedule but wrong category)
    deductible_txns = [c for c in hunt_txns if c["schedule"] not in ("personal", "unmapped")]

    # Match personal transactions against deductible patterns
    candidates: dict[str, list[dict]] = defaultdict(list)

    for txn in personal_txns:
        merchant_lower = txn["merchant"].lower().strip()
        # Use plaid_name for garbled merchants
        if merchant_lower in GARBLED_MERCHANTS:
            merchant_lower = txn.get("plaid_name", merchant_lower).lower().strip()

        # Skip if merchant is a known negative
        if any(neg in merchant_lower for neg in negative_merchants):
            continue

        for pattern in deductible_patterns:
            pattern_merchant = pattern["merchant_contains"].lower()
            if pattern_merchant in merchant_lower:
                candidates[pattern["target_category"]].append({
                    "txn": txn,
                    "pattern": pattern,
                    "reason": "merchant_match",
                })
                break

    # Check for miscategorized deductions (right schedule, wrong category)
    for txn in deductible_txns:
        merchant_lower = txn["merchant"].lower().strip()
        if merchant_lower in GARBLED_MERCHANTS:
            merchant_lower = txn.get("plaid_name", merchant_lower).lower().strip()
        for pattern in deductible_patterns:
            pattern_merchant = pattern["merchant_contains"].lower()
            if pattern_merchant in merchant_lower:
                if txn["category"] != pattern["target_category"]:
                    candidates[pattern["target_category"]].append({
                        "txn": txn,
                        "pattern": pattern,
                        "reason": "wrong_category",
                        "current_category": txn["category"],
                    })
                break

    # Build batches grouped by target category
    batches = []
    for target_cat, items in sorted(candidates.items()):
        schedule = items[0]["pattern"].get("target_schedule", "unknown") if items else "unknown"
        batches.append({
            "target_category": target_cat,
            "target_schedule": schedule,
            "count": len(items),
            "total": round(sum(i["txn"]["amount"] for i in items), 2),
            "items": items,
        })

    return batches


def print_batches(batches: list[dict]) -> None:
    """Print hunt results as numbered batches for review."""
    if not batches:
        print("\nNo missed deductions found.")
        return

    total_found = sum(b["count"] for b in batches)
    total_amount = sum(b["total"] for b in batches)
    print(f"\n{'='*60}")
    print(f"  DEDUCTION HUNT RESULTS: {total_found} candidates, ${total_amount:,.2f}")
    print(f"{'='*60}")

    for i, batch in enumerate(batches, 1):
        print(f"\n  BATCH {i}: {batch['target_category']} ({batch['target_schedule']})")
        print(f"  {batch['count']} transactions, ${batch['total']:,.2f}")
        print(f"  {'─'*56}")

        for item in sorted(batch["items"], key=lambda x: x["txn"]["date"]):
            txn = item["txn"]
            reason = item.get("reason", "")
            current = item.get("current_category", txn["category"])
            flag = f" [currently: {current}]" if reason == "wrong_category" else f" [personal: {current}]"
            print(f"    {txn['date']}  {txn['merchant']:30s}  ${txn['amount']:>10,.2f}{flag}")
            print(f"      id={txn['id']}  {txn['account']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Hunt for missed deductions")
    parser.add_argument("--year", type=int, required=True, help="Tax year")
    parser.add_argument("--train", action="store_true", help="Learn patterns from verified window")
    parser.add_argument("--hunt", action="store_true", help="Hunt using learned patterns")
    parser.add_argument("--json", action="store_true", help="Output batches as JSON")
    args = parser.parse_args()

    # Default: both train and hunt
    if not args.train and not args.hunt:
        args.train = True
        args.hunt = True

    async def run():
        if args.train:
            await train(args.year)
        if args.hunt:
            batches = await hunt(args.year)
            if args.json:
                # Serialize for programmatic use
                output = []
                for b in batches:
                    output.append({
                        "target_category": b["target_category"],
                        "target_schedule": b["target_schedule"],
                        "count": b["count"],
                        "total": b["total"],
                        "transactions": [
                            {
                                "id": i["txn"]["id"],
                                "date": i["txn"]["date"],
                                "merchant": i["txn"]["merchant"],
                                "amount": i["txn"]["amount"],
                                "current_category": i.get("current_category", i["txn"]["category"]),
                                "reason": i.get("reason", ""),
                            }
                            for i in b["items"]
                        ],
                    })
                print(json.dumps(output, indent=2))
            else:
                print_batches(batches)

    asyncio.run(run())


if __name__ == "__main__":
    main()
