# Last Edited: 2026-03-29 21:00
"""Standardize filenames in tax_document_archive/{year}/.

Renames tax documents to consistent canonical formats:
    Institutional: {year}_{institution-slug}_{form-type}.pdf
    Self-prepared: {year}_self_{category-slug}.{ext}
    Reference:     {year}_ref_{type-slug}.{ext}

Uses filename_patterns from config/tax_documents_master.yaml to identify
what each file is, then builds the canonical name.

Safety:
  - No match → printed for manual review, not renamed
  - Multiple matches → printed for manual review, not renamed
  - Target path already exists → refused, printed for manual review
  - Dry-run by default (--apply to execute)
  - Rollback manifest written before any renames (--rollback to reverse)

Usage:
    python3 -m execution.tax.rename_docs --year 2025
    python3 -m execution.tax.rename_docs --year 2025 --apply
    python3 -m execution.tax.rename_docs --year 2025 --rollback
"""

import argparse
import json
import re
from pathlib import Path

import yaml

from execution.tax.models import TaxDocumentsMaster, TaxConfig

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
    return TaxConfig(**data)


def _matches_pattern(filename: str, pattern: str) -> bool:
    """Case-insensitive glob pattern match."""
    from fnmatch import fnmatch
    return fnmatch(filename.lower(), pattern.lower())


def _slugify(name: str) -> str:
    """Convert institution name to a URL-safe slug.

    'Goldman Sachs Marcus' → 'goldman-sachs-marcus'
    'Schwab (brokerage)'   → 'schwab'
    'New American Funding' → 'new-american-funding'
    """
    # Strip parenthetical qualifiers like '(brokerage)', '(bank)'
    name = re.sub(r"\s*\(.*?\)\s*", "", name)
    # Lowercase, replace non-alphanumeric runs with hyphens, strip edges
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug


def _form_slug(form_number: str) -> str:
    """Normalize form number for filename.

    '1099-Composite' → '1099-composite'
    'W-2'            → 'w-2'
    '1099-B/DIV'     → '1099-b-div'
    'Gain/Loss Report' → 'gain-loss-report'
    'Year-End Statement' → 'year-end-statement'
    """
    slug = re.sub(r"[^a-z0-9]+", "-", form_number.lower()).strip("-")
    return slug


def _source_extension(filename: str) -> str:
    """Get lowercase extension from source filename."""
    ext = Path(filename).suffix.lower()
    return ext if ext else ".pdf"


# Fallback when source file has no extension
_FORMAT_EXT_MAP = {"pdf": ".pdf", "csv": ".csv", "summary": ".pdf"}


def _ext_for_self_prepared(filename: str, spec_format: str) -> str:
    """Derive file extension for a self-prepared doc.

    Prefers the source file's actual extension. Falls back to the spec's
    format field only if the source has no extension.
    """
    ext = Path(filename).suffix.lower()
    if ext:
        return ext
    return _FORMAT_EXT_MAP.get(spec_format.lower(), ".pdf")


def _extract_account_suffix(filename: str, pattern: str) -> str | None:
    """Extract last 5 digits of account number from filename.

    Uses the spec's account_pattern regex to find the account number,
    then returns the last 5 digits as a disambiguation suffix.
    """
    match = re.search(pattern, filename)
    if match:
        account = match.group(0)
        return account[-5:]
    return None


def _resolve_institution_name(spec_id: str, entity_name: str | None,
                               institution: str, config: TaxConfig,
                               year: int) -> str | None:
    """Get the actual institution name, resolving parameterized entries."""
    # If entity_name is set, use it directly
    if entity_name:
        return entity_name

    # Parameterized — resolve from tax_config.yaml
    year_config = config.tax_years.get(year)
    if not year_config:
        return None

    params = year_config.parameterized_institutions
    if spec_id == "employer_w2" and params.employer_name:
        return params.employer_name
    if spec_id == "employer_1095c":
        # 1095-C employer may differ from W-2 employer (PEO split)
        return params.employer_1095c_name or params.employer_name
    if spec_id == "mortgage_1098" and params.loan_servicer_name:
        return params.loan_servicer_name

    return None


def _contains_wrong_year(filename: str, target_year: int) -> bool:
    """Check if filename contains a year that doesn't match the target.

    Accepts both target year and target+1 (institutions generate forms
    in Jan/Feb of the following year).
    """
    years_found = re.findall(r"20[2-3]\d", filename)
    if not years_found:
        return False
    acceptable = {target_year, target_year + 1}
    return all(int(y) not in acceptable for y in years_found)


def plan_renames(year: int) -> tuple[list[tuple[str, str, str]], list[str], list[str]]:
    """Plan file renames for a given tax year.

    Returns:
        (renames, skipped_multi, skipped_none)
        - renames: list of (original_name, target_name, doc_description)
        - skipped_multi: files that matched multiple specs
        - skipped_none: files that matched no specs
    """
    master = load_master()
    config = load_config()
    archive_dir = ARCHIVE_BASE / str(year)

    if not archive_dir.exists():
        print(f"Archive directory not found: {archive_dir}")
        return [], [], []

    # Get all files (skip hidden files and directories)
    archive_files = sorted(
        f.name for f in archive_dir.iterdir()
        if f.is_file() and not f.name.startswith(".")
    )

    # ── Build spec lookup ──────────────────────────────────────────────
    # Each spec: (target_base, description, patterns, account_pattern_or_None)
    SpecEntry = tuple[str, str, list[str], str | None]
    specs: list[SpecEntry] = []
    # Map target_base → account_pattern for multi-account resolution
    multi_account_patterns: dict[str, str] = {}

    # Institutional docs
    for spec in master.institutional:
        inst_name = _resolve_institution_name(
            spec.id, spec.entity_name, spec.institution, config, year
        )
        if not inst_name:
            continue

        target = f"{year}_{_slugify(inst_name)}_{_form_slug(spec.form_number)}.pdf"
        desc = f"{spec.institution} {spec.form_number}"
        acct = spec.account_pattern if spec.multi_account else None
        specs.append((target, desc, spec.filename_patterns, acct))
        if acct:
            multi_account_patterns[target] = acct

    # Self-prepared docs
    for spec in master.self_prepared:
        # Extension will be resolved per-file in the matching loop
        target = f"{year}_self_{_form_slug(spec.id)}"  # no ext yet
        desc = f"Self-prepared: {spec.name}"
        specs.append((target, desc, spec.filename_patterns, None))

    # Reference docs (rename-only, not DB-tracked)
    for spec in master.reference:
        target = f"{year}_ref_{_form_slug(spec.id)}"  # no ext yet
        desc = f"Reference: {spec.name}"
        specs.append((target, desc, spec.filename_patterns, None))

    # ── Match files to specs ───────────────────────────────────────────
    renames: list[tuple[str, str, str]] = []
    skipped_multi: list[str] = []
    skipped_none: list[str] = []
    already_canonical: list[str] = []
    claimed: set[str] = set()
    target_names: set[str] = set()

    # For multi-account: collect files per spec target base
    multi_account_groups: dict[str, list[tuple[str, str, str]]] = {}

    for filename in archive_files:
        if _contains_wrong_year(filename, year):
            skipped_none.append(filename)
            continue

        matches: list[tuple[str, str, str | None]] = []
        for target, desc, patterns, acct_pattern in specs:
            for pattern in patterns:
                if _matches_pattern(filename, pattern):
                    matches.append((target, desc, acct_pattern))
                    break

        if len(matches) == 0:
            skipped_none.append(filename)
        elif len(matches) > 1:
            skipped_multi.append(filename)
        else:
            target_base, desc, acct_pattern = matches[0]

            # Resolve extension: if target has no extension (self-prepared/reference),
            # derive from source file
            if "." not in target_base.split("_")[-1]:
                ext = _source_extension(filename)
                target_name = f"{target_base}{ext}"
            else:
                target_name = target_base

            if acct_pattern:
                # Multi-account: defer to group resolution
                key = target_base
                if key not in multi_account_groups:
                    multi_account_groups[key] = []
                multi_account_groups[key].append((filename, target_name, desc))
                claimed.add(filename)
            elif filename == target_name:
                already_canonical.append(filename)
                claimed.add(filename)
            elif target_name in target_names:
                skipped_multi.append(filename)
            elif (archive_dir / target_name).exists() and target_name not in claimed:
                skipped_multi.append(filename)
            else:
                renames.append((filename, target_name, desc))
                target_names.add(target_name)
                claimed.add(filename)

    # ── Resolve multi-account groups ───────────────────────────────────
    for target_base, group_files in multi_account_groups.items():
        if len(group_files) == 1:
            # Single file — no suffix needed
            filename, target_name, desc = group_files[0]
            if filename == target_name:
                already_canonical.append(filename)
            elif target_name not in target_names:
                renames.append((filename, target_name, desc))
                target_names.add(target_name)
            else:
                skipped_multi.append(filename)
        else:
            # Multiple files — disambiguate with account suffix
            acct_pattern = multi_account_patterns.get(target_base)

            for filename, target_name, desc in group_files:
                suffix = _extract_account_suffix(filename, acct_pattern) if acct_pattern else None
                if suffix:
                    stem, ext = target_name.rsplit(".", 1)
                    suffixed_target = f"{stem}_{suffix}.{ext}"
                else:
                    suffixed_target = target_name

                if filename == suffixed_target:
                    already_canonical.append(filename)
                elif suffixed_target not in target_names:
                    renames.append((filename, suffixed_target, desc))
                    target_names.add(suffixed_target)
                else:
                    skipped_multi.append(filename)

    if already_canonical:
        print(f"  Already canonical ({len(already_canonical)}):")
        for f in already_canonical:
            print(f"    {f}")

    return renames, skipped_multi, skipped_none


def _write_manifest(archive_dir: Path, renames: list[tuple[str, str, str]]) -> Path:
    """Write a rollback manifest before applying renames."""
    manifest_path = archive_dir / ".rename_manifest.json"
    manifest = {target: original for original, target, _ in renames}
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    return manifest_path


def rollback(year: int) -> None:
    """Reverse renames using the manifest."""
    archive_dir = ARCHIVE_BASE / str(year)
    manifest_path = archive_dir / ".rename_manifest.json"

    if not manifest_path.exists():
        print(f"No rollback manifest found at {manifest_path}")
        return

    with open(manifest_path) as f:
        manifest: dict[str, str] = json.load(f)

    reversed_count = 0
    for target, original in manifest.items():
        target_path = archive_dir / target
        original_path = archive_dir / original
        if target_path.exists() and not original_path.exists():
            target_path.rename(original_path)
            print(f"  {target} -> {original}")
            reversed_count += 1
        elif not target_path.exists():
            print(f"  SKIP {target} (not found)")
        elif original_path.exists():
            print(f"  SKIP {target} -> {original} (original already exists)")

    manifest_path.unlink()
    print(f"\n  {reversed_count} files restored. Manifest deleted.")


def run(year: int, apply: bool = False) -> None:
    """Execute the rename plan."""
    archive_dir = ARCHIVE_BASE / str(year)
    print(f"{'APPLYING' if apply else 'DRY RUN'}: Scanning {archive_dir}/\n")

    renames, skipped_multi, skipped_none = plan_renames(year)

    if renames:
        print(f"  Renames ({len(renames)}):")
        for original, target, desc in renames:
            print(f"    {original}")
            print(f"      -> {target}  [{desc}]")

        if apply:
            manifest_path = _write_manifest(archive_dir, renames)
            print(f"\n  Manifest written: {manifest_path.name}")
            for original, target, _ in renames:
                (archive_dir / original).rename(archive_dir / target)
            print(f"  {len(renames)} files renamed.")
    else:
        print("  No renames needed.")

    if skipped_multi:
        print(f"\n  MANUAL REVIEW — multiple matches ({len(skipped_multi)}):")
        for f in skipped_multi:
            print(f"    ? {f}")

    if skipped_none:
        print(f"\n  UNMATCHED — no spec found ({len(skipped_none)}):")
        for f in skipped_none:
            print(f"    - {f}")

    total = len(renames) + len(skipped_multi) + len(skipped_none)
    print(f"\n  Summary: {len(renames)} rename, {len(skipped_multi)} multi-match, "
          f"{len(skipped_none)} unmatched, {total} total files")

    if not apply and renames:
        print("\n  Run with --apply to execute renames.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Standardize tax document filenames"
    )
    parser.add_argument("--year", type=int, required=True, help="Tax year")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--apply",
        action="store_true",
        help="Actually rename files (default is dry-run)",
    )
    group.add_argument(
        "--rollback",
        action="store_true",
        help="Reverse renames using the manifest",
    )
    args = parser.parse_args()

    if args.rollback:
        rollback(args.year)
    else:
        run(args.year, apply=args.apply)


if __name__ == "__main__":
    main()
