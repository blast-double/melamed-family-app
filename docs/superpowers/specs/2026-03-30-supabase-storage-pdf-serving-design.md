# Supabase Storage PDF Serving

*2026-03-30*

## Problem

The tax-portal PDF viewer fails on Vercel with "Failed to load PDF." The API route (`/api/pdf`) reads PDFs from the local filesystem via `readFile`, which doesn't exist in Vercel's serverless environment. PDFs live only on Aaron's local machine at `tax_document_archive/{year}/`.

## Solution

Store PDFs in Supabase Storage and serve them via public URLs. The DB already has a `storage_url` column (unused) — populate it and use it in the frontend.

## Components

### 1. Supabase Storage Bucket

- **Bucket name:** `tax-documents`
- **Access:** Public (auth planned later)
- **Path convention:** `{year}/{filename}` — mirrors local archive minus `tax_document_archive/` prefix
- Example: `2025/2025_betterment_5498-fmv_43197.pdf` in the bucket

### 2. Upload Script — `execution/tax/upload_to_storage.py`

Standalone CLI tool that uploads PDFs to Supabase Storage and writes the public URL to `storage_url` in the documents table.

**Interface:**
```
python3 -m execution.tax.upload_to_storage --year 2025
python3 -m execution.tax.upload_to_storage --year 2025 --dry-run
python3 -m execution.tax.upload_to_storage --year 2025 --file 2025_betterment_5498-fmv_43197.pdf
```

**Logic:**
1. List all PDFs in `tax_document_archive/{year}/`
2. For each PDF, check if it already exists in the bucket (skip if same size)
3. Upload to `tax-documents/{year}/{filename}`
4. Get the public URL from Supabase
5. Find the matching document row by `file_path` = `tax_document_archive/{year}/{filename}`
6. Write the public URL to `storage_url`
7. Print summary: uploaded, skipped (already exists), no DB match

**Flags:**
- `--dry-run`: Show what would be uploaded without uploading
- `--file`: Upload a single file instead of the whole year directory
- `--year`: Required — tax year to process

**Dependencies:** `supabase-py` (already installed for DB access).

### 3. Ingest Skill Update — `ingest-tax-docs` SKILL.md

Add **Step 6: Upload to Supabase Storage** after the existing Step 5 (gap status).

After files are renamed, matched, and marked in the DB, upload them to Supabase Storage:

```bash
python3 -m execution.tax.upload_to_storage --year {year}
```

This is the natural integration point — files have canonical names and DB records at this stage.

### 4. Tax-Portal Frontend Changes

**`document-drawer.tsx`** — Prefer `storage_url`, fall back to `/api/pdf` route:

```typescript
const pdfUrl = doc.storage_url
  || (doc.file_path ? `/api/pdf?path=${encodeURIComponent(doc.file_path)}` : null);
```

**`/api/pdf/route.ts`** — Keep as local-dev fallback until cutover validates (see Cutover section). Delete after.

**`verify/page.tsx`** — Add `storage_url` to the Supabase select query.

**`lib/types.ts`** — Add `storage_url` to the `ExtractedDocument` type.

### 5. DB Writes

The upload script writes `storage_url` directly — a targeted update on the `documents` table filtered by `file_path`. It does NOT touch `status` or use `mark_document_received`. This avoids regressing documents that are already `submitted` or `verified`.

## Data Flow

```
Local archive → upload_to_storage.py → Supabase Storage bucket (public)
                                      → documents.storage_url (DB)

Tax-portal → reads storage_url from DB → passes URL to PDFViewer → pdf.js loads directly
```

## What Stays the Same

- `file_path` column — keeps the local relative path for scripts that read from disk
- `rename_docs.py`, `identify_pdf.py` — unchanged, still work on local files
- `match_files.py` — still writes `file_path`; upload script handles `storage_url` separately
- `extract_pdf.py` — still reads local files for OCR/vision extraction

## Bucket Creation

The bucket must be created once in Supabase dashboard or via the upload script on first run. The script should handle bucket creation if it doesn't exist:

```python
supabase.storage.create_bucket("tax-documents", options={"public": True})
```

## Cutover

The frontend switch and `/api/pdf` deletion happen only after all checks pass:

1. **Backfill first:** Run `python3 -m execution.tax.upload_to_storage --year 2025` for the current tax year
2. **Verify DB:** Confirm every document shown on `/verify` has a non-null `storage_url`
3. **Verify browser:** Open one document drawer on the deployed Vercel site, confirm PDF loads from `storage_url`
4. **If any check fails:** The fallback chain (`storage_url || /api/pdf`) keeps the old path alive. Do not delete `/api/pdf/route.ts` until all checks pass.

## Edge Cases

| Case | Handling |
|------|----------|
| File already in bucket (same size) | Skip upload, still update `storage_url` if missing |
| PDF in archive but no DB record | Upload to bucket, warn "no DB match" |
| DB record has `file_path` but file missing locally | Skip, warn |
| Bucket doesn't exist yet | Create it on first upload |
| Upload fails mid-batch | Continue with remaining files, report failures at end |
