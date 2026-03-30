# Last Edited: 2026-03-27 12:30
"""Google Document AI OCR extraction for tax PDFs.

Extracts raw text from PDFs using Google Document AI. The Claude Code
orchestrator handles structured field extraction (Vision) and reconciliation
during skill execution — no Anthropic API key needed.

Usage:
    python3 -m execution.tax.extract_pdf --file path/to/1099.pdf
    python3 -m execution.tax.extract_pdf --file path/to/1099.pdf --output json
"""

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import documentai

_env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_env_path)

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
CREDENTIALS_PATH = WORKSPACE_ROOT / os.environ.get(
    "GOOGLE_SERVICE_ACCOUNT_FILE", "execution/.credentials/service_account.json"
)

# Parse Google OCR endpoint
_ocr_endpoint = os.environ.get("GOOGLE_OCR", "")
_parts = _ocr_endpoint.replace(":process", "").split("/")
GOOGLE_PROJECT_ID = _parts[_parts.index("projects") + 1] if "projects" in _parts else ""
GOOGLE_LOCATION = _parts[_parts.index("locations") + 1] if "locations" in _parts else ""
GOOGLE_PROCESSOR_ID = _parts[_parts.index("processors") + 1] if "processors" in _parts else ""


def extract_ocr_text(pdf_path: Path) -> dict:
    """Send PDF to Google Document AI. Returns {"text": ..., "entities": [...]}."""
    client = documentai.DocumentProcessorServiceClient.from_service_account_file(
        str(CREDENTIALS_PATH)
    )
    resource_name = client.processor_path(GOOGLE_PROJECT_ID, GOOGLE_LOCATION, GOOGLE_PROCESSOR_ID)

    with open(pdf_path, "rb") as f:
        pdf_content = f.read()

    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(
            content=pdf_content,
            mime_type="application/pdf",
        ),
    )

    response = client.process_document(request=request)
    document = response.document

    entities = []
    for entity in document.entities:
        entities.append({
            "type": entity.type_ or "unknown",
            "value": entity.mention_text or "",
            "confidence": entity.confidence,
        })

    return {
        "file": pdf_path.name,
        "text": document.text,
        "text_length": len(document.text),
        "entity_count": len(entities),
        "entities": entities,
    }


def extract_batch(pdf_paths: list[Path]) -> list[dict]:
    """Extract OCR text from multiple PDFs."""
    results = []
    for path in pdf_paths:
        print(f"  [OCR] {path.name}...")
        result = extract_ocr_text(path)
        print(f"    {result['text_length']} chars, {result['entity_count']} entities")
        results.append(result)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from tax PDFs via Google Document AI")
    parser.add_argument("--file", required=True, help="Path to PDF (or glob pattern)")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    pdf_path = Path(args.file)
    if not pdf_path.is_absolute():
        pdf_path = WORKSPACE_ROOT / pdf_path

    result = extract_ocr_text(pdf_path)

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"File: {result['file']}")
        print(f"Text length: {result['text_length']} chars")
        print(f"Entities: {result['entity_count']}")
        print(f"\n{'='*60}")
        print(result["text"])


if __name__ == "__main__":
    main()
