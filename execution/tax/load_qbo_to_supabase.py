#!/usr/bin/env python3
# Last Edited: 2026-03-30 11:00
"""
Load QBO Tax Summary into Supabase for CPA Verify Tab

Reads a JSON export (produced by keynote_tax_export.py) and creates
document records in Supabase with ReconciledField[] metadata that the
/verify page renders automatically.

Creates 3 documents per entity:
  1. P&L Summary       → Schedule E (passthrough income/expenses)
  2. Distributions      → Schedule E (guaranteed payments, profit share)
  3. Interest Income    → Schedule B (bank interest by account)

Cross-validates computed totals against QBO-reported values. Mismatched
fields are marked "disputed" and the script exits nonzero with a warning.

Idempotent: safe to re-run (upserts on document name uniqueness).

Usage:
    python3 -m execution.tax.load_qbo_to_supabase --year 2025
"""

import argparse
import json
import logging
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]

# Accounts that represent bank interest (not K-1 pass-through income)
INTEREST_ACCOUNT_ID = "47"  # "Ordinary Income" in QBO


def load_json(year: int) -> dict:
    """Load the QBO tax summary JSON for the given year."""
    path = WORKSPACE_ROOT / "tax_document_archive" / str(year) / f"keynote_tax_summary_{year}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"QBO export not found at {path}. "
            f"Run: python3 -m execution.keynote_tax_export --year {year}"
        )
    with open(path) as f:
        return json.load(f)


def lookup_entity_id(client: Any, entity_name: str) -> str:
    """Look up an entity's UUID from Supabase. Fails loudly if not found."""
    result = client.table("entities").select("id").eq("name", entity_name).execute()
    if not result.data:
        raise RuntimeError(
            f"Entity '{entity_name}' not found in Supabase. Run seed.py first."
        )
    return result.data[0]["id"]


def make_field(
    label: str,
    value: float | str,
    confidence: str = "verified",
    schedule_line: str | None = None,
    qbo_value: float | str | None = None,
    computed_value: float | str | None = None,
) -> dict:
    """Build a single ReconciledField dict."""
    val = f"{value:.2f}" if isinstance(value, (int, float)) else value
    ocr = f"{qbo_value:.2f}" if isinstance(qbo_value, (int, float)) else qbo_value
    vis = f"{computed_value:.2f}" if isinstance(computed_value, (int, float)) else computed_value
    return {
        "label": label,
        "value": val,
        "confidence": confidence,
        "ocr_value": ocr,
        "vision_value": vis,
        "schedule_line": schedule_line,
    }


def check_match(qbo_val: float, computed_val: float, label: str, warnings: list[str]) -> str:
    """Compare QBO-reported vs computed value. Returns confidence and appends warnings."""
    if abs(qbo_val - computed_val) < 0.01:
        return "verified"
    warnings.append(
        f"  MISMATCH: {label}: QBO reports ${qbo_val:,.2f}, "
        f"computed ${computed_val:,.2f} (diff ${abs(qbo_val - computed_val):,.2f})"
    )
    return "disputed"


# ── Aggregation helpers ─────────────────────────────────────────────────


def aggregate_expenses(transactions: list[dict]) -> dict[str, float]:
    """Sum expenses by account_name from transaction line items.

    Includes all expense accounts (Bank Charges, Legal, Taxes, Guaranteed
    Payments). Credits reduce the total (e.g. FTB refund).
    Skips income, distribution, and investment accounts.
    """
    # Accounts that are NOT expenses — skip these
    NON_EXPENSE_ACCOUNTS = {
        "Ordinary Income", "Services", "Profit Distribution from HF",
        "Homeowners First:Ordinary Income",
        "Investment in Homeowners First",
        "Homeowners First:Non deductible expenses (K-1)",
    }
    totals: dict[str, float] = defaultdict(float)
    for txn in transactions:
        for line in txn.get("lines", []):
            acct = line["account_name"]
            if "Partner Distributions" in acct or "Due to" in acct:
                continue
            if acct in NON_EXPENSE_ACCOUNTS:
                continue
            if line["posting_type"] == "Debit":
                totals[acct] += line["amount"]
            elif line["posting_type"] == "Credit":
                totals[acct] -= line["amount"]
    return dict(totals)


def aggregate_interest_by_bank(transactions: list[dict]) -> dict[str, float]:
    """Sum bank interest income by bank account name.

    Only Deposit-type transactions to account_id 47 (Ordinary Income).
    Excludes JournalEntries (K-1 reclassifications).
    """
    totals: dict[str, float] = defaultdict(float)
    for txn in transactions:
        if txn["type"] != "Deposit":
            continue
        for line in txn.get("lines", []):
            if line["account_id"] == INTEREST_ACCOUNT_ID:
                totals[txn["bank_account_name"]] += line["amount"]
    return dict(totals)


# ── Document builders ───────────────────────────────────────────────────


def build_pnl_document(
    data: dict, year: int, entity_name: str, entity_id: str, owner_id: str, warnings: list[str]
) -> dict:
    """Build the P&L Summary document payload.

    P&L totals come from QBO's own report (already validated by the export
    script: pnl_arithmetic_matches). Expense breakdown is derived from
    transaction line items for CPA detail.
    """
    pnl = data["profit_and_loss"]
    validation = data.get("validation", {})
    pnl_valid = validation.get("pnl_arithmetic_matches", False)

    # QBO's own arithmetic check determines confidence on totals
    total_confidence = "verified" if pnl_valid else "disputed"
    if not pnl_valid:
        warnings.append("  MISMATCH: QBO P&L arithmetic check failed (pnl_arithmetic_matches: false)")

    # Aggregate expenses from transactions for supplementary breakdown
    expense_breakdown = aggregate_expenses(data["transactions"])

    fields = []

    # Income lines — from QBO P&L report
    fields.append(make_field(
        "Ordinary Income (Services)", pnl["income"],
        confidence=total_confidence,
        schedule_line="K-1 Line 1",
    ))
    fields.append(make_field(
        "Other Income (HF K-1)", pnl["other_income"],
        confidence=total_confidence,
        schedule_line="K-1 Line 1",
    ))

    # Expense breakdown from transaction aggregation (supplementary detail)
    for acct_name, amount in sorted(expense_breakdown.items()):
        if abs(amount) < 0.01:
            continue
        fields.append(make_field(
            acct_name, amount,
            confidence="single_source",
            schedule_line="K-1 Expenses",
        ))

    # P&L totals — from QBO report directly
    fields.append(make_field(
        "Operating Expenses Total", pnl["operating_expenses"],
        confidence=total_confidence,
        schedule_line="K-1 Expenses",
    ))
    fields.append(make_field(
        "Other Expenses", pnl["other_expenses"],
        confidence=total_confidence,
        schedule_line="K-1 Expenses",
    ))
    fields.append(make_field(
        "Net Operating Income", pnl["net_operating_income"],
        confidence=total_confidence,
        schedule_line="K-1 Line 1",
    ))
    fields.append(make_field(
        "Net Other Income", pnl["net_other_income"],
        confidence=total_confidence,
        schedule_line="K-1 Line 1",
    ))
    fields.append(make_field(
        "Net Income", pnl["net_income"],
        confidence=total_confidence,
        schedule_line="K-1 Line 1",
    ))

    return {
        "name": f"{year} Keynote Capital P&L Summary",
        "type": "financial",
        "source_entity_id": entity_id,
        "owner_entity_id": owner_id,
        "tax_year": year,
        "tax_schedule": "Schedule E",
        "form_number": "QBO P&L",
        "status": "extracted",
        "file_path": str(
            WORKSPACE_ROOT / "tax_document_archive" / str(year)
            / f"keynote_tax_summary_{year}.json"
        ),
        "metadata": {
            "source": "quickbooks_online",
            "realm_id": data["metadata"]["realm_id"],
            "accounting_method": data["metadata"]["accounting_method"],
            "extracted": {
                "fields": fields,
                "extracted_at": datetime.now().isoformat(),
            },
        },
    }


def build_distributions_document(
    data: dict, year: int, entity_id: str, owner_id: str, warnings: list[str]
) -> dict:
    """Build the Distributions to Aaron document payload."""
    summary = data["distribution_summary"]
    distributions = data["distributions_to_aaron"]

    # Cross-check: sum individual distributions by type vs reported totals
    computed_gp = sum(d["amount"] for d in distributions if d["type"] == "guaranteed_payment")
    computed_ps = sum(d["amount"] for d in distributions if d["type"] == "profit_share")
    computed_ca = sum(d["amount"] for d in distributions if d["type"] == "clearing_account")
    computed_total = sum(d["amount"] for d in distributions)

    gp_conf = check_match(summary["guaranteed_payments_total"], computed_gp, "Guaranteed Payments", warnings)
    ps_conf = check_match(summary["profit_share_total"], computed_ps, "Profit Share", warnings)
    ca_conf = check_match(summary["clearing_account_total"], computed_ca, "Clearing Account", warnings)
    total_conf = check_match(summary["total_to_aaron"], computed_total, "Total Distributions", warnings)

    fields = [
        make_field(
            "Guaranteed Payments Total", summary["guaranteed_payments_total"],
            confidence=gp_conf,
            schedule_line="K-1 Line 4",
            qbo_value=summary["guaranteed_payments_total"],
            computed_value=computed_gp,
        ),
        make_field(
            "Profit Share Distributions", summary["profit_share_total"],
            confidence=ps_conf,
            schedule_line="K-1 Line 1 (draw)",
            qbo_value=summary["profit_share_total"],
            computed_value=computed_ps,
        ),
        make_field(
            "Clearing Account (Due to Aaron)", summary["clearing_account_total"],
            confidence=ca_conf,
            schedule_line="Non-taxable",
            qbo_value=summary["clearing_account_total"],
            computed_value=computed_ca,
        ),
        make_field(
            "Total Distributions to Aaron", summary["total_to_aaron"],
            confidence=total_conf,
            schedule_line="K-1 reconciliation",
            qbo_value=summary["total_to_aaron"],
            computed_value=computed_total,
        ),
        make_field(
            "Payment Count", summary["payment_count"],
            schedule_line=None,
        ),
    ]

    # Add individual distribution line items for detail
    for d in distributions:
        fields.append(make_field(
            f"{d['date']} — {d['type'].replace('_', ' ').title()}",
            d["amount"],
            confidence="single_source",
            schedule_line=d["account_name"],
        ))

    return {
        "name": f"{year} Keynote Capital Distributions",
        "type": "financial",
        "source_entity_id": entity_id,
        "owner_entity_id": owner_id,
        "tax_year": year,
        "tax_schedule": "Schedule E",
        "form_number": "Distribution Summary",
        "status": "extracted",
        "file_path": str(
            WORKSPACE_ROOT / "tax_document_archive" / str(year)
            / f"keynote_tax_summary_{year}.json"
        ),
        "metadata": {
            "source": "quickbooks_online",
            "extracted": {
                "fields": fields,
                "extracted_at": datetime.now().isoformat(),
            },
        },
    }


def build_interest_document(
    data: dict, year: int, entity_id: str, owner_id: str, warnings: list[str]
) -> dict:
    """Build the Interest Income document payload."""
    interest_by_bank = aggregate_interest_by_bank(data["transactions"])
    total_interest = sum(interest_by_bank.values())

    fields = []
    for bank_name, amount in sorted(interest_by_bank.items()):
        if abs(amount) < 0.01:
            continue
        fields.append(make_field(
            f"{bank_name} Interest", amount,
            confidence="single_source",
            schedule_line="Schedule B, Part I",
        ))

    fields.append(make_field(
        "Total Bank Interest Income", total_interest,
        confidence="single_source",
        schedule_line="Schedule B, Part I",
    ))

    return {
        "name": f"{year} Keynote Capital Interest",
        "type": "financial",
        "source_entity_id": entity_id,
        "owner_entity_id": owner_id,
        "tax_year": year,
        "tax_schedule": "Schedule B",
        "form_number": "QBO Interest",
        "status": "extracted",
        "file_path": str(
            WORKSPACE_ROOT / "tax_document_archive" / str(year)
            / f"keynote_tax_summary_{year}.json"
        ),
        "metadata": {
            "source": "quickbooks_online",
            "extracted": {
                "fields": fields,
                "extracted_at": datetime.now().isoformat(),
            },
        },
    }


# ── Main ────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Load QBO tax summary into Supabase")
    parser.add_argument("--year", type=int, default=datetime.now().year - 1,
                        help="Tax year (default: prior year)")
    args = parser.parse_args()
    year = args.year

    # Import here so module-level doesn't require Supabase credentials
    from execution.db.client import get_client
    from execution.db.queries import upsert_document, mark_document_extracted

    logger.info(f"Loading Keynote Capital QBO data for {year}")

    data = load_json(year)
    entity_name = data["metadata"]["entity"]
    logger.info(f"Entity: {entity_name}, period: {data['metadata']['period']['start']} to {data['metadata']['period']['end']}")

    client = get_client()
    entity_id = lookup_entity_id(client, entity_name)
    owner_id = lookup_entity_id(client, "Aaron Melamed")

    warnings: list[str] = []

    # Build all three documents
    docs = [
        build_pnl_document(data, year, entity_name, entity_id, owner_id, warnings),
        build_distributions_document(data, year, entity_id, owner_id, warnings),
        build_interest_document(data, year, entity_id, owner_id, warnings),
    ]

    # Upsert each document, then store extracted fields
    for doc in docs:
        extracted = doc["metadata"].pop("extracted")
        upsert_result = upsert_document(doc)
        if not upsert_result:
            logger.error(f"Failed to upsert document: {doc['name']}")
            return 1
        mark_result = mark_document_extracted(doc["name"], extracted)
        if not mark_result:
            logger.error(f"Failed to mark extracted: {doc['name']}")
            return 1

        field_count = len(extracted["fields"])
        logger.info(f"  ✓ {doc['name']} — {field_count} fields, schedule: {doc['tax_schedule']}")

    # Summary
    print(f"\n{'='*60}")
    print(f"Loaded {len(docs)} documents for {year} {entity_name}")
    for doc in docs:
        print(f"  • {doc['name']} → {doc['tax_schedule']}")

    if warnings:
        print(f"\n⚠ {len(warnings)} VALIDATION WARNING(S):")
        for w in warnings:
            print(w)
        print(f"\nAffected fields marked 'disputed' on /verify.")
        return 1

    print(f"\n✓ All cross-checks passed. View at /verify.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
