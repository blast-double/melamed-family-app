# Last Edited: 2026-03-27 10:00
"""Create an Asana project for tax document collection.

Reads the master checklist from config/tax_documents_master.yaml,
enriches tasks with portal URLs and click-paths from config/institution_portals.yaml,
and creates a project with sections organized by tax schedule.

Usage:
    python3 -m execution.tax.asana_tasks --year 2025
    python3 -m execution.tax.asana_tasks --year 2025 --dry-run
"""

import argparse
import os
from collections import defaultdict
from pathlib import Path

import yaml
from dotenv import load_dotenv

import asana

from execution.tax.models import InstitutionPortal, TaxConfig, TaxDocumentsMaster, TaxYearConfig

# Load env
_env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_env_path)

CONFIG_ROOT = Path(__file__).resolve().parents[2] / "config"
MASTER_PATH = CONFIG_ROOT / "tax_documents_master.yaml"
CONFIG_PATH = CONFIG_ROOT / "tax_config.yaml"
PORTALS_PATH = CONFIG_ROOT / "institution_portals.yaml"

WORKSPACE_GID = "1213815286778073"


def _get_api_client() -> asana.ApiClient:
    config = asana.Configuration()
    config.access_token = os.environ["ASANA_PAT"]
    return asana.ApiClient(config)


def _load_master() -> TaxDocumentsMaster:
    with open(MASTER_PATH) as f:
        data = yaml.safe_load(f)
    return TaxDocumentsMaster(**data)


def _load_config() -> TaxConfig:
    with open(CONFIG_PATH) as f:
        data = yaml.safe_load(f)
    if "tax_years" in data and data["tax_years"]:
        data["tax_years"] = {int(k): v for k, v in data["tax_years"].items()}
    return TaxConfig(**data)


def _load_portals() -> dict[str, InstitutionPortal]:
    """Load institution_portals.yaml. Returns {id: InstitutionPortal}."""
    if not PORTALS_PATH.exists():
        return {}
    with open(PORTALS_PATH) as f:
        data = yaml.safe_load(f) or {}
    return {k: InstitutionPortal(**v) for k, v in data.items() if isinstance(v, dict)}


def _render_portal_notes(portal: InstitutionPortal | None, institution: str) -> list[str]:
    """Render download instructions from portal data, or a generic fallback."""
    if portal and (portal.portal_url or portal.click_path):
        lines = []
        if portal.portal_url:
            lines.append(f"\n📥 Download: {portal.portal_url}")
        if portal.click_path:
            lines.append("Steps:")
            for i, step in enumerate(portal.click_path, 1):
                lines.append(f"  {i}. {step}")
        return lines
    return [f"Download from {institution}'s portal/tax center"]


def _resolve_due_date(typical_arrival: str, tax_year: int) -> str | None:
    """Convert 'Late Jan', 'Mid-Feb' etc. to an ISO date string for Asana."""
    filing_year = tax_year + 1
    mapping = {
        "Jan": f"{filing_year}-01-20",
        "Late Jan": f"{filing_year}-01-31",
        "Mid-Feb": f"{filing_year}-02-15",
        "Late Feb": f"{filing_year}-02-28",
        "Mar": f"{filing_year}-03-15",
    }
    return mapping.get(typical_arrival)


def _resolve_institution(name: str, year_config: TaxYearConfig) -> str:
    if name == "(employer)":
        return year_config.parameterized_institutions.employer_name or "Employer"
    if name == "(loan servicer)":
        return year_config.parameterized_institutions.loan_servicer_name or "Loan Servicer"
    return name


# Schedule display names for Asana sections
SCHEDULE_DISPLAY = {
    "Schedule E": "Schedule E — Rental & Passthrough Income",
    "Schedule D / Form 8949": "Schedule D — Capital Gains & Losses",
    "Schedule D + Schedule B": "Schedule D + B — Investments",
    "Schedule B": "Schedule B — Interest & Dividends",
    "Schedule C": "Schedule C — Business Income & Expenses",
    "Schedule C — Home Office": "Schedule C — Home Office",
    "Form 1040 — Wages": "Form 1040 — Wages",
    "Form 1040-ES / 540-ES": "Estimated Tax Payments",
    "Schedule E / Schedule C": "Schedule E / C — Income",
    "Reference only": "Reference Documents",
    "ACA compliance": "ACA Compliance",
}


def build_task_list(
    tax_year: int,
) -> dict[str, list[dict]]:
    """Build tasks grouped by schedule section.

    Returns: {"Schedule E — Rental...": [{"name": ..., "notes": ..., "due": ...}, ...]}
    """
    master = _load_master()
    config = _load_config()
    year_config = config.tax_years.get(tax_year, TaxYearConfig())
    portals = _load_portals()

    sections: dict[str, list[dict]] = defaultdict(list)

    # Institutional documents — always include all, mark inactive conditionals
    for spec in master.institutional:
        institution = _resolve_institution(spec.institution, year_config)
        section_name = SCHEDULE_DISPLAY.get(spec.tax_schedule, spec.tax_schedule)
        due_date = _resolve_due_date(spec.typical_arrival, tax_year)

        # Determine if this conditional item is active this year
        is_inactive = spec.conditional and not year_config.conditional_items.get(spec.id, False)

        notes_parts = [
            f"Form: {spec.form_number}",
            f"Source: {institution} — {spec.description}",
            f"Tax Schedule: {spec.tax_schedule}",
        ]
        if is_inactive:
            notes_parts.insert(0, f"⚠️ NOT EXPECTED THIS YEAR — {spec.condition}")
            notes_parts.append(f"\nIf this changes, uncheck this task and collect the document.")

        # Enriched portal instructions
        portal = portals.get(spec.id)
        notes_parts.extend(_render_portal_notes(portal, institution))
        notes_parts.append(f"\nDrop the file into tax_document_archive/{tax_year}/")

        task = {
            "name": f"Collect {institution} {spec.form_number}",
            "notes": "\n".join(notes_parts),
            "due_on": due_date,
            "completed": is_inactive,  # Pre-complete inactive conditional tasks
        }
        sections[section_name].append(task)

    # Self-prepared documents
    for spec in master.self_prepared:
        section_name = SCHEDULE_DISPLAY.get(spec.tax_schedule, spec.tax_schedule)
        # Self-prepared docs are due when Aaron starts assembling — use Apr 1 as target
        filing_year = tax_year + 1
        due_date = f"{filing_year}-04-01"

        monarch_portal = portals.get("monarch_money_export")

        notes_parts = [
            f"Document: {spec.name}",
            f"Tax Schedule: {spec.tax_schedule}",
            f"Format: {spec.format}",
            f"Source: {spec.source}",
        ]
        if spec.monarch_category:
            url = monarch_portal.portal_url if monarch_portal else "https://app.monarchmoney.com/transactions"
            notes_parts.append(f"\n📥 Export from Monarch: {url}")
            notes_parts.append(f"Steps:")
            notes_parts.append(f"  1. Log in to app.monarchmoney.com → Transactions")
            notes_parts.append(f"  2. Filter by category: \"{spec.monarch_category}\"")
            notes_parts.append(f"  3. Set date range: {tax_year}-01-01 to {tax_year}-12-31")
            notes_parts.append(f"  4. Click three-dot menu (upper right) → Export")
            notes_parts.append(f"  5. Select {spec.format} format and download")
        else:
            notes_parts.append(f"\nManual preparation required.")
        notes_parts.append(f"\nDrop the file into tax_document_archive/{tax_year}/")

        task = {
            "name": f"Prepare {spec.name}",
            "notes": "\n".join(notes_parts),
            "due_on": due_date,
        }
        sections[section_name].append(task)

    return dict(sections)


def create_asana_project(tax_year: int) -> str:
    """Create the Asana project with sections and tasks. Returns the project URL."""
    api_client = _get_api_client()
    projects_api = asana.ProjectsApi(api_client)
    sections_api = asana.SectionsApi(api_client)
    tasks_api = asana.TasksApi(api_client)

    # Create the project
    project_data = projects_api.create_project(
        body={
            "data": {
                "name": f"{tax_year} Tax Season",
                "workspace": WORKSPACE_GID,
                "notes": (
                    f"Personal tax document collection for {tax_year}.\n"
                    f"Generated by execution/tax/asana_tasks.py.\n\n"
                    f"Collect all institutional documents and Monarch exports,\n"
                    f"then drop them into tax_document_archive/{tax_year}/."
                ),
                "default_view": "list",
            }
        },
        opts={},
    )
    project_gid = project_data["gid"]
    project_url = f"https://app.asana.com/0/{project_gid}"
    print(f"  Created project: {tax_year} Tax Season ({project_url})")

    # Build the task list
    task_sections = build_task_list(tax_year)

    # Create sections and tasks
    task_count = 0
    for section_name, task_list in task_sections.items():
        section_data = sections_api.create_section_for_project(
            project_gid,
            {"body": {"data": {"name": section_name}}},
        )
        section_gid = section_data["gid"]
        print(f"  Created section: {section_name} ({len(task_list)} tasks)")

        for task_info in task_list:
            task_body = {
                "data": {
                    "name": task_info["name"],
                    "notes": task_info["notes"],
                    "projects": [project_gid],
                    "memberships": [{"project": project_gid, "section": section_gid}],
                    "completed": task_info.get("completed", False),
                }
            }
            if task_info.get("due_on"):
                task_body["data"]["due_on"] = task_info["due_on"]

            tasks_api.create_task(body=task_body, opts={})
            task_count += 1

    print(f"\n  Total: {task_count} tasks across {len(task_sections)} sections")
    return project_url


def dry_run(tax_year: int) -> None:
    """Print what would be created without hitting the API."""
    task_sections = build_task_list(tax_year)

    print(f"Project: {tax_year} Tax Season\n")
    total = 0
    for section_name, task_list in task_sections.items():
        print(f"  [{section_name}]")
        for task in task_list:
            due = f" (due {task['due_on']})" if task.get("due_on") else ""
            check = "✅" if task.get("completed") else "⬜"
            not_expected = " — not expected this year" if task.get("completed") else ""
            print(f"    {check} {task['name']}{due}{not_expected}")
            total += 1
        print()
    print(f"Total: {total} tasks across {len(task_sections)} sections")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Asana tax collection project")
    parser.add_argument("--year", type=int, required=True, help="Tax year")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating")
    args = parser.parse_args()

    if args.dry_run:
        dry_run(args.year)
    else:
        print(f"Creating Asana project for {args.year} tax season...\n")
        url = create_asana_project(args.year)
        print(f"\n  Project URL: {url}")


if __name__ == "__main__":
    main()
