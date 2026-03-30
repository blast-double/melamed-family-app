---
name: ingest-tax-docs
description: Auto-identify and rename tax documents dropped in the archive. Uses pattern matching first, then OCR for unrecognized PDFs. Dry-run by default with rollback safety.
user-invocable: true
---

# Ingest Tax Documents

Auto-identify and rename tax documents dropped in the archive. Pattern matching first (fast), OCR fallback for unrecognized PDFs. Dry-run by default.

## Prerequisites

- `config/tax_documents_master.yaml` exists (master checklist with filename patterns)
- `config/tax_config.yaml` exists (per-year config with conditionals)
- `GOOGLE_OCR` and `GOOGLE_SERVICE_ACCOUNT_FILE` in `.env` (only needed for OCR fallback)

## Workflow

### Step 1: Parse the Request

Extract the tax year from the user's request:
- "ingest tax docs for 2025" → year 2025
- "ingest my tax documents" → default to current year minus 1

### Step 2: Dry-Run Pattern Matching

Run the rename tool in dry-run mode (no files touched):

```bash
python3 -m execution.tax.rename_docs --year {year}
```

Show the user the full output:
- **Renames:** files that will be renamed to canonical format
- **Multi-match:** files matching multiple specs (need manual review)
- **Unmatched:** files matching no spec

### Step 3: OCR Identification of Unmatched PDFs

If there are unmatched **PDF** files (skip CSVs and other non-PDFs):

```bash
python3 -m execution.tax.identify_pdf --dir tax_document_archive/{year}/ --output text
```

Present OCR results grouped by confidence:

- **High confidence** → include in rename plan, note the identification
- **Medium confidence** → present to user: "OCR thinks this is {institution} {form} for {year}. Include in rename?"
- **Low confidence** → present to user: "Could not confidently identify {filename}. Leave unrenamed."

**Never auto-rename medium or low confidence files.** Only high confidence gets auto-included.

### Step 4: Apply Renames (User Approval Required)

After user reviews the dry-run + OCR results:

```bash
python3 -m execution.tax.rename_docs --year {year} --apply
```

Confirm:
- Rollback manifest written (`.rename_manifest.json`)
- Number of files renamed
- Any files left unrenamed (with reason)

### Step 5: Show Updated Gap Status

After renames are applied, show what's still missing:

```bash
python3 -m execution.tax.match_files --year {year} --dry-run
```

This shows matched, missing, not-expected, and reference docs.

### Step 6: Upload to Supabase Storage

After matching is complete, upload renamed files to Supabase Storage so the tax-portal can display them:

```bash
python3 -m execution.tax.upload_to_storage --year {year}
```

Confirm:
- Number of files uploaded
- Number of DB records updated with `storage_url`
- Any files with no DB match (expected for unmapped archive files)

## Rollback

If renames were wrong:

```bash
python3 -m execution.tax.rename_docs --year {year} --rollback
```

This reads `.rename_manifest.json` and reverses all renames.

## Error Handling

| Error | Fix |
|---|---|
| Archive directory doesn't exist | Create `tax_document_archive/{year}/` and tell user to add files |
| No new files to process | Report "all files already follow canonical naming" |
| OCR returns low confidence | Show identification but do NOT include in rename plan |
| Multiple files match same spec | Show in "multi-match" section for manual review |
| Rollback manifest missing | Cannot rollback — files were renamed without manifest (shouldn't happen) |

## Acceptance Checks

- All pattern-matchable files renamed (0 false negatives from known patterns)
- Rollback manifest written before any renames applied
- Ambiguous files stay unrenamed (not silently misnamed)
- Non-PDF unmatched files (CSVs) reported separately, not sent to OCR

## Reference

- **Rename tool**: `execution/tax/rename_docs.py`
- **OCR identifier**: `execution/tax/identify_pdf.py`
- **File matcher**: `execution/tax/match_files.py`
- **Master checklist**: `config/tax_documents_master.yaml`
- **Per-year config**: `config/tax_config.yaml`
- **Storage uploader**: `execution/tax/upload_to_storage.py`
- **Directive**: `directives/tax/tax-preparation.md`
