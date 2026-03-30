# Last Edited: 2026-03-26 12:00
"""Run SQL migrations against Supabase PostgreSQL. Atomic — rolls back on any error."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import psycopg2

# Load .env from workspace root
_env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_env_path)

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def get_database_url() -> str:
    """Get the database connection string, handling the legacy env var name."""
    return os.environ.get("SUPABASE_DATABASE_URL") or os.environ["SUPABASE_DATA_STRING_CONNETION"]


def run_migration(filename: str) -> None:
    """Execute a single migration file atomically."""
    sql_path = MIGRATIONS_DIR / filename
    if not sql_path.exists():
        print(f"Migration file not found: {sql_path}")
        sys.exit(1)

    sql = sql_path.read_text()
    db_url = get_database_url()

    conn = psycopg2.connect(db_url)
    try:
        # The SQL file contains its own BEGIN/COMMIT, so use autocommit
        # to let the SQL manage its own transaction
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql)
        print(f"Migration {filename} applied successfully.")
    except Exception as e:
        print(f"Migration {filename} FAILED: {e}")
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    migration = sys.argv[1] if len(sys.argv) > 1 else "001_foundation_schema.sql"
    print(f"Running migration: {migration}")
    run_migration(migration)
