# Last Edited: 2026-03-26 12:00
"""CLI tool to print tax document status for a given year."""

import argparse

from execution.db.queries import (
    get_missing_documents,
    get_document_status_summary,
    get_cpa_package,
)


def print_checklist(tax_year: int) -> None:
    """Print a full tax document status report."""
    print(f"\n{'='*60}")
    print(f"  TAX DOCUMENT STATUS — {tax_year}")
    print(f"{'='*60}\n")

    # Summary
    summary = get_document_status_summary(tax_year)
    total = sum(summary.values())
    print(f"Total documents: {total}")
    for status, count in sorted(summary.items()):
        symbol = {"expected": "⬜", "received": "✅", "submitted": "📤", "verified": "✔️"}.get(status, "?")
        print(f"  {symbol} {status}: {count}")

    # Missing documents
    missing = get_missing_documents(tax_year)
    print(f"\n{'—'*60}")
    print(f"MISSING ({len(missing)} documents still expected):")
    print(f"{'—'*60}")
    if not missing:
        print("  🎉 All documents received!")
    else:
        current_schedule = None
        for doc in missing:
            schedule = doc["tax_schedule"] or "Other"
            if schedule != current_schedule:
                current_schedule = schedule
                print(f"\n  [{schedule}]")
            conditional = ""
            if doc.get("metadata", {}).get("conditional"):
                conditional = f" ⚠️  ({doc['metadata']['condition']})"
            print(f"    ⬜ {doc['name']} ({doc['form_number']}){conditional}")

    # CPA package (if any docs received)
    package = get_cpa_package(tax_year)
    if package:
        print(f"\n{'—'*60}")
        print("CPA PACKAGE (received/submitted, grouped by schedule):")
        print(f"{'—'*60}")
        for schedule, doc_names in sorted(package.items()):
            print(f"\n  [{schedule}]")
            for name in doc_names:
                print(f"    ✅ {name}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Tax document checklist")
    parser.add_argument("year", type=int, nargs="?", default=2024, help="Tax year (default: 2024)")
    args = parser.parse_args()
    print_checklist(args.year)


if __name__ == "__main__":
    main()
