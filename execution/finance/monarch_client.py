# Last Edited: 2026-03-29 20:30
"""Monarch Money client — env-loading wrapper with session-first auth.

Auth strategy:
  1. Load saved session from disk and validate with a lightweight API call.
  2. If no session or session is stale, do a full login with MFA.
  3. On login failure (Monarch rate-limits aggressively), retry with backoff.
  4. Save session after every successful login so future calls skip auth.
"""

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from monarchmoney import MonarchMoney
from monarchmoney.monarchmoney import MonarchMoneyEndpoints

_env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_env_path)

# PyPI 0.1.15 hardcodes the old domain; Monarch migrated to api.monarch.com
# See: https://github.com/hammem/monarchmoney/issues/184
MonarchMoneyEndpoints.BASE_URL = "https://api.monarch.com"

_SESSION_FILE = Path(__file__).resolve().parent.parent / ".credentials" / "monarch_session"
# Fallback: MonarchMoney's default session path (created by standalone scripts)
_FALLBACK_SESSION = Path(__file__).resolve().parents[2] / ".mm" / "mm_session.pickle"

_LOGIN_RETRIES = 3
_LOGIN_BACKOFF_SECS = 5


async def get_client() -> MonarchMoney:
    """Return an authenticated MonarchMoney client.

    Session-first: loads saved session and validates with a lightweight call.
    Only performs a full login if no session exists or the session is stale.
    Retries login with backoff if Monarch rate-limits the attempt.
    """
    _SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    mm = MonarchMoney(session_file=str(_SESSION_FILE))
    mm._headers["User-Agent"] = "Mozilla/5.0"

    # Try saved session first — no login call
    for session_path in [_SESSION_FILE, _FALLBACK_SESSION]:
        if session_path.exists():
            try:
                mm = MonarchMoney(session_file=str(session_path))
                mm._headers["User-Agent"] = "Mozilla/5.0"
                mm.load_session()
                await mm.get_accounts()  # lightweight validation
                # If we loaded from fallback, copy to primary location
                if session_path != _SESSION_FILE:
                    import shutil
                    shutil.copy2(session_path, _SESSION_FILE)
                return mm
            except Exception:
                pass  # Session stale or corrupt — fall through to login

    # No valid session — full login with retry
    mm = MonarchMoney(session_file=str(_SESSION_FILE))
    mm._headers["User-Agent"] = "Mozilla/5.0"

    last_error = None
    for attempt in range(1, _LOGIN_RETRIES + 1):
        try:
            await mm.login(
                email=os.environ["MONARCH_EMAIL"],
                password=os.environ["MONARCH_PASSWORD"],
                mfa_secret_key=os.environ.get("MONARCH_MFA_SECRET_KEY"),
                use_saved_session=False,
            )
            mm.save_session()
            return mm
        except Exception as e:
            last_error = e
            if attempt < _LOGIN_RETRIES:
                wait = _LOGIN_BACKOFF_SECS * attempt
                print(f"[monarch] Login attempt {attempt} failed: {e}. Retrying in {wait}s...")
                await asyncio.sleep(wait)

    raise RuntimeError(
        f"Monarch login failed after {_LOGIN_RETRIES} attempts. "
        f"Last error: {last_error}. "
        f"Monarch rate-limits rapid login attempts — wait 2-3 minutes and retry."
    )
