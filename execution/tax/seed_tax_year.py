# Last Edited: 2026-03-26 16:00
"""Seed expected tax documents for any tax year into Supabase.

Reads the master checklist from config/tax_documents_master.yaml and
per-year config from config/tax_config.yaml. Replaces the hardcoded
seed_documents_2024() in execution/db/seed.py.

Usage:
    python3 -m execution.tax.seed_tax_year --year 2024
    python3 -m execution.tax.seed_tax_year --year 2025
"""

import argparse
from pathlib import Path

import yaml

from execution.db.client import get_client
from execution.tax.models import (
    TaxConfig,
    TaxDocumentsMaster,
    TaxYearConfig,
)

CONFIG_ROOT = Path(__file__).resolve().parents[2] / "config"
MASTER_PATH = CONFIG_ROOT / "tax_documents_master.yaml"
CONFIG_PATH = CONFIG_ROOT / "tax_config.yaml"


def load_master() -> TaxDocumentsMaster:
    """Load and validate tax_documents_master.yaml."""
    with open(MASTER_PATH) as f:
        data = yaml.safe_load(f)
    return TaxDocumentsMaster(**data)


def load_config() -> TaxConfig:
    """Load and validate tax_config.yaml."""
    with open(CONFIG_PATH) as f:
        data = yaml.safe_load(f)
    # YAML keys are ints but Pydantic expects str keys for dict — convert
    if "tax_years" in data and data["tax_years"]:
        data["tax_years"] = {int(k): v for k, v in data["tax_years"].items()}
    return TaxConfig(**data)


def resolve_institution_name(
    institution: str,
    year_config: TaxYearConfig,
) -> str:
    """Replace parameterized institution names with actual values."""
    if institution == "(employer)":
        return year_config.parameterized_institutions.employer_name or "(employer)"
    if institution == "(loan servicer)":
        return year_config.parameterized_institutions.loan_servicer_name or "(loan servicer)"
    return institution


def seed_tax_year(tax_year: int) -> int:
    """Seed all expected documents for a tax year. Returns count of documents seeded."""
    master = load_master()
    config = load_config()
    year_config = config.tax_years.get(tax_year, TaxYearConfig())

    client = get_client()

    # Look up Aaron's entity ID
    aaron_result = client.table("entities").select("id").eq("name", "Aaron Melamed").execute()
    if not aaron_result.data:
        raise RuntimeError("Aaron Melamed entity not found in DB. Run seed.py first.")
    aaron_id = aaron_result.data[0]["id"]

    # Build entity name -> ID map for source lookups
    entities_result = client.table("entities").select("id, name").execute()
    entity_map: dict[str, str] = {row["name"]: row["id"] for row in entities_result.data}

    documents: list[dict] = []

    # Institutional documents
    for spec in master.institutional:
        # Skip conditional items that are disabled for this year
        if spec.conditional:
            enabled = year_config.conditional_items.get(spec.id, False)
            if not enabled:
                continue

        institution_name = resolve_institution_name(spec.institution, year_config)
        entity_name = spec.entity_name
        if entity_name is None:
            # Parameterized — try to resolve from year config
            if spec.institution == "(employer)":
                entity_name = year_config.parameterized_institutions.employer_name
            elif spec.institution == "(loan servicer)":
                entity_name = year_config.parameterized_institutions.loan_servicer_name

        source_id = entity_map.get(entity_name) if entity_name else aaron_id

        doc = {
            "name": f"{tax_year} {institution_name} {spec.form_number}",
            "type": "tax_form",
            "source_entity_id": source_id or aaron_id,
            "owner_entity_id": aaron_id,
            "tax_year": tax_year,
            "tax_schedule": spec.tax_schedule,
            "form_number": spec.form_number,
            "status": "expected",
            "metadata": {
                "master_id": spec.id,
                "conditional": spec.conditional,
                "condition": spec.condition,
                "description": spec.description,
            },
        }
        documents.append(doc)

    # Self-prepared documents
    for spec in master.self_prepared:
        doc = {
            "name": f"{tax_year} {spec.name}",
            "type": "tax_form",
            "source_entity_id": aaron_id,
            "owner_entity_id": aaron_id,
            "tax_year": tax_year,
            "tax_schedule": spec.tax_schedule,
            "form_number": spec.format,
            "status": "expected",
            "metadata": {
                "master_id": spec.id,
                "self_prepared": True,
                "source": spec.source,
                "monarch_category": spec.monarch_category,
                "description": spec.description,
            },
        }
        documents.append(doc)

    if not documents:
        print(f"No documents to seed for {tax_year}.")
        return 0

    result = client.table("documents").upsert(documents, on_conflict="name").execute()
    return len(result.data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed tax documents for a given year")
    parser.add_argument("--year", type=int, required=True, help="Tax year to seed")
    args = parser.parse_args()

    print(f"Seeding expected documents for tax year {args.year}...")
    count = seed_tax_year(args.year)
    print(f"  {count} documents seeded.")


if __name__ == "__main__":
    main()
