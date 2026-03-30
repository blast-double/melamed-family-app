# Last Edited: 2026-03-26 12:00
"""Seed the family Supabase database with entities, tags, and 2024 expected documents."""

from execution.db.client import get_client


def seed_entities(client) -> dict[str, str]:
    """Insert all entities. Returns {name: id} mapping for FK references."""
    entities = [
        {"type": "person", "name": "Aaron Melamed", "relationship": "self", "is_family": True,
         "metadata": {"nationality": "US"}},
        {"type": "person", "name": "Eugenia Guadalupe Canul Celis", "relationship": "spouse", "is_family": True,
         "metadata": {"nationality": "Mexican"}},
        {"type": "business", "name": "Itero", "relationship": "owned_business", "is_family": False,
         "metadata": {"entity_type": "s-corp", "workspace_path": "Itero/"}},
        {"type": "business", "name": "Keynote Capital, LLC", "relationship": "owned_business", "is_family": False,
         "metadata": {"entity_type": "llc"}},
        {"type": "business", "name": "Homeowners First, LLC", "relationship": "owned_business", "is_family": False,
         "metadata": {"entity_type": "llc"}},
        {"type": "business", "name": "Palisades Labs", "relationship": "owned_business", "is_family": False,
         "metadata": {"entity_type": "llc", "workspace_path": "Palisades Labs/"}},
        {"type": "institution", "name": "Schwab", "relationship": "brokerage", "is_family": False,
         "metadata": {"institution_type": "brokerage"}},
        {"type": "institution", "name": "Betterment", "relationship": "investment", "is_family": False,
         "metadata": {"institution_type": "robo-advisor"}},
        {"type": "institution", "name": "Guideline", "relationship": "retirement_401k", "is_family": False,
         "metadata": {"institution_type": "retirement"}},
        {"type": "institution", "name": "Goldman Sachs Marcus", "relationship": "savings", "is_family": False,
         "metadata": {"institution_type": "savings"}},
        {"type": "institution", "name": "American Express", "relationship": "banking", "is_family": False,
         "metadata": {"institution_type": "banking"}},
        {"type": "institution", "name": "Wells Fargo", "relationship": "banking", "is_family": False,
         "metadata": {"institution_type": "banking"}},
        {"type": "institution", "name": "Coinbase", "relationship": "crypto", "is_family": False,
         "metadata": {"institution_type": "crypto_exchange"}},
        {"type": "institution", "name": "ProPay", "relationship": "payment_processor", "is_family": False,
         "metadata": {"institution_type": "payment_processor"}},
        {"type": "institution", "name": "New American Funding", "relationship": "mortgage_servicer", "is_family": False,
         "metadata": {"institution_type": "mortgage"}},
        {"type": "institution", "name": "JustWorks", "relationship": "payroll", "is_family": False,
         "metadata": {"institution_type": "payroll"}},
        {"type": "institution", "name": "State Street", "relationship": "retirement", "is_family": False,
         "metadata": {"institution_type": "retirement"}},
        {"type": "institution", "name": "T-Mobile", "relationship": "telecom", "is_family": False,
         "metadata": {"institution_type": "telecom"}},
        {"type": "property", "name": "1771 11th Ave, SF", "relationship": "rental_property", "is_family": False,
         "metadata": {"property_type": "residential", "address": "1771 11th Ave, San Francisco, CA"}},
    ]

    result = client.table("entities").upsert(entities, on_conflict="name").execute()
    return {row["name"]: row["id"] for row in result.data}


def seed_tags(client) -> dict[str, str]:
    """Insert all tags. Returns {name: id} mapping."""
    tags = [
        {"name": "schedule-a", "display_name": "Schedule A (Itemized Deductions)", "type": "tax_category"},
        {"name": "schedule-b", "display_name": "Schedule B (Interest & Dividends)", "type": "tax_category"},
        {"name": "schedule-c", "display_name": "Schedule C (Business Income)", "type": "tax_category"},
        {"name": "schedule-d", "display_name": "Schedule D (Capital Gains)", "type": "tax_category"},
        {"name": "schedule-e", "display_name": "Schedule E (Rental/Passthrough)", "type": "tax_category"},
        {"name": "schedule-se", "display_name": "Schedule SE (Self-Employment Tax)", "type": "tax_category"},
        {"name": "form-8949", "display_name": "Form 8949 (Sales of Capital Assets)", "type": "tax_category"},
        {"name": "deductible", "display_name": "Deductible Expense", "type": "expense_category"},
        {"name": "home-office", "display_name": "Home Office", "type": "expense_category"},
        {"name": "rental-expense", "display_name": "Rental Property Expense", "type": "expense_category"},
        {"name": "tax-2023", "display_name": "Tax Year 2023", "type": "tax_year"},
        {"name": "tax-2024", "display_name": "Tax Year 2024", "type": "tax_year"},
        {"name": "tax-2025", "display_name": "Tax Year 2025", "type": "tax_year"},
        {"name": "green-card", "display_name": "Green Card", "type": "initiative"},
    ]

    result = client.table("tags").upsert(tags, on_conflict="name").execute()
    return {row["name"]: row["id"] for row in result.data}


def seed_documents_2024(client, entity_map: dict[str, str]) -> list[dict]:
    """Insert 2024 expected tax documents. Returns inserted rows."""
    aaron_id = entity_map["Aaron Melamed"]

    doc_specs = [
        ("2024 JustWorks W-2", "W-2", "JustWorks", "Schedule C",
         {"conditional": True, "condition": "only if employed that year"}),
        ("2024 Schwab 1099-Composite", "1099-Composite", "Schwab", "Schedule D", {}),
        ("2024 Betterment 1099-B/DIV", "1099-B", "Betterment", "Schedule D", {}),
        ("2024 Betterment FMV Statement", "FMV", "Betterment", "Schedule D", {}),
        ("2024 Guideline 401k Statement", "Year-End Statement", "Guideline", None, {}),
        ("2024 State Street 1099-R", "1099-R", "State Street", None,
         {"conditional": True, "condition": "only if distribution taken"}),
        ("2024 Marcus 1099-INT", "1099-INT", "Goldman Sachs Marcus", "Schedule B", {}),
        ("2024 Amex 1099-INT", "1099-INT", "American Express", "Schedule B", {}),
        ("2024 Schwab 1099-INT", "1099-INT", "Schwab", "Schedule B", {}),
        ("2024 Wells Fargo 1099-INT", "1099-INT", "Wells Fargo", "Schedule B",
         {"conditional": True, "condition": "only if account active"}),
        ("2024 Mortgage 1098", "1098", "New American Funding", "Schedule A", {}),
        ("2024 ProPay 1099-K", "1099-K", "ProPay", "Schedule E", {}),
        ("2024 Health Insurance 1095", "1095-C", None, None,
         {"conditional": True, "condition": "varies by year and employer"}),
        ("2024 Coinbase 1099", "1099", "Coinbase", "Schedule D",
         {"conditional": True, "condition": "only if trades that year"}),
        ("2024 Rental Income Summary", "CSV", None, "Schedule E", {"self_prepared": True}),
        ("2024 Rental Expenses", "CSV", None, "Schedule E", {"self_prepared": True}),
        ("2024 Home Office Rent Allocation", "CSV", None, "Schedule C", {"self_prepared": True}),
        ("2024 Business Meals", "CSV", None, "Schedule C", {"self_prepared": True}),
        ("2024 Dues & Subscriptions", "CSV", None, "Schedule C", {"self_prepared": True}),
        ("2024 Credit Card Annual Fees", "CSV", None, "Schedule C", {"self_prepared": True}),
        ("2024 Cell Phone Expenses", "CSV", None, "Schedule C", {"self_prepared": True}),
        ("2024 Office Supplies", "CSV", None, "Schedule C", {"self_prepared": True}),
        ("2024 Utilities (Home Office)", "CSV", None, "Schedule C", {"self_prepared": True}),
    ]

    documents = []
    for name, form_number, source_name, tax_schedule, metadata in doc_specs:
        source_id = entity_map.get(source_name) if source_name else aaron_id
        doc = {
            "name": name,
            "type": "tax_form",
            "source_entity_id": source_id,
            "owner_entity_id": aaron_id,
            "tax_year": 2024,
            "tax_schedule": tax_schedule,
            "form_number": form_number,
            "status": "expected",
            "metadata": metadata,
        }
        documents.append(doc)

    result = client.table("documents").upsert(documents, on_conflict="name").execute()
    return result.data


def run_seed():
    """Run the full seed process."""
    client = get_client()

    print("Seeding entities...")
    entity_map = seed_entities(client)
    print(f"  {len(entity_map)} entities seeded.")

    print("Seeding tags...")
    tag_map = seed_tags(client)
    print(f"  {len(tag_map)} tags seeded.")

    print("Seeding 2024 expected documents...")
    docs = seed_documents_2024(client, entity_map)
    print(f"  {len(docs)} documents seeded.")

    print("Seed complete.")
    return entity_map, tag_map, docs


if __name__ == "__main__":
    run_seed()
