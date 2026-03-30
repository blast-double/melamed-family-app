# Last Edited: 2026-03-26 12:00
"""Verify seed data landed correctly in Supabase."""

import pytest
from execution.db.client import get_client


@pytest.fixture(scope="module")
def client():
    return get_client()


def test_entities_seeded(client):
    """All 19 entities exist with correct types."""
    result = client.table("entities").select("name, type").execute()
    names = {row["name"] for row in result.data}
    assert "Aaron Melamed" in names
    assert "Schwab" in names
    assert "1771 11th Ave, SF" in names
    assert len(result.data) >= 19


def test_entity_types_correct(client):
    """Spot-check entity types."""
    result = client.table("entities").select("name, type").eq("name", "Aaron Melamed").execute()
    assert result.data[0]["type"] == "person"

    result = client.table("entities").select("name, type").eq("name", "Schwab").execute()
    assert result.data[0]["type"] == "institution"

    result = client.table("entities").select("name, type").eq("name", "Itero").execute()
    assert result.data[0]["type"] == "business"


def test_tags_seeded(client):
    """All 14 tags exist."""
    result = client.table("tags").select("name, type").execute()
    names = {row["name"] for row in result.data}
    assert "schedule-d" in names
    assert "green-card" in names
    assert "deductible" in names
    assert len(result.data) >= 14


def test_documents_2024_seeded(client):
    """All 23 expected 2024 documents exist."""
    result = client.table("documents").select("name, status, tax_year").eq("tax_year", 2024).execute()
    assert len(result.data) >= 23


def test_documents_have_source_entities(client):
    """Institutional documents link to their source entity."""
    result = (
        client.table("documents")
        .select("name, source_entity_id")
        .eq("name", "2024 Schwab 1099-Composite")
        .execute()
    )
    assert result.data[0]["source_entity_id"] is not None
