# Last Edited: 2026-03-29 21:00
"""Thin classifier that identifies tax documents via OCR text.

Runs deterministic regex rules against OCR output to extract institution,
form type, tax year, and account number. No LLM calls — pure pattern
matching for speed and reproducibility.

Usage:
    python3 -m execution.tax.identify_pdf --file path/to/doc.pdf
    python3 -m execution.tax.identify_pdf --dir taxes/2024/archive/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from execution.tax.models import IdentificationResult

# Graceful import: Google Cloud dependency may not be installed in test
# environments. The classify path (_classify_text) works without it.
try:
    from execution.tax.extract_pdf import extract_ocr_text
except ImportError:
    extract_ocr_text = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Institution patterns — order matters: more specific patterns first
# ---------------------------------------------------------------------------

_INSTITUTION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"Goldman\s*Sachs|Marcus", re.IGNORECASE), "Goldman Sachs Marcus"),
    (re.compile(r"New\s*American\s*Funding", re.IGNORECASE), "New American Funding"),
    (re.compile(r"American\s*Express|AMEX", re.IGNORECASE), "American Express"),
    (re.compile(r"Schwab", re.IGNORECASE), "Schwab"),
    (re.compile(r"Betterment", re.IGNORECASE), "Betterment"),
    (re.compile(r"Coinbase", re.IGNORECASE), "Coinbase"),
    (re.compile(r"ProPay", re.IGNORECASE), "ProPay"),
    (re.compile(r"Guideline", re.IGNORECASE), "Guideline"),
    (re.compile(r"JustWorks", re.IGNORECASE), "JustWorks"),
]

# ---------------------------------------------------------------------------
# Form type patterns — ordered from most specific to generic fallback
# ---------------------------------------------------------------------------

_FORM_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    # Composite must precede the generic 1099 catch-all
    (re.compile(r"1099[- ]?Composite|Composite\b.*?Year[- ]?End", re.IGNORECASE), "1099-Composite"),
    (re.compile(r"1099[- ]?MISC|Form\s*1099[- ]?MISC", re.IGNORECASE), "1099-MISC"),
    (re.compile(r"1099[- ]?INT|Form\s*1099[- ]?INT|1099INT", re.IGNORECASE), "1099-INT"),
    (re.compile(r"1099[- ]?B/DIV|1099[- ]?DIV|1099[- ]?B", re.IGNORECASE), "1099-B/DIV"),
    (re.compile(r"1099[- ]?K", re.IGNORECASE), "1099-K"),
    (re.compile(r"1099[- ]?R", re.IGNORECASE), "1099-R"),
    # IRA FMV / Form 5498 — year-end value + RMD statement
    (re.compile(r"Fair\s+Market\s+Value|FMV|Form\s*5498|Required\s+Minimum\s+Distribution", re.IGNORECASE), "5498-FMV"),
    # Supplemental tax info (supplements 1099-B/DIV)
    (re.compile(r"[Ss]upplemental\s+[Tt]ax", re.IGNORECASE), "1099-Supplemental"),
    (re.compile(r"1095[- ]?C", re.IGNORECASE), "1095-C"),
    (re.compile(r"1098\b", re.IGNORECASE), "1098"),
    (re.compile(r"W[- ]?2\b|W2\b", re.IGNORECASE), "W-2"),
    # 401k / retirement statements
    (re.compile(r"401\s*\(?k\)?|retirement\s+(?:plan|account)\s+statement", re.IGNORECASE), "401k-Statement"),
    # Gain/loss reports (supports Form 8949)
    (re.compile(r"[Gg]ain.{0,5}[Ll]oss|[Tt]ransaction\s+[Hh]istory", re.IGNORECASE), "Gain/Loss Report"),
    # Generic 1099 — only if no specific variant matched above
    (re.compile(r"1099\b", re.IGNORECASE), "1099"),
]

# ---------------------------------------------------------------------------
# Tax year patterns
# ---------------------------------------------------------------------------

_YEAR_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"Tax\s+Year\s+(20\d{2})", re.IGNORECASE),
    re.compile(r"for\s+(?:the\s+)?(?:tax\s+)?year\s+(20\d{2})", re.IGNORECASE),
    # "for 2024" near a form identifier (within ~60 chars)
    re.compile(r"(?:1099|1098|W-?2|1095|Form)\b.{0,60}\bfor\s+(20\d{2})", re.IGNORECASE),
    re.compile(r"\bfor\s+(20\d{2})\b.{0,60}(?:1099|1098|W-?2|1095|Form)", re.IGNORECASE),
    # Standalone "for YYYY" as lower-priority fallback
    re.compile(r"\bfor\s+(20\d{2})\b", re.IGNORECASE),
]

# Account number: 10-15 digit sequences (skip obvious non-account numbers
# like zip codes or phone numbers by requiring >= 10 digits)
_ACCOUNT_PATTERN = re.compile(r"\b(\d{10,15})\b")


# ---------------------------------------------------------------------------
# Core classification
# ---------------------------------------------------------------------------


def _classify_text(text: str) -> IdentificationResult:
    """Deterministic regex classification of raw OCR text.

    Searches for institution, form type, tax year, and account number
    using ordered pattern lists. Confidence is based on how many of the
    three primary signals (institution, form_type, tax_year) were found.
    """
    institution: str | None = None
    form_type: str | None = None
    tax_year: int | None = None
    account_number: str | None = None

    # --- Institution ---
    for pattern, name in _INSTITUTION_PATTERNS:
        if pattern.search(text):
            institution = name
            break

    # --- Form type ---
    for pattern, form_name in _FORM_PATTERNS:
        if pattern.search(text):
            form_type = form_name
            break

    # --- Tax year ---
    for pattern in _YEAR_PATTERNS:
        m = pattern.search(text)
        if m:
            tax_year = int(m.group(1))
            break

    # --- Account number ---
    m = _ACCOUNT_PATTERN.search(text)
    if m:
        account_number = m.group(1)

    # --- Confidence ---
    signals_found = sum(1 for v in (institution, form_type, tax_year) if v is not None)
    if signals_found == 3:
        confidence = "high"
    elif signals_found == 2:
        confidence = "medium"
    else:
        confidence = "low"

    return IdentificationResult(
        institution=institution,
        form_type=form_type,
        tax_year=tax_year,
        account_number=account_number,
        confidence=confidence,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def identify_pdf(pdf_path: Path) -> IdentificationResult:
    """Identify a tax PDF by running OCR then classifying the text.

    Raises:
        RuntimeError: If extract_pdf could not be imported (missing
            Google Cloud dependency).
        FileNotFoundError: If the PDF path does not exist.
    """
    if extract_ocr_text is None:
        raise RuntimeError(
            "extract_ocr_text unavailable — google-cloud-documentai is not installed. "
            "Use _classify_text(raw_text) directly if you already have OCR output."
        )

    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    ocr_result = extract_ocr_text(pdf_path)
    result = _classify_text(ocr_result["text"])
    return result


def identify_batch(pdf_paths: list[Path]) -> list[IdentificationResult]:
    """Identify multiple tax PDFs. Prints progress to stderr."""
    results: list[IdentificationResult] = []
    for i, path in enumerate(pdf_paths, 1):
        print(f"  [{i}/{len(pdf_paths)}] Identifying {path.name}...", file=sys.stderr)
        result = identify_pdf(path)
        print(
            f"    -> {result.institution or '?'} / {result.form_type or '?'} / "
            f"{result.tax_year or '?'} ({result.confidence})",
            file=sys.stderr,
        )
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Identify tax PDFs via OCR text classification"
    )
    parser.add_argument("--file", help="Path to a single PDF")
    parser.add_argument("--dir", help="Path to a directory of PDFs")
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    if not args.file and not args.dir:
        parser.error("Provide --file or --dir")

    paths: list[Path] = []
    if args.file:
        paths.append(Path(args.file))
    if args.dir:
        dir_path = Path(args.dir)
        if not dir_path.is_dir():
            parser.error(f"Not a directory: {args.dir}")
        paths.extend(sorted(dir_path.glob("*.pdf")))

    if not paths:
        print("No PDF files found.", file=sys.stderr)
        sys.exit(1)

    results = identify_batch(paths)

    if args.output == "json":
        import json

        print(json.dumps([r.model_dump() for r in results], indent=2, default=str))
    else:
        for path, result in zip(paths, results):
            print(f"\n{'='*60}")
            print(f"File:        {path.name}")
            print(f"Institution: {result.institution or 'Unknown'}")
            print(f"Form:        {result.form_type or 'Unknown'}")
            print(f"Tax Year:    {result.tax_year or 'Unknown'}")
            print(f"Account:     {result.account_number or 'Unknown'}")
            print(f"Confidence:  {result.confidence}")


if __name__ == "__main__":
    main()
