# Last Edited: 2026-03-26 12:00
"""Supabase client module. Uses service_role key for backend/admin access."""

import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env from workspace root
_env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_env_path)

_SUPABASE_URL = os.environ["SUPABASE_PROJECT_URL"]
_SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]


def get_client() -> Client:
    """Return a Supabase client using the service_role key (bypasses RLS)."""
    return create_client(_SUPABASE_URL, _SUPABASE_KEY)


def get_database_url() -> str:
    """Return the PostgreSQL connection string, handling legacy env var name."""
    return os.environ.get("SUPABASE_DATABASE_URL") or os.environ["SUPABASE_DATA_STRING_CONNETION"]
