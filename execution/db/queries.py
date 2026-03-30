# Last Edited: 2026-03-30 09:00
"""Tax MVP queries against the family Supabase database."""

from execution.db.client import get_client


def get_missing_documents(tax_year: int) -> list[dict]:
    """Return documents still in 'expected' status for a given tax year."""
    client = get_client()
    result = (
        client.table("documents")
        .select("name, form_number, tax_schedule, metadata")
        .eq("tax_year", tax_year)
        .eq("status", "expected")
        .order("tax_schedule")
        .order("name")
        .execute()
    )
    return result.data


def get_received_documents(tax_year: int) -> list[dict]:
    """Return documents that have been received for a given tax year."""
    client = get_client()
    result = (
        client.table("documents")
        .select("name, form_number, tax_schedule, status, file_path")
        .eq("tax_year", tax_year)
        .in_("status", ["received", "submitted", "verified"])
        .order("tax_schedule")
        .order("name")
        .execute()
    )
    return result.data


def get_cpa_package(tax_year: int) -> dict[str, list[str]]:
    """Return received/submitted documents grouped by tax schedule.

    Returns: {"Schedule D": ["2024 Schwab 1099-Composite", ...], ...}
    """
    docs = get_received_documents(tax_year)
    package: dict[str, list[str]] = {}
    for doc in docs:
        schedule = doc["tax_schedule"] or "Other"
        package.setdefault(schedule, []).append(doc["name"])
    return package


def get_document_status_summary(tax_year: int) -> dict[str, int]:
    """Return count of documents by status for a given tax year."""
    client = get_client()
    result = (
        client.table("documents")
        .select("status")
        .eq("tax_year", tax_year)
        .execute()
    )
    counts: dict[str, int] = {}
    for row in result.data:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return counts


def get_documents_by_entity(entity_name: str, tax_year: int) -> list[dict]:
    """Return all documents from a specific source entity for a tax year."""
    client = get_client()
    entity_result = client.table("entities").select("id").eq("name", entity_name).execute()
    if not entity_result.data:
        return []
    entity_id = entity_result.data[0]["id"]

    result = (
        client.table("documents")
        .select("name, status, tax_schedule, form_number")
        .eq("source_entity_id", entity_id)
        .eq("tax_year", tax_year)
        .order("name")
        .execute()
    )
    return result.data


def mark_document_received(document_name: str, file_path: str | None = None) -> dict:
    """Update a document's status to 'received' and optionally set file_path."""
    client = get_client()
    update = {"status": "received"}
    if file_path:
        update["file_path"] = file_path
    result = (
        client.table("documents")
        .update(update)
        .eq("name", document_name)
        .execute()
    )
    return result.data[0] if result.data else {}


def upsert_document(doc: dict) -> dict:
    """Create or update a document row by name."""
    client = get_client()
    result = client.table("documents").upsert(doc, on_conflict="name").execute()
    return result.data[0] if result.data else {}


def mark_document_extracted(
    document_name: str, extracted: dict, file_path: str | None = None
) -> dict:
    """Update status to 'extracted' and store extraction under metadata.extracted.

    The tax portal reads doc.metadata?.extracted?.fields, so the payload
    must be nested under the 'extracted' key within metadata.
    """
    client = get_client()
    # Fetch existing metadata to preserve other keys
    doc = (
        client.table("documents")
        .select("metadata")
        .eq("name", document_name)
        .execute()
    )
    existing_meta = doc.data[0]["metadata"] if doc.data and doc.data[0].get("metadata") else {}
    existing_meta["extracted"] = extracted
    update: dict = {"status": "extracted", "metadata": existing_meta}
    if file_path:
        update["file_path"] = file_path
    result = (
        client.table("documents")
        .update(update)
        .eq("name", document_name)
        .execute()
    )
    return result.data[0] if result.data else {}


def mark_document_submitted(document_name: str) -> dict:
    """Update a document's status to 'submitted'."""
    client = get_client()
    result = (
        client.table("documents")
        .update({"status": "submitted"})
        .eq("name", document_name)
        .execute()
    )
    return result.data[0] if result.data else {}
