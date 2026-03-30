# Last Edited: 2026-03-30
"""Upload tax PDFs to Supabase Storage and write public URLs to documents.storage_url.

Usage:
    python3 -m execution.tax.upload_to_storage --year 2025
    python3 -m execution.tax.upload_to_storage --year 2025 --dry-run
    python3 -m execution.tax.upload_to_storage --year 2025 --file 2025_betterment_5498-fmv_43197.pdf
"""

import argparse
from pathlib import Path

from execution.db.client import get_client

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_BASE = WORKSPACE_ROOT / "tax_document_archive"
BUCKET_NAME = "tax-documents"


def ensure_bucket(client) -> None:
    """Create the storage bucket if it doesn't exist."""
    try:
        client.storage.get_bucket(BUCKET_NAME)
    except Exception:
        client.storage.create_bucket(BUCKET_NAME, options={"public": True})
        print(f"  Created bucket '{BUCKET_NAME}' (public)")


def get_public_url(client, storage_path: str) -> str:
    """Get the public URL for a file in the bucket."""
    return client.storage.from_(BUCKET_NAME).get_public_url(storage_path)


def upload_file(client, local_path: Path, storage_path: str) -> str:
    """Upload a single file to Supabase Storage. Returns the public URL."""
    with open(local_path, "rb") as f:
        client.storage.from_(BUCKET_NAME).upload(
            storage_path,
            f,
            file_options={"content-type": "application/pdf", "upsert": "true"},
        )
    return get_public_url(client, storage_path)


def update_storage_url(client, file_path: str, storage_url: str) -> bool:
    """Write storage_url to the documents row matching file_path. Does NOT touch status."""
    result = (
        client.table("documents")
        .update({"storage_url": storage_url})
        .eq("file_path", file_path)
        .execute()
    )
    return len(result.data) > 0


def upload_year(tax_year: int, dry_run: bool = False, single_file: str | None = None) -> None:
    """Upload all PDFs for a tax year (or a single file) to Supabase Storage."""
    archive_dir = ARCHIVE_BASE / str(tax_year)
    if not archive_dir.exists():
        print(f"  Archive directory not found: {archive_dir}")
        return

    if single_file:
        pdf_files = [archive_dir / single_file]
        if not pdf_files[0].exists():
            print(f"  File not found: {pdf_files[0]}")
            return
    else:
        pdf_files = sorted(archive_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"  No PDFs found in {archive_dir}")
        return

    client = get_client()

    if not dry_run:
        ensure_bucket(client)

    uploaded = 0
    db_updated = 0
    db_missed = 0
    errors = 0

    for pdf_path in pdf_files:
        storage_path = f"{tax_year}/{pdf_path.name}"
        file_path = f"tax_document_archive/{tax_year}/{pdf_path.name}"

        if dry_run:
            print(f"  [DRY RUN] Would upload: {pdf_path.name} -> {storage_path}")
            continue

        try:
            public_url = upload_file(client, pdf_path, storage_path)
            uploaded += 1

            if update_storage_url(client, file_path, public_url):
                db_updated += 1
                print(f"  ✅ {pdf_path.name} -> storage_url set")
            else:
                db_missed += 1
                print(f"  ⚠️  {pdf_path.name} -> uploaded, but no DB match for file_path={file_path}")
        except Exception as e:
            errors += 1
            print(f"  ❌ {pdf_path.name} -> {e}")

    if not dry_run:
        print(f"\n  Summary: {uploaded} uploaded, {db_updated} DB updated, "
              f"{db_missed} no DB match, {errors} errors")


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload tax PDFs to Supabase Storage")
    parser.add_argument("--year", type=int, required=True, help="Tax year")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be uploaded")
    parser.add_argument("--file", type=str, help="Upload a single file instead of all PDFs")
    args = parser.parse_args()

    print(f"Uploading {args.year} tax PDFs to Supabase Storage...\n")
    upload_year(args.year, dry_run=args.dry_run, single_file=args.file)


if __name__ == "__main__":
    main()
