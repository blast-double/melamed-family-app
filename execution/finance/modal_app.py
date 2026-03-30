# Last Edited: 2026-03-29 22:00
"""Modal web endpoint for the transaction categorization engine.

Deploys execution/finance/categorize.py as a serverless HTTPS endpoint
so the tax-portal on Vercel can call it without needing a local Python process.

Usage:
    modal deploy execution/finance/modal_app.py     # deploy
    modal serve execution/finance/modal_app.py      # local dev

Endpoint:
    GET /categorize?year=2025  → JSON response
"""

import modal

app = modal.App("tax-categorize")

image = (
    modal.Image.debian_slim(python_version="3.13")
    .pip_install(
        "PyYAML>=6.0",
        "monarchmoney==0.1.15",
        "gql>=3.4,<4",
        "python-dotenv==1.2.2",
        "aiohttp>=3.13.0",
        "oathtool>=2.4.0",
        "fastapi[standard]",
    )
    .add_local_dir("execution/finance/", remote_path="/app/execution/finance/")
    .add_local_file("execution/__init__.py", remote_path="/app/execution/__init__.py")
    .add_local_dir("config/", remote_path="/app/config/")
)

# Persistent volume for session caching (avoids re-login on warm starts)
session_vol = modal.Volume.from_name("monarch-session", create_if_missing=True)


@app.function(
    image=image,
    secrets=[modal.Secret.from_name("monarch")],
    volumes={"/app/execution/.credentials": session_vol},
    timeout=120,
)
@modal.fastapi_endpoint(method="GET")
async def categorize(year: int = 2025):
    """Classify transactions for a tax year and return structured JSON."""
    import sys
    import os

    os.chdir("/app")
    if "/app" not in sys.path:
        sys.path.insert(0, "/app")

    from execution.finance.categorize import (
        run as categorize_run,
        build_json_output,
        load_schedule_rules,
        load_cpa_notes,
        load_manual_adjustments,
    )

    # Suppress stdout (json_mode=False) — we build the output ourselves
    classified = await categorize_run(year, json_mode=False)
    sched_rules = load_schedule_rules()
    cpa_notes = load_cpa_notes(sched_rules)
    manual_adj = load_manual_adjustments(sched_rules)
    result = build_json_output(classified, year, cpa_notes=cpa_notes, manual_adjustments=manual_adj)

    session_vol.commit()

    return result
