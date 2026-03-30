---
name: extract-tax-forms
description: Extract structured data from tax PDFs using dual-pass OCR + Vision extraction. Reconciles field-by-field, stores in Supabase for the tax portal's /verify page.
user-invocable: true
---

# Extract Tax Forms

Dual-pass extraction: Google Document AI OCR + Claude Vision. Reconcile field-by-field. Store in Supabase `documents.metadata.extracted` for the tax portal.

## Prerequisites

- `GOOGLE_OCR` and `GOOGLE_SERVICE_ACCOUNT_FILE` in `.env`
- `SUPABASE_PROJECT_URL` and `SUPABASE_SERVICE_ROLE_KEY` in `.env`
- Tax documents renamed to canonical format in `tax_document_archive/{year}/`
- 2025 documents seeded in Supabase (run `python3 -m execution.tax.seed_tax_year --year {year}` if not)

## Workflow

### Step 1: Parse the Request

Extract the tax year:
- "extract tax forms for 2025" → year 2025
- "extract my tax forms" → default to current year minus 1

### Step 2: Verify Supabase is Seeded

Check that document rows exist for the tax year:
```bash
python3 -c "from execution.db.queries import get_document_status_summary; print(get_document_status_summary({year}))"
```

If empty, seed first:
```bash
python3 -m execution.tax.seed_tax_year --year {year}
```

For multi-account documents (e.g., Betterment 5498-FMV with two accounts), upsert separate rows:
```python
from execution.db.queries import upsert_document
# After seeding, create individual multi-account rows
upsert_document({
    "name": "2025 Betterment 5498-FMV (43197)",
    "type": "tax_form",
    "tax_year": 2025,
    "tax_schedule": "Form 5498 / IRA",
    "form_number": "5498-FMV",
    "status": "received",
    # ... (copy source_entity_id and owner_entity_id from the base row)
})
```

### Step 3: List PDFs to Extract

Scan `tax_document_archive/{year}/` for PDF files only (skip CSVs, markdown, manifests).

Map each PDF to its extraction prompt using the form slug from the filename:

| Form slug in filename | Prompt file |
|----------------------|-------------|
| `1098` | `config/extraction_prompts/1098.txt` |
| `1099-int` | `config/extraction_prompts/1099_int.txt` |
| `1099-composite` | `config/extraction_prompts/1099_composite.txt` |
| `1099-b-div` | `config/extraction_prompts/1099_b_div.txt` |
| `1099-k` | `config/extraction_prompts/1099_k.txt` |
| `1099-supplemental` | `config/extraction_prompts/1099_supplemental.txt` |
| `5498-fmv` | `config/extraction_prompts/5498_fmv.txt` |

### Step 4: Extract Each PDF (Dual-Pass)

For each PDF:

**Pass 1 — OCR:**
```bash
python3 -m execution.tax.extract_pdf --file {path} --output json
```
This returns raw text + entities from Google Document AI.

**Pass 2 — Vision:**
Read the PDF directly using Claude's vision capability. Apply the extraction prompt from Step 3 to extract structured JSON fields.

**Reconcile:**
Compare OCR-extracted values against Vision-extracted values field-by-field:
- Both agree → `confidence: "verified"`
- Disagree → `confidence: "disputed"` (flag for review)
- Only one source has the value → `confidence: "single_source"`

### Step 5: Store in Supabase

For each extracted document, store under `metadata.extracted` (this is what the portal reads):

```python
from execution.db.queries import mark_document_extracted

mark_document_extracted("2025 Goldman Sachs Marcus 1099-INT", {
    "fields": [
        {
            "label": "Box 1 - Interest income",
            "value": "2960.31",
            "confidence": "verified",
            "ocr_value": "2960.31",
            "vision_value": "2960.31",
            "schedule_line": "Schedule B, Part I"
        }
    ],
    "extraction_status": "complete",
    "disputed_count": 0,
    "extracted_at": "2026-03-30T09:00:00"
})
```

**Multi-account document names:**
- `2025_betterment_5498-fmv_43197.pdf` → `"2025 Betterment 5498-FMV (43197)"`
- `2025_betterment_5498-fmv_73349.pdf` → `"2025 Betterment 5498-FMV (73349)"`

### Step 6: Report Results

Show a summary table:

```
Document                              Fields  Verified  Disputed
─────────────────────────────────────────────────────────────────
2025 New American Funding 1098            10        10         0
2025 Goldman Sachs Marcus 1099-INT        11        11         0
2025 American Express 1099-INT            11        11         0
...
```

If any disputed fields exist, present them for resolution before proceeding.

### Step 7: Verify in Portal

Tell the user to check the tax portal's `/verify` page to confirm extracted data displays correctly.

## Error Handling

| Error | Fix |
|---|---|
| OCR fails (Google API error) | Check `.env` credentials, verify Google service account |
| No extraction prompt for form type | Create prompt in `config/extraction_prompts/`, follow existing format |
| Supabase document not found | Run `seed_tax_year` to create the row first |
| Disputed fields | Present both OCR and Vision values, let user pick the correct one |
| PDF is image-only (no selectable text) | OCR handles this — Google Document AI does full OCR on images |

## Reference

- **OCR extraction**: `execution/tax/extract_pdf.py`
- **DB queries**: `execution/db/queries.py` (`mark_document_extracted`, `upsert_document`)
- **Extraction prompts**: `config/extraction_prompts/`
- **Models**: `execution/tax/models.py` (ExtractedData, ReconciledField, ReconciliationResult)
- **Tax portal verify page**: `tax-portal/src/app/verify/page.tsx`
- **Directive**: `directives/tax/tax-preparation.md`
