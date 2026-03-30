# Supabase Storage PDF Serving — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Serve tax PDFs from Supabase Storage so the Vercel-deployed tax-portal can display them.

**Architecture:** Upload PDFs from local archive to a public Supabase Storage bucket. Write the public URL to the existing `storage_url` column. Frontend reads `storage_url` directly — no API proxy needed. The `/api/pdf` route stays as a fallback until cutover validates.

**Tech Stack:** Python (supabase-py), Next.js/TypeScript (tax-portal), Supabase Storage

**Spec:** `docs/superpowers/specs/2026-03-30-supabase-storage-pdf-serving-design.md`

---

## File Structure

| Action | Path | Responsibility |
|--------|------|---------------|
| Create | `execution/tax/upload_to_storage.py` | CLI tool: upload PDFs to Supabase Storage, write `storage_url` to DB |
| Modify | `tax-portal/src/lib/types.ts:54-64` | Add `storage_url` to `ExtractedDocument` interface |
| Modify | `tax-portal/src/app/verify/page.tsx:340-350,569,388-397` | Add `storage_url` to `SupabaseDoc`, select query, and `buildScheduleGroups` mapping |
| Modify | `tax-portal/src/components/document-drawer.tsx:133-136` | Use `storage_url` with fallback to `/api/pdf` |
| Modify | `.claude/skills/ingest-tax-docs/SKILL.md:67-75` | Add Step 6: upload to Supabase Storage |

---

### Task 1: Upload Script — `execution/tax/upload_to_storage.py`

**Files:**
- Create: `execution/tax/upload_to_storage.py`

- [ ] **Step 1: Write the upload script**

```python
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
```

- [ ] **Step 2: Test the script with dry-run**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal && python3 -m execution.tax.upload_to_storage --year 2025 --dry-run`

Expected: List of PDFs that would be uploaded, no actual uploads.

- [ ] **Step 3: Test with a single real file**

Run: `python3 -m execution.tax.upload_to_storage --year 2025 --file 2025_betterment_5498-fmv_43197.pdf`

Expected: One file uploaded, `storage_url` set in DB, prints `✅`.

Verify in DB:
```bash
python3 -c "
from execution.db.client import get_client
c = get_client()
r = c.table('documents').select('name, storage_url').like('file_path', '%betterment_5498-fmv%').execute()
print(r.data)
"
```

Expected: Row has non-null `storage_url` starting with the Supabase project URL.

- [ ] **Step 4: Commit**

```bash
git add execution/tax/upload_to_storage.py
git commit -m "feat: add Supabase Storage upload script for tax PDFs"
```

---

### Task 2: Full Backfill — Upload All 2025 PDFs

**Files:** None (uses script from Task 1)

- [ ] **Step 1: Run the full upload**

Run: `python3 -m execution.tax.upload_to_storage --year 2025`

Expected: All PDFs uploaded, most with DB matches. Note any "no DB match" warnings.

- [ ] **Step 2: Verify coverage**

```bash
python3 -c "
from execution.db.client import get_client
c = get_client()
total = c.table('documents').select('id', count='exact').eq('tax_year', 2025).neq('status', 'expected').execute()
has_url = c.table('documents').select('id', count='exact').eq('tax_year', 2025).neq('status', 'expected').neq('storage_url', None).execute()
print(f'Documents with storage_url: {has_url.count} / {total.count}')
"
```

Expected: All (or nearly all) non-expected documents have `storage_url`.

---

### Task 3: Frontend — Add `storage_url` to Types and Query

**Files:**
- Modify: `tax-portal/src/lib/types.ts:54-64`
- Modify: `tax-portal/src/app/verify/page.tsx:340-350,569,388-397`

- [ ] **Step 1: Add `storage_url` to `ExtractedDocument` interface**

In `tax-portal/src/lib/types.ts`, add `storage_url` to the interface:

```typescript
export interface ExtractedDocument {
  id: string;
  name: string;
  form_type: string;
  institution: string;
  tax_year: number;
  tax_schedule: string;
  status: "expected" | "received" | "extracted" | "verified";
  fields: ReconciledField[];
  file_path: string | null;
  storage_url: string | null;
}
```

- [ ] **Step 2: Add `storage_url` to `SupabaseDoc` interface in `verify/page.tsx`**

In `tax-portal/src/app/verify/page.tsx`, update the `SupabaseDoc` interface:

```typescript
interface SupabaseDoc {
  id: string;
  name: string;
  form_number: string | null;
  tax_schedule: string | null;
  status: string;
  file_path: string | null;
  storage_url: string | null;
  tax_year: number;
  metadata: Record<string, unknown>;
  source_entity: { name: string } | null;
}
```

- [ ] **Step 3: Add `storage_url` to the Supabase select query**

In `tax-portal/src/app/verify/page.tsx`, update the `.select()` call (~line 569):

```typescript
.select("id, name, form_number, tax_schedule, status, file_path, storage_url, tax_year, metadata, source_entity:entities!source_entity_id(name)")
```

- [ ] **Step 4: Pass `storage_url` through in `buildScheduleGroups`**

In `tax-portal/src/app/verify/page.tsx`, update the mapping inside `buildScheduleGroups` (~line 387-398):

```typescript
return {
  id: doc.id,
  name: doc.name,
  form_type: doc.form_number || "Unknown",
  institution: doc.source_entity?.name || "Unknown",
  tax_year: doc.tax_year,
  tax_schedule: doc.tax_schedule || "",
  status: doc.status as ExtractedDocument["status"],
  fields,
  file_path: doc.file_path,
  storage_url: doc.storage_url,
};
```

- [ ] **Step 5: Commit**

```bash
cd tax-portal
git add src/lib/types.ts src/app/verify/page.tsx
git commit -m "feat: add storage_url to document types and query"
```

---

### Task 4: Frontend — Use `storage_url` in Document Drawer

**Files:**
- Modify: `tax-portal/src/components/document-drawer.tsx:133-136`

- [ ] **Step 1: Update PDF URL construction**

In `tax-portal/src/components/document-drawer.tsx`, replace the `pdfUrl` logic (~line 133-136):

```typescript
// Prefer Supabase Storage URL; fall back to local API route for dev
const pdfUrl = doc.storage_url
  || (doc.file_path ? `/api/pdf?path=${encodeURIComponent(doc.file_path)}` : null);
```

- [ ] **Step 2: Verify the build passes**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal/tax-portal && npm run build`

Expected: Build succeeds with no type errors.

- [ ] **Step 3: Commit**

```bash
git add src/components/document-drawer.tsx
git commit -m "feat: serve PDFs from Supabase Storage with local fallback"
```

---

### Task 5: Cutover Validation

**Files:** None (validation only)

- [ ] **Step 1: Deploy to Vercel**

Push the tax-portal changes and confirm deployment succeeds.

- [ ] **Step 2: Verify on deployed site**

Open the Vercel-deployed tax-portal `/verify` page. Click "View Source Document" on the Betterment 5498-FMV (the one from the original screenshot). Confirm the PDF loads.

- [ ] **Step 3: Spot-check a second document**

Open another document drawer. Confirm PDF loads.

- [ ] **Step 4: Check for any documents with missing `storage_url`**

```bash
python3 -c "
from execution.db.client import get_client
c = get_client()
r = c.table('documents').select('name, file_path').eq('tax_year', 2025).neq('status', 'expected').is_('storage_url', 'null').execute()
if r.data:
    print(f'{len(r.data)} documents missing storage_url:')
    for d in r.data:
        print(f'  - {d[\"name\"]}')
else:
    print('All documents have storage_url ✅')
"
```

---

### Task 6: Delete `/api/pdf` Route (After Cutover)

**Files:**
- Delete: `tax-portal/src/app/api/pdf/route.ts`

Only proceed if Task 5 validates successfully.

- [ ] **Step 1: Delete the API route**

Remove `tax-portal/src/app/api/pdf/route.ts`.

- [ ] **Step 2: Remove the fallback from document-drawer**

In `tax-portal/src/components/document-drawer.tsx`, simplify:

```typescript
const pdfUrl = doc.storage_url || null;
```

- [ ] **Step 3: Build and deploy**

Run: `cd /Users/aaronmelamed/Dropbox/antigravity/workspaces/personal/tax-portal && npm run build`

Expected: Build succeeds.

- [ ] **Step 4: Commit**

```bash
git add -u
git commit -m "chore: remove /api/pdf route — PDFs served from Supabase Storage"
```

---

### Task 7: Update `ingest-tax-docs` Skill

**Files:**
- Modify: `.claude/skills/ingest-tax-docs/SKILL.md:67-75`

- [ ] **Step 1: Add Step 6 to the skill**

In `.claude/skills/ingest-tax-docs/SKILL.md`, after the existing Step 5 block (line 75), add:

```markdown
### Step 6: Upload to Supabase Storage

After matching is complete, upload renamed files to Supabase Storage so the tax-portal can display them:

\`\`\`bash
python3 -m execution.tax.upload_to_storage --year {year}
\`\`\`

Confirm:
- Number of files uploaded
- Number of DB records updated with `storage_url`
- Any files with no DB match (expected for unmapped archive files)
```

- [ ] **Step 2: Add the upload tool to the Reference section**

In the `## Reference` section at the bottom, add:

```markdown
- **Storage uploader**: `execution/tax/upload_to_storage.py`
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/ingest-tax-docs/SKILL.md
git commit -m "feat: add Supabase Storage upload step to ingest-tax-docs skill"
```
