# Last Edited: 2026-03-26 12:00
"""Verify Supabase connection works via both REST client and psycopg2."""

from execution.db.client import get_client, get_database_url
import psycopg2


def test_supabase_client_connects():
    """Supabase REST client can reach the project and query entities."""
    client = get_client()
    result = client.table("entities").select("id").limit(1).execute()
    assert hasattr(result, "data")


def test_database_url_valid():
    """psycopg2 can connect using the database URL."""
    conn = psycopg2.connect(get_database_url())
    cur = conn.cursor()
    cur.execute("SELECT 1")
    assert cur.fetchone()[0] == 1
    conn.close()
