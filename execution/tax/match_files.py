# Last Edited: 2026-03-29 21:00
"""Match files in tax_document_archive/ to expected documents using pattern-based matching.

Conditional-aware: uses tax_config.yaml to skip disabled specs and show
clear N/A annotations instead of false "missing" reports.

Reference docs are reported separately (informational, not DB-tracked).

Usage:
    python3 -m execution.tax.match_files --year 2024
    python3 -m execution.tax.match_files --year 2025 --dry-run
"""

import argparse
from fnmatch import fnmatch
from pathlib import Path

import yaml

from execution.db.queries import mark_document_received
from execution.tax.models import (
    MatchResult,
    TaxConfig,
    TaxDocumentsMaster,
    TaxYearConfig,
)

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_BASE = WORKSPACE_ROOT / "tax_document_archive"
MASTER_PATH = WORKSPACE_ROOT / "config" / "tax_documents_master.yaml"
CONFIG_PATH = WORKSPACE_ROOT / "config" / "tax_config.yaml"


def load_master() -> TaxDocumentsMaster:
    """Load and validate tax_documents_master.yaml."""
    with open(MASTER_PATH) as f:
        data = yaml.safe_load(f)
    return TaxDocumentsMaster(**data)


def load_config() -> TaxConfig:
    """Load and validate tax_config.yaml."""
    with open(CONFIG_PATH) as f:
        data = yaml.safe_load(f)
    if "tax_years" in data and data["tax_years"]:
        data["tax_years"] = {int(k): v for k, v in data["tax_years"].items()}
    return TaxConfig(**data)


def _matches_pattern(filename: str, pattern: str) -> bool:
    """Case-insensitive glob pattern match."""
    return fnmatch(filename.lower(), pattern.lower())


def _contains_wrong_year(filename: str, target_year: int) -> bool:
    """Check if filename contains a year that doesn't match the target tax year.

    Accepts both the target year and target+1 (institutions generate forms
    in Jan/Feb of the following year, so a 2024 tax form may have 2025 in
    the filename as the generation date).

    Returns True only if a year is found that is NOT the target year or
    target+1. Returns False if no year is found or acceptable years are found.
    """
    import re

    years_found = re.findall(r"20[2-3]\d", filename)
    if not years_found:
        return False
    acceptable = {target_year, target_year + 1}
    return all(int(y) not in acceptable for y in years_found)


def match_archive(
    tax_year: int,
) -> tuple[list[MatchResult], list[str], list[MatchResult], list[tuple[str, str]]]:
    """Match archive files to master checklist entries (conditional-aware).

    Returns:
        (match_results, unmapped_files, reference_results, skipped_conditional)
        - match_results: institutional + self-prepared matches
        - unmapped_files: archive files that didn't match anything
        - reference_results: reference doc matches (informational)
        - skipped_conditional: list of (spec_id, condition) for disabled specs
    """
    master = load_master()
    config = load_config()
    year_config = config.tax_years.get(tax_year, TaxYearConfig())
    archive_dir = ARCHIVE_BASE / str(tax_year)

    if not archive_dir.exists():
        print(f"Archive directory not found: {archive_dir}")
        return [], [], [], []

    archive_files = {
        f.name for f in archive_dir.iterdir() if f.is_file() and not f.name.startswith(".")
    }
    claimed_files: set[str] = set()
    results: list[MatchResult] = []
    skipped_conditional: list[tuple[str, str]] = []

    # ── Institutional specs ────────────────────────────────────────────
    for spec in master.institutional:
        # Check conditional items
        if spec.conditional:
            enabled = year_config.conditional_items.get(spec.id, False)
            if not enabled:
                skipped_conditional.append(
                    (spec.id, spec.condition or "conditional item disabled")
                )
                continue

        doc_name = f"{tax_year} {spec.institution} {spec.form_number}"
        candidates = _find_candidates(
            archive_files, claimed_files, spec.filename_patterns, tax_year
        )

        matched_file = None
        confidence: str = "none"
        if len(candidates) == 1:
            matched_file = candidates[0]
            confidence = "exact"
        elif len(candidates) > 1:
            matched_file = candidates[0]
            confidence = "pattern"

        if matched_file:
            claimed_files.add(matched_file)

        results.append(
            MatchResult(
                doc_id=spec.id,
                doc_name=doc_name,
                matched_file=matched_file,
                confidence=confidence,
            )
        )

    # ── Self-prepared specs ────────────────────────────────────────────
    for spec in master.self_prepared:
        doc_name = f"{tax_year} {spec.name}"
        candidates = _find_candidates(
            archive_files, claimed_files, spec.filename_patterns, tax_year
        )

        matched_file = None
        confidence = "none"
        if len(candidates) == 1:
            matched_file = candidates[0]
            confidence = "exact"
        elif len(candidates) > 1:
            matched_file = candidates[0]
            confidence = "pattern"

        if matched_file:
            claimed_files.add(matched_file)

        results.append(
            MatchResult(
                doc_id=spec.id,
                doc_name=doc_name,
                matched_file=matched_file,
                confidence=confidence,
            )
        )

    # ── Reference docs (informational only) ────────────────────────────
    reference_results: list[MatchResult] = []
    for spec in master.reference:
        doc_name = f"{tax_year} {spec.name}"
        candidates = _find_candidates(
            archive_files, claimed_files, spec.filename_patterns, tax_year
        )

        matched_file = None
        confidence = "none"
        if candidates:
            matched_file = candidates[0]
            confidence = "exact" if len(candidates) == 1 else "pattern"
            claimed_files.add(matched_file)

        reference_results.append(
            MatchResult(
                doc_id=spec.id,
                doc_name=doc_name,
                matched_file=matched_file,
                confidence=confidence,
            )
        )

    unmapped = sorted(archive_files - claimed_files)
    return results, unmapped, reference_results, skipped_conditional


def _find_candidates(
    archive_files: set[str],
    claimed_files: set[str],
    patterns: list[str],
    tax_year: int,
) -> list[str]:
    """Find archive files matching any of the given patterns."""
    candidates: list[str] = []
    for filename in archive_files:
        if filename in claimed_files:
            continue
        if _contains_wrong_year(filename, tax_year):
            continue
        for pattern in patterns:
            if _matches_pattern(filename, pattern):
                candidates.append(filename)
                break
    return candidates


def match_and_mark(tax_year: int) -> tuple[list[str], list[str]]:
    """Match archive files and update DB status. Returns (matched, unmatched) doc names."""
    results, unmapped, reference_results, skipped = match_archive(tax_year)

    matched_names: list[str] = []
    unmatched_names: list[str] = []

    for result in results:
        if result.matched_file:
            relative_path = f"tax_document_archive/{tax_year}/{result.matched_file}"
            db_result = mark_document_received(result.doc_name, file_path=relative_path)
            if db_result:
                matched_names.append(result.doc_name)
                symbol = "✅" if result.confidence == "exact" else "🟡"
                print(f"  {symbol} {result.doc_name} -> {result.matched_file}")
            else:
                unmatched_names.append(result.doc_name)
                print(f"  ❌ {result.doc_name}: DB record not found (file: {result.matched_file})")
        else:
            unmatched_names.append(result.doc_name)
            print(f"  ⬜ {result.doc_name}: no matching file in archive")

    if skipped:
        print(f"\n  Not expected ({len(skipped)}):")
        for spec_id, condition in skipped:
            print(f"  -- {spec_id}: {condition}")

    if reference_results:
        ref_found = [r for r in reference_results if r.matched_file]
        if ref_found:
            print(f"\n  Reference docs found ({len(ref_found)}):")
            for r in ref_found:
                print(f"  📎 {r.doc_name} -> {r.matched_file}")

    if unmapped:
        print(f"\n  ⚠️  Files in archive not mapped to any document:")
        for f in unmapped:
            print(f"    - {f}")

    return matched_names, unmatched_names


def main() -> None:
    parser = argparse.ArgumentParser(description="Match tax archive files to expected documents")
    parser.add_argument("--year", type=int, required=True, help="Tax year")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show matches without updating DB",
    )
    args = parser.parse_args()

    print(f"Matching {args.year} archive files to expected documents...\n")

    if args.dry_run:
        results, unmapped, reference_results, skipped = match_archive(args.year)
        matched = [r for r in results if r.matched_file]
        unmatched = [r for r in results if not r.matched_file]

        if matched:
            print("  MATCHED:")
            for r in matched:
                symbol = "✅" if r.confidence == "exact" else "🟡"
                print(f"    {symbol} {r.doc_name} -> {r.matched_file}")

        if unmatched:
            print(f"\n  MISSING ({len(unmatched)}):")
            for r in unmatched:
                print(f"    ⬜ {r.doc_name}")

        if skipped:
            print(f"\n  NOT EXPECTED ({len(skipped)}):")
            for spec_id, condition in skipped:
                print(f"    -- {spec_id}: {condition}")

        ref_found = [r for r in reference_results if r.matched_file]
        if ref_found:
            print(f"\n  REFERENCE DOCS FOUND ({len(ref_found)}):")
            for r in ref_found:
                print(f"    📎 {r.doc_name} -> {r.matched_file}")

        if unmapped:
            print(f"\n  UNMATCHED ARCHIVE FILES ({len(unmapped)}):")
            for f in unmapped:
                print(f"    - {f}")

        print(f"\nDry run: {len(matched)} matched, {len(unmatched)} missing, "
              f"{len(skipped)} not expected")
    else:
        matched, unmatched = match_and_mark(args.year)
        print(f"\nResults: {len(matched)} matched, {len(unmatched)} unmatched")


if __name__ == "__main__":
    main()
