#!/usr/bin/env python3
# Last Edited: 2026-03-30 00:30
"""
Keynote Capital QBO Tax Export

Exports Keynote Capital financial data from QuickBooks Online
for Aaron Melamed's personal tax preparation. Read-only — no QBO writes.

CROSS-WORKSPACE DEPENDENCY: This script imports the QuickBooks client from
~/Dropbox/antigravity/workspaces/Keynote/. If that workspace is broken,
restructured, or its QBO client API changes, this script will fail at
import time. It will NOT silently produce wrong data.

Output: tax_document_archive/<year>/keynote_tax_summary_<year>.json
All-or-nothing: any API or validation failure aborts with no output file.

Usage:
    python3 execution/keynote_tax_export.py          # defaults to prior year
    python3 execution/keynote_tax_export.py --year 2025
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set

from dotenv import load_dotenv

# ── Cross-workspace import setup ─────────────────────────────────────────
KEYNOTE_ROOT = Path.home() / "Dropbox/antigravity/workspaces/Keynote"
PERSONAL_ROOT = Path(__file__).resolve().parents[1]

if not KEYNOTE_ROOT.exists():
    raise RuntimeError(
        f"Keynote workspace not found at {KEYNOTE_ROOT}. "
        "This script depends on the Keynote workspace for QBO integration."
    )

# Load Keynote's .env with override=True so QBO_ vars take precedence
# over anything already in the environment from the personal workspace
load_dotenv(KEYNOTE_ROOT / ".env", override=True)

# Remove personal workspace's execution/ from sys.path to prevent its
# utils/ package (which has __init__.py) from shadowing Keynote's utils/
# (namespace package). Without this, `from utils.credential_manager import ...`
# inside quickbooks_client.py resolves to the wrong utils package.
_script_dir = str(Path(__file__).resolve().parent)
if _script_dir in sys.path:
    sys.path.remove(_script_dir)
sys.path.insert(0, str(KEYNOTE_ROOT / "execution"))

from bookkeeping.quickbooks_client import QuickBooksClient  # noqa: E402

# Restore personal execution dir for any future imports
sys.path.append(_script_dir)

# ── Configuration ────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

KC_REALM_ID = "123145929508714"

# Aaron-related accounts (distribution candidates)
AARON_ACCOUNT_IDS: Set[str] = {"49", "51", "64"}
AARON_ACCOUNT_TYPE_MAP = {
    "49": "guaranteed_payment",
    "51": "profit_share",
    "64": "clearing_account",
}
EXPECTED_AARON_ACCOUNTS = {
    "49": "Guaranteed Payments",
    "51": "Partner Distributions - Aaron",
    "64": "Due to Aaron",
}

# KC bank accounts (cash-movement verification)
BANK_ACCOUNT_IDS: Set[str] = {"26", "27", "67"}
EXPECTED_BANK_ACCOUNTS = {
    "26": "Keynote Savings (0931)",
    "27": "Keynote Capital (5374)",
    "67": "AMEX Checking (3207)",
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export Keynote Capital QBO data for tax prep")
    parser.add_argument(
        "--year", type=int,
        default=datetime.now().year - 1,
        help="Tax year to export (default: prior year)",
    )
    return parser.parse_args()


def _paths_for_year(year: int):
    out_dir = PERSONAL_ROOT / "tax_document_archive" / str(year)
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / f"keynote_tax_summary_{year}.json"
    temp = out_dir / f".keynote_tax_summary_{year}.tmp.json"
    return output, temp


# ── P&L Parser ───────────────────────────────────────────────────────────

def _col_value(col_data: list, index: int, default: str = "") -> str:
    if col_data and len(col_data) > index:
        return col_data[index].get("value", default)
    return default


def _col_float(col_data: list, index: int) -> float:
    try:
        return float(_col_value(col_data, index, "0"))
    except (ValueError, TypeError):
        return 0.0


def parse_pnl(report: Dict[str, Any]) -> Dict[str, float]:
    """Extract P&L metrics from QBO report response using group identifiers."""
    result = {
        "income": 0.0,
        "cogs": 0.0,
        "gross_profit": 0.0,
        "operating_expenses": 0.0,
        "net_operating_income": 0.0,
        "other_income": 0.0,
        "other_expenses": 0.0,
        "net_other_income": 0.0,
        "net_income": 0.0,
    }

    # Map QBO group identifiers to our output keys
    group_map = {
        "Income": "income",
        "COGS": "cogs",
        "GrossProfit": "gross_profit",
        "Expenses": "operating_expenses",
        "NetOperatingIncome": "net_operating_income",
        "OtherIncome": "other_income",
        "OtherExpenses": "other_expenses",
        "NetOtherIncome": "net_other_income",
        "NetIncome": "net_income",
    }

    for row in report.get("Rows", {}).get("Row", []):
        group = row.get("group", "")
        key = group_map.get(group)
        if not key:
            continue

        if row.get("type") == "Section":
            summary = row.get("Summary", {})
            result[key] = _col_float(summary.get("ColData", []), 1)
        else:
            result[key] = _col_float(row.get("ColData", []), 1)

    return result


# ── Transaction Serializers ──────────────────────────────────────────────

def serialize_deposit(deposit, acct_lookup: Dict[str, str]) -> Dict[str, Any]:
    lines = []
    if hasattr(deposit, "Line") and deposit.Line:
        for line in deposit.Line:
            ld = {
                "amount": float(line.Amount) if hasattr(line, "Amount") and line.Amount else 0.0,
                "description": getattr(line, "Description", "") or "",
                "posting_type": "Credit",
                "account_id": "",
                "account_name": "",
            }
            detail = getattr(line, "DepositLineDetail", None)
            if detail:
                ref = getattr(detail, "AccountRef", None)
                if ref:
                    ld["account_id"] = str(getattr(ref, "value", ""))
                    ld["account_name"] = (
                        getattr(ref, "name", "") or acct_lookup.get(ld["account_id"], "")
                    )
            lines.append(ld)

    bank_id, bank_name = "", ""
    ref = getattr(deposit, "DepositToAccountRef", None)
    if ref:
        bank_id = str(getattr(ref, "value", ""))
        bank_name = getattr(ref, "name", "") or acct_lookup.get(bank_id, "")

    return {
        "qbo_id": deposit.Id,
        "date": str(deposit.TxnDate) if deposit.TxnDate else "",
        "type": "Deposit",
        "total_amount": float(deposit.TotalAmt) if deposit.TotalAmt else 0.0,
        "memo": getattr(deposit, "PrivateNote", "") or "",
        "bank_account_id": bank_id,
        "bank_account_name": bank_name,
        "lines": lines,
    }


def serialize_purchase(purchase, acct_lookup: Dict[str, str]) -> Dict[str, Any]:
    lines = []
    if hasattr(purchase, "Line") and purchase.Line:
        for line in purchase.Line:
            ld = {
                "amount": float(line.Amount) if hasattr(line, "Amount") and line.Amount else 0.0,
                "description": getattr(line, "Description", "") or "",
                "posting_type": "Debit",
                "account_id": "",
                "account_name": "",
            }
            if getattr(line, "DetailType", "") == "AccountBasedExpenseLineDetail":
                detail = getattr(line, "AccountBasedExpenseLineDetail", None)
                if detail:
                    ref = getattr(detail, "AccountRef", None)
                    if ref:
                        ld["account_id"] = str(getattr(ref, "value", ""))
                        ld["account_name"] = (
                            getattr(ref, "name", "") or acct_lookup.get(ld["account_id"], "")
                        )
            lines.append(ld)

    bank_id, bank_name = "", ""
    ref = getattr(purchase, "AccountRef", None)
    if ref:
        bank_id = str(getattr(ref, "value", ""))
        bank_name = getattr(ref, "name", "") or acct_lookup.get(bank_id, "")

    return {
        "qbo_id": purchase.Id,
        "date": str(purchase.TxnDate) if purchase.TxnDate else "",
        "type": "Purchase",
        "total_amount": float(purchase.TotalAmt) if purchase.TotalAmt else 0.0,
        "memo": getattr(purchase, "PrivateNote", "") or "",
        "bank_account_id": bank_id,
        "bank_account_name": bank_name,
        "lines": lines,
    }


def serialize_journal_entry(je, acct_lookup: Dict[str, str]) -> Dict[str, Any]:
    lines = []
    if hasattr(je, "Line") and je.Line:
        for line in je.Line:
            ld = {
                "amount": float(line.Amount) if hasattr(line, "Amount") and line.Amount else 0.0,
                "description": getattr(line, "Description", "") or "",
                "posting_type": "",
                "account_id": "",
                "account_name": "",
            }
            detail = getattr(line, "JournalEntryLineDetail", None)
            if detail:
                ld["posting_type"] = getattr(detail, "PostingType", "") or ""
                ref = getattr(detail, "AccountRef", None)
                if ref:
                    ld["account_id"] = str(getattr(ref, "value", ""))
                    ld["account_name"] = (
                        getattr(ref, "name", "") or acct_lookup.get(ld["account_id"], "")
                    )
            lines.append(ld)

    return {
        "qbo_id": je.Id,
        "date": str(je.TxnDate) if je.TxnDate else "",
        "type": "JournalEntry",
        "total_amount": float(je.TotalAmt) if je.TotalAmt else 0.0,
        "memo": getattr(je, "PrivateNote", "") or "",
        "bank_account_id": "",
        "bank_account_name": "",
        "lines": lines,
    }


# ── Distribution Extraction ─────────────────────────────────────────────

def extract_aaron_distributions(txns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract all cash payments to Aaron.

    Cash-movement filter: requires BOTH an Aaron-account line AND a bank
    account (transaction-level or line-level) in the same transaction.
    Excludes pure reclassification JEs with no cash movement.
    """
    distributions: List[Dict[str, Any]] = []

    for txn in txns:
        has_bank = txn.get("bank_account_id", "") in BANK_ACCOUNT_IDS
        bank_name = txn.get("bank_account_name", "")

        aaron_lines: List[Dict[str, Any]] = []
        for line in txn.get("lines", []):
            aid = line.get("account_id", "")
            if aid in AARON_ACCOUNT_IDS:
                aaron_lines.append(line)
            if aid in BANK_ACCOUNT_IDS:
                has_bank = True
                if not bank_name:
                    bank_name = line.get("account_name", "")

        if not aaron_lines or not has_bank:
            continue

        for line in aaron_lines:
            aid = line.get("account_id", "")
            distributions.append({
                "date": txn["date"],
                "amount": line["amount"],
                "type": AARON_ACCOUNT_TYPE_MAP.get(aid, "unknown"),
                "account_id": aid,
                "account_name": line.get("account_name", ""),
                "bank_account": bank_name,
                "source_transaction_id": txn["qbo_id"],
                "source_transaction_type": txn["type"],
                "description": line.get("description", ""),
            })

    return sorted(distributions, key=lambda d: d["date"])


# ── Validation ───────────────────────────────────────────────────────────

def validate_export(
    pnl: Dict[str, float],
    distributions: List[Dict[str, Any]],
    summary: Dict[str, Any],
    counts: Dict[str, int],
) -> Dict[str, Any]:
    """Run self-reconciliation checks. Raises on failure — no partial exports."""
    errors: List[str] = []

    # 1. Distribution total check
    computed = round(sum(d["amount"] for d in distributions), 2)
    reported = round(summary["total_to_aaron"], 2)
    dist_ok = abs(computed - reported) < 0.01
    if not dist_ok:
        errors.append(
            f"Distribution total mismatch: sum of rows = {computed}, "
            f"reported total = {reported}"
        )

    # 2. P&L arithmetic check
    expected = round(
        pnl["gross_profit"] - pnl["operating_expenses"] + pnl["net_other_income"], 2
    )
    actual = round(pnl["net_income"], 2)
    pnl_ok = abs(expected - actual) < 0.01
    if not pnl_ok:
        errors.append(
            f"P&L arithmetic: gross_profit({pnl['gross_profit']}) - "
            f"expenses({pnl['operating_expenses']}) + "
            f"net_other({pnl['net_other_income']}) = {expected}, "
            f"but net_income = {actual}"
        )

    result = {
        "distribution_total_matches": dist_ok,
        "pnl_arithmetic_matches": pnl_ok,
        "transaction_counts": counts,
        "errors": errors,
    }

    if errors:
        raise RuntimeError(
            "Export validation failed — no JSON written.\n"
            + "\n".join(f"  - {e}" for e in errors)
        )

    return result


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    args = _parse_args()
    year = args.year
    period_start = f"{year}-01-01"
    period_end = f"{year}-12-31"
    output_file, temp_file = _paths_for_year(year)

    logger.info(f"Starting Keynote Capital {year} tax export...")

    # 1. Connect to Keynote Capital QBO
    qbo = QuickBooksClient(company="kc")

    # 2. Safety assertions — verify we're talking to KC, not HF
    assert qbo.realm_id == KC_REALM_ID, (
        f"Wrong QBO company! Expected realm {KC_REALM_ID} (Keynote Capital), "
        f"got {qbo.realm_id}"
    )
    logger.info(f"Connected to realm {qbo.realm_id} (Keynote Capital)")

    # 3. Verify expected accounts exist
    coa = qbo.get_chart_of_accounts()
    if not coa:
        raise RuntimeError("Failed to fetch chart of accounts from QBO")

    acct_lookup = {a["id"]: a["name"] for a in coa}

    for acct_id, expected in {**EXPECTED_AARON_ACCOUNTS, **EXPECTED_BANK_ACCOUNTS}.items():
        actual = acct_lookup.get(acct_id)
        if actual is None:
            raise RuntimeError(
                f"Expected account ID {acct_id} ({expected}) not found in QBO"
            )
        if actual != expected:
            logger.warning(
                f"Account {acct_id} name mismatch: expected '{expected}', got '{actual}'"
            )
    logger.info("All expected accounts verified")

    # 4. Pull P&L
    logger.info(f"Fetching P&L ({period_start} to {period_end})...")
    pnl_raw = qbo.get_profit_and_loss(period_start, period_end)
    if not pnl_raw:
        raise RuntimeError("Failed to fetch P&L from QBO")
    pnl = parse_pnl(pnl_raw)
    logger.info(f"P&L net income: ${pnl['net_income']:,.2f}")

    # 5. Pull all transactions
    logger.info("Fetching deposits...")
    raw_deposits = qbo.query_all_deposits(period_start, period_end)
    logger.info(f"  {len(raw_deposits)} deposits")

    logger.info("Fetching purchases...")
    raw_purchases = qbo.query_all_purchases(period_start, period_end)
    logger.info(f"  {len(raw_purchases)} purchases")

    logger.info("Fetching journal entries...")
    raw_jes = qbo.query_all_journal_entries(period_start, period_end)
    logger.info(f"  {len(raw_jes)} journal entries")

    # 6. Serialize all transactions (line-aware)
    all_txns: List[Dict[str, Any]] = []
    for d in raw_deposits:
        all_txns.append(serialize_deposit(d, acct_lookup))
    for p in raw_purchases:
        all_txns.append(serialize_purchase(p, acct_lookup))
    for je in raw_jes:
        all_txns.append(serialize_journal_entry(je, acct_lookup))
    all_txns.sort(key=lambda t: t["date"])

    # 7. Extract Aaron's distributions (cash-movement filtered)
    distributions = extract_aaron_distributions(all_txns)
    logger.info(f"Found {len(distributions)} cash distributions to Aaron")

    # 8. Build summary
    gp = round(sum(d["amount"] for d in distributions if d["type"] == "guaranteed_payment"), 2)
    ps = round(sum(d["amount"] for d in distributions if d["type"] == "profit_share"), 2)
    ca = round(sum(d["amount"] for d in distributions if d["type"] == "clearing_account"), 2)
    dist_summary = {
        "guaranteed_payments_total": gp,
        "profit_share_total": ps,
        "clearing_account_total": ca,
        "total_to_aaron": round(gp + ps + ca, 2),
        "payment_count": len(distributions),
    }

    counts = {
        "deposits": len(raw_deposits),
        "purchases": len(raw_purchases),
        "journal_entries": len(raw_jes),
    }

    # 9. Validate (hard stop on failure — no partial exports)
    logger.info("Running validation checks...")
    validation = validate_export(pnl, distributions, dist_summary, counts)
    logger.info("All validation checks passed")

    # 10. Build output
    output = {
        "metadata": {
            "entity": "Keynote Capital, LLC",
            "realm_id": KC_REALM_ID,
            "period": {"start": period_start, "end": period_end},
            "accounting_method": "Cash",
            "generated_at": datetime.now().isoformat(),
        },
        "profit_and_loss": pnl,
        "transactions": all_txns,
        "distributions_to_aaron": distributions,
        "distribution_summary": dist_summary,
        "reconciliation": {
            "note": (
                "Match distributions_to_aaron against Monarch accounts: "
                "Investor Checking, Personal Savings, Marcus Savings"
            ),
            "payments": [
                {"date": d["date"], "amount": d["amount"], "type": d["type"]}
                for d in distributions
            ],
        },
        "validation": validation,
    }

    # 11. Atomic write — temp file then rename
    logger.info(f"Writing output to {output_file}...")
    with open(temp_file, "w") as f:
        json.dump(output, f, indent=2)
    os.replace(str(temp_file), str(output_file))

    logger.info("Export complete.")
    logger.info(f"  P&L net income:    ${pnl['net_income']:,.2f}")
    logger.info(f"  Distributions:     ${dist_summary['total_to_aaron']:,.2f} ({dist_summary['payment_count']} payments)")
    logger.info(f"    GP:              ${gp:,.2f}")
    logger.info(f"    Profit share:    ${ps:,.2f}")
    logger.info(f"    Clearing:        ${ca:,.2f}")
    logger.info(f"  Output:            {output_file}")


if __name__ == "__main__":
    main()
