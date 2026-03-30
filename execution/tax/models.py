# Last Edited: 2026-03-29 21:00
"""Pydantic models for tax document management.

Used by: seed_tax_year.py, match_files.py, asana_tasks.py, extract_pdf.py,
         execution/finance/categorize.py, tax-portal.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# --- Master YAML models ---


class InstitutionalDocSpec(BaseModel):
    """One institutional document entry from tax_documents_master.yaml."""

    id: str
    institution: str
    description: str
    entity_name: str | None = None
    form_number: str
    tax_schedule: str
    typical_arrival: str
    conditional: bool = False
    condition: str | None = None
    download_url: str | None = None
    multi_account: bool = False
    account_pattern: str | None = None
    filename_patterns: list[str] = Field(default_factory=list)


class SelfPreparedDocSpec(BaseModel):
    """One self-prepared document entry from tax_documents_master.yaml."""

    id: str
    name: str
    description: str
    tax_schedule: str
    format: str
    source: str
    monarch_category: str | None = None
    filename_patterns: list[str] = Field(default_factory=list)


class ReferenceDocSpec(BaseModel):
    """One reference document entry from tax_documents_master.yaml.

    Reference docs are rename-only: not DB-tracked, not in gap reports.
    """

    id: str
    name: str
    description: str
    filename_patterns: list[str] = Field(default_factory=list)


class Deadline(BaseModel):
    """One deadline entry from tax_documents_master.yaml."""

    date: str
    description: str
    forms: list[str] = Field(default_factory=list)


class TaxDocumentsMaster(BaseModel):
    """Full parsed tax_documents_master.yaml."""

    institutional: list[InstitutionalDocSpec]
    self_prepared: list[SelfPreparedDocSpec]
    reference: list[ReferenceDocSpec] = Field(default_factory=list)
    deadlines: list[Deadline]


# --- Institution portal models ---


class InstitutionPortal(BaseModel):
    """Cached portal data for one institution, enriched by Tavily."""

    portal_url: str | None = None
    click_path: list[str] = Field(default_factory=list)
    expected_format: str | None = None
    last_verified: str | None = None


# --- Per-year config models ---


class ParameterizedInstitutions(BaseModel):
    """Actual names for parameterized institutions in a given year."""

    employer_name: str | None = None
    employer_1095c_name: str | None = None  # May differ from W-2 employer (PEO split)
    loan_servicer_name: str | None = None


class TaxYearConfig(BaseModel):
    """Per-year setup from tax_config.yaml."""

    initialized: bool = False
    parameterized_institutions: ParameterizedInstitutions = Field(
        default_factory=ParameterizedInstitutions
    )
    conditional_items: dict[str, bool] = Field(default_factory=dict)
    cpa_package_submitted: bool = False
    cpa_package_date: str | None = None


class TaxConfig(BaseModel):
    """Full parsed tax_config.yaml."""

    california_filing_status: Literal["resident", "nonresident", "undetermined"] = (
        "undetermined"
    )
    ca_status_notes: str = ""
    tax_years: dict[int, TaxYearConfig] = Field(default_factory=dict)


# --- File matching models ---


class MatchResult(BaseModel):
    """Result of matching one archive file to an expected document."""

    doc_id: str
    doc_name: str
    matched_file: str | None = None
    confidence: Literal["exact", "pattern", "none"] = "none"


# --- Data extraction models (subsystem 3) ---


class ExtractedField(BaseModel):
    """One field extracted from a tax form."""

    label: str
    value: str
    schedule_line: str | None = None  # e.g., "Schedule B, Part I, Line 1"


class ExtractedData(BaseModel):
    """Structured data extracted from a single tax document."""

    document_id: str
    form_type: str
    institution: str
    tax_year: int
    fields: list[ExtractedField]
    raw_text: str | None = None
    extracted_at: datetime = Field(default_factory=datetime.now)


# --- PDF identification models ---


class IdentificationResult(BaseModel):
    """Result of auto-identifying a tax PDF via OCR."""

    institution: str | None = None
    form_type: str | None = None
    tax_year: int | None = None
    account_number: str | None = None
    confidence: Literal["high", "medium", "low"] = "low"
    matched_spec_id: str | None = None


# --- PDF reconciliation models ---


class ReconciledField(BaseModel):
    """One field after dual-extraction reconciliation."""

    label: str
    value: str
    confidence: Literal["verified", "disputed", "single_source"]
    ocr_value: str | None = None
    vision_value: str | None = None
    schedule_line: str | None = None


class ReconciliationResult(BaseModel):
    """Result of comparing Google OCR vs Claude Vision extraction."""

    document_id: str
    form_type: str
    institution: str
    tax_year: int
    fields: list[ReconciledField]
    all_agreed: bool
    disputed_fields: list[str] = Field(default_factory=list)
    extracted_at: datetime = Field(default_factory=datetime.now)


# --- CPA cover document models ---


class CoverDocumentEntry(BaseModel):
    """One document listed in a cover section."""

    name: str
    form_number: str
    source: str
    file_path: str | None = None
    notes: str | None = None


class CoverSection(BaseModel):
    """One tax schedule section of the CPA summary."""

    schedule_name: str  # e.g., "Schedule E"
    schedule_display: str  # e.g., "Schedule E — Rental & Passthrough Income"
    documents: list[CoverDocumentEntry] = Field(default_factory=list)
    totals: dict[str, float] | None = None  # e.g., {"income": 124008.23}


class CoverDocument(BaseModel):
    """The full CPA package summary, organized by schedule."""

    tax_year: int
    generated_at: datetime = Field(default_factory=datetime.now)
    sections: list[CoverSection] = Field(default_factory=list)
    missing_items: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
