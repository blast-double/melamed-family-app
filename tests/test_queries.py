# Last Edited: 2026-03-26 12:00
"""Verify MVP tax queries work against seeded data. Each test resets its own state."""

import pytest
from execution.db.queries import (
    get_missing_documents,
    get_received_documents,
    get_cpa_package,
    get_document_status_summary,
    get_documents_by_entity,
    mark_document_received,
    mark_document_submitted,
)
from execution.db.client import get_client


@pytest.fixture(scope="module")
def client():
    return get_client()


def _reset_doc(client, name: str) -> None:
    """Reset a document back to expected state."""
    client.table("documents").update(
        {"status": "expected", "file_path": None}
    ).eq("name", name).execute()


def test_missing_documents_returns_expected(client):
    """Missing docs query returns documents in 'expected' status."""
    missing = get_missing_documents(2024)
    assert len(missing) >= 1
    assert all("name" in doc for doc in missing)


def test_received_documents_shape(client):
    """Received documents returns a list."""
    received = get_received_documents(2024)
    assert isinstance(received, list)


def test_status_summary_shape(client):
    """Status summary returns a dict of status: count."""
    summary = get_document_status_summary(2024)
    assert isinstance(summary, dict)
    total = sum(summary.values())
    assert total >= 23


def test_documents_by_entity(client):
    """Query docs by source entity name."""
    schwab_docs = get_documents_by_entity("Schwab", 2024)
    schwab_names = [d["name"] for d in schwab_docs]
    assert "2024 Schwab 1099-Composite" in schwab_names


def test_mark_received_and_submitted(client):
    """Mark a doc as received, then submitted, verify status changes."""
    doc = mark_document_received(
        "2024 Schwab 1099-Composite",
        file_path="tax_document_archive/2024/Schwab 1099 Composite and Year-End Summary - 2024_2025-02-07_117.PDF"
    )
    assert doc["status"] == "received"
    assert doc["file_path"] is not None

    doc = mark_document_submitted("2024 Schwab 1099-Composite")
    assert doc["status"] == "submitted"

    # Reset
    _reset_doc(client, "2024 Schwab 1099-Composite")


def test_cpa_package_groups_by_schedule(client):
    """CPA package groups docs by schedule after marking some received."""
    mark_document_received("2024 Marcus 1099-INT")
    mark_document_received("2024 Amex 1099-INT")

    package = get_cpa_package(2024)
    assert "Schedule B" in package
    assert "2024 Marcus 1099-INT" in package["Schedule B"]

    # Reset
    _reset_doc(client, "2024 Marcus 1099-INT")
    _reset_doc(client, "2024 Amex 1099-INT")
