# Last Edited: 2026-03-29 21:00
"""Fixture-based tests for the tax document rename pipeline.

Tests plan_renames() from execution.tax.rename_docs against real config/master
YAML files, with only the archive directory path monkeypatched to use tmp_path.
"""

import json

import pytest

from execution.tax import rename_docs
from execution.tax.rename_docs import plan_renames, rollback, _write_manifest

# ── Fixture file lists ────────────────────────────────────────────────────────

FILES_2024 = [
    "1098-2024.pdf",
    "2024 Non w2 Income + rent.pdf",
    "2024_MELAAAR_AARON D. MELAMED_GovernmentCopy_Individual.pdf",
    "Amex 2024 1099-INT.pdf",
    "Betterment - TaxStatement_2024_1099B_DIV_268011224580120.pdf",
    "Betterment - supplemental_tax_form_268011224580120_2024.pdf",
    "Coinbase 1099.pdf",
    "Expenses.pdf",
    "Gain Loss Coinbase.pdf",
    "Goldman Sachs 2024 1099-INT.pdf",
    "JustWorks 2024 W-2.pdf",
    "Orum 1095-C Health Ins Coverage.pdf",
    "PROPAY 2024 1099-K.pdf",
    "SOL Transcations.pdf",
    "Schwab 1099 Composite and Year-End Summary - 2024_2025-02-07_117.PDF",
    "Schwab Bank 1099 Tax Forms_2025-01-24_145.PDF",
    "TaxStatement_2024_FMV_268011225343197.pdf",
]

FILES_2025 = [
    "1098-2025.pdf",
    "1099 Composite and Year-End Summary - 2025_2026-01-23_117.PDF",
    "AMEX Savings 2025 INT.pdf",
    "TaxStatement_2025_1099B_DIV_268011224580120.pdf",
    "TaxStatement_2025_FMV_268011224573349.pdf",
    "TaxStatement_2025_FMV_268011225343197.pdf",
    "Tax_1099INT_2025_8823_1518407_1405266.PDF",
    "Transactions_2026-03-27T10-19-29.csv",
    "supplemental_tax_form_268011224580120_2025.pdf",
]


# ── Helpers ───────────────────────────────────────────────────────────────────


def _create_archive(tmp_path, year: int, filenames: list[str]):
    """Create a fake archive directory with empty files."""
    archive_dir = tmp_path / str(year)
    archive_dir.mkdir(parents=True, exist_ok=True)
    for name in filenames:
        (archive_dir / name).touch()
    return archive_dir


def _patch_archive_base(monkeypatch, tmp_path):
    """Point ARCHIVE_BASE at the tmp_path so plan_renames reads our fixtures."""
    monkeypatch.setattr(rename_docs, "ARCHIVE_BASE", tmp_path)


# ── 2024 Tests ────────────────────────────────────────────────────────────────


class Test2024:
    """Tests for the 2024 tax year archive."""

    def test_2024_all_files_mapped(self, tmp_path, monkeypatch):
        """All 17 files in the 2024 archive get a rename plan entry.

        Expects: 17 renames, 0 unmatched, 0 multi-match.
        """
        _create_archive(tmp_path, 2024, FILES_2024)
        _patch_archive_base(monkeypatch, tmp_path)

        renames, skipped_multi, skipped_none = plan_renames(2024)

        assert len(renames) == 17, (
            f"Expected 17 renames but got {len(renames)}. "
            f"Multi-match: {skipped_multi}, Unmatched: {skipped_none}"
        )
        assert len(skipped_multi) == 0, f"Unexpected multi-matches: {skipped_multi}"
        assert len(skipped_none) == 0, f"Unexpected unmatched files: {skipped_none}"

    def test_2024_canonical_names_correct(self, tmp_path, monkeypatch):
        """Spot-check that key 2024 files get the right canonical names."""
        _create_archive(tmp_path, 2024, FILES_2024)
        _patch_archive_base(monkeypatch, tmp_path)

        renames, _, _ = plan_renames(2024)
        rename_map = {orig: target for orig, target, _ in renames}

        # W-2 (parameterized employer = JustWorks)
        assert rename_map.get("JustWorks 2024 W-2.pdf") == "2024_justworks_w-2.pdf"

        # Mortgage 1098 (parameterized servicer = New American Funding)
        assert rename_map.get("1098-2024.pdf") == "2024_new-american-funding_1098.pdf"

        # Schwab brokerage composite
        assert rename_map.get(
            "Schwab 1099 Composite and Year-End Summary - 2024_2025-02-07_117.PDF"
        ) == "2024_schwab_1099-composite.pdf"

        # Goldman Sachs Marcus 1099-INT
        assert rename_map.get(
            "Goldman Sachs 2024 1099-INT.pdf"
        ) == "2024_goldman-sachs-marcus_1099-int.pdf"

        # Filed return (reference doc)
        assert rename_map.get(
            "2024_MELAAAR_AARON D. MELAMED_GovernmentCopy_Individual.pdf"
        ) == "2024_ref_filed-return.pdf"

    def test_2024_single_fmv_no_suffix(self, tmp_path, monkeypatch):
        """With only one FMV file in 2024, no account suffix is appended."""
        _create_archive(tmp_path, 2024, FILES_2024)
        _patch_archive_base(monkeypatch, tmp_path)

        renames, _, _ = plan_renames(2024)
        rename_map = {orig: target for orig, target, _ in renames}

        fmv_target = rename_map.get("TaxStatement_2024_FMV_268011225343197.pdf")
        assert fmv_target == "2024_betterment_5498-fmv.pdf", (
            f"Single FMV should not have suffix, got: {fmv_target}"
        )


# ── 2025 Tests ────────────────────────────────────────────────────────────────


class Test2025:
    """Tests for the 2025 tax year archive."""

    def test_2025_multi_account_fmv(self, tmp_path, monkeypatch):
        """Two Betterment FMV files get disambiguated with account suffixes.

        Account 268011224573349 -> _73349 suffix
        Account 268011225343197 -> _43197 suffix
        """
        _create_archive(tmp_path, 2025, FILES_2025)
        _patch_archive_base(monkeypatch, tmp_path)

        renames, skipped_multi, skipped_none = plan_renames(2025)
        rename_map = {orig: target for orig, target, _ in renames}

        fmv_73349 = rename_map.get("TaxStatement_2025_FMV_268011224573349.pdf")
        fmv_43197 = rename_map.get("TaxStatement_2025_FMV_268011225343197.pdf")

        assert fmv_73349 == "2025_betterment_5498-fmv_73349.pdf", (
            f"Expected _73349 suffix, got: {fmv_73349}"
        )
        assert fmv_43197 == "2025_betterment_5498-fmv_43197.pdf", (
            f"Expected _43197 suffix, got: {fmv_43197}"
        )

    def test_2025_amex_pattern(self, tmp_path, monkeypatch):
        """'AMEX Savings 2025 INT.pdf' matches amex_1099int spec."""
        _create_archive(tmp_path, 2025, FILES_2025)
        _patch_archive_base(monkeypatch, tmp_path)

        renames, _, _ = plan_renames(2025)
        rename_map = {orig: target for orig, target, _ in renames}

        amex_target = rename_map.get("AMEX Savings 2025 INT.pdf")
        assert amex_target == "2025_american-express_1099-int.pdf", (
            f"AMEX Savings should match amex_1099int, got: {amex_target}"
        )

    def test_2025_goldman_sachs_pattern(self, tmp_path, monkeypatch):
        """Goldman Sachs Tax_1099INT pattern matches marcus_1099int spec."""
        _create_archive(tmp_path, 2025, FILES_2025)
        _patch_archive_base(monkeypatch, tmp_path)

        renames, _, _ = plan_renames(2025)
        rename_map = {orig: target for orig, target, _ in renames}

        gs_target = rename_map.get(
            "Tax_1099INT_2025_8823_1518407_1405266.PDF"
        )
        assert gs_target == "2025_goldman-sachs-marcus_1099-int.pdf", (
            f"Tax_1099INT should match marcus_1099int, got: {gs_target}"
        )

    def test_2025_schwab_composite(self, tmp_path, monkeypatch):
        """Schwab composite without 'Schwab' prefix still matches via pattern."""
        _create_archive(tmp_path, 2025, FILES_2025)
        _patch_archive_base(monkeypatch, tmp_path)

        renames, _, _ = plan_renames(2025)
        rename_map = {orig: target for orig, target, _ in renames}

        schwab_target = rename_map.get(
            "1099 Composite and Year-End Summary - 2025_2026-01-23_117.PDF"
        )
        assert schwab_target == "2025_schwab_1099-composite.pdf", (
            f"Expected schwab composite match, got: {schwab_target}"
        )


# ── Edge Case Tests ───────────────────────────────────────────────────────────


class TestEdgeCases:
    """Tests for unmatched files, extension handling, and empty archives."""

    def test_unmatched_csv(self, tmp_path, monkeypatch):
        """Transactions CSV with future-year timestamp ends up in skipped_none."""
        _create_archive(tmp_path, 2025, FILES_2025)
        _patch_archive_base(monkeypatch, tmp_path)

        _, _, skipped_none = plan_renames(2025)

        assert "Transactions_2026-03-27T10-19-29.csv" in skipped_none, (
            f"Expected Transactions CSV in skipped_none, got: {skipped_none}"
        )

    def test_self_prepared_extension(self, tmp_path, monkeypatch):
        """Self-prepared docs get their extension from the source file, not the spec."""
        _create_archive(tmp_path, 2024, FILES_2024)
        _patch_archive_base(monkeypatch, tmp_path)

        renames, _, _ = plan_renames(2024)
        rename_map = {orig: target for orig, target, _ in renames}

        # Expenses.pdf is self-prepared (expense_summary), should keep .pdf
        expenses_target = rename_map.get("Expenses.pdf")
        assert expenses_target is not None, "Expenses.pdf should be in renames"
        assert expenses_target.endswith(".pdf"), (
            f"Self-prepared PDF should keep .pdf extension, got: {expenses_target}"
        )

        # Non-W2 Income is self-prepared, should keep .pdf
        non_w2_target = rename_map.get("2024 Non w2 Income + rent.pdf")
        assert non_w2_target is not None, "Non w2 Income should be in renames"
        assert non_w2_target.endswith(".pdf"), (
            f"Self-prepared PDF should keep .pdf extension, got: {non_w2_target}"
        )

    def test_empty_archive(self, tmp_path, monkeypatch):
        """Empty archive directory produces no renames and no errors."""
        _create_archive(tmp_path, 2024, [])
        _patch_archive_base(monkeypatch, tmp_path)

        renames, skipped_multi, skipped_none = plan_renames(2024)

        assert renames == []
        assert skipped_multi == []
        assert skipped_none == []

    def test_nonexistent_archive(self, tmp_path, monkeypatch):
        """Missing archive directory returns empty results (no crash)."""
        _patch_archive_base(monkeypatch, tmp_path)
        # Don't create the directory at all

        renames, skipped_multi, skipped_none = plan_renames(2024)

        assert renames == []
        assert skipped_multi == []
        assert skipped_none == []

    def test_hidden_files_ignored(self, tmp_path, monkeypatch):
        """Hidden files (dotfiles) are not processed."""
        archive_dir = _create_archive(tmp_path, 2024, FILES_2024)
        (archive_dir / ".DS_Store").touch()
        (archive_dir / ".rename_manifest.json").touch()
        _patch_archive_base(monkeypatch, tmp_path)

        renames, skipped_multi, skipped_none = plan_renames(2024)

        all_originals = [orig for orig, _, _ in renames] + skipped_multi + skipped_none
        assert ".DS_Store" not in all_originals
        assert ".rename_manifest.json" not in all_originals


# ── Rollback Tests ────────────────────────────────────────────────────────────


class TestRollback:
    """Tests for the rollback manifest and rollback execution."""

    def test_rollback_manifest_written(self, tmp_path, monkeypatch):
        """Applying renames writes a rollback manifest with correct structure."""
        archive_dir = _create_archive(tmp_path, 2024, FILES_2024)
        _patch_archive_base(monkeypatch, tmp_path)

        renames, _, _ = plan_renames(2024)
        manifest_path = _write_manifest(archive_dir, renames)

        assert manifest_path.exists(), "Manifest file should be written"
        assert manifest_path.name == ".rename_manifest.json"

        with open(manifest_path) as f:
            manifest = json.load(f)

        # Manifest maps target -> original (for reversal)
        assert len(manifest) == len(renames)
        for orig, target, _ in renames:
            assert target in manifest, f"Manifest missing target: {target}"
            assert manifest[target] == orig, (
                f"Manifest[{target}] should be {orig}, got {manifest[target]}"
            )

    def test_rollback_reverses_renames(self, tmp_path, monkeypatch):
        """Rollback restores original filenames and deletes the manifest."""
        archive_dir = _create_archive(tmp_path, 2025, FILES_2025)
        _patch_archive_base(monkeypatch, tmp_path)

        renames, _, _ = plan_renames(2025)

        # Write manifest and perform the renames (simulate --apply)
        _write_manifest(archive_dir, renames)
        for orig, target, _ in renames:
            (archive_dir / orig).rename(archive_dir / target)

        # Verify files were renamed
        for _, target, _ in renames:
            assert (archive_dir / target).exists(), f"Renamed file missing: {target}"

        # Now rollback
        rollback(2025)

        # Verify originals are restored
        for orig, target, _ in renames:
            assert (archive_dir / orig).exists(), (
                f"Original not restored: {orig}"
            )
            assert not (archive_dir / target).exists(), (
                f"Renamed file still exists after rollback: {target}"
            )

        # Manifest should be deleted
        assert not (archive_dir / ".rename_manifest.json").exists(), (
            "Manifest should be deleted after rollback"
        )

    def test_rollback_no_manifest(self, tmp_path, monkeypatch, capsys):
        """Rollback with no manifest prints a message and does not crash."""
        _create_archive(tmp_path, 2025, [])
        _patch_archive_base(monkeypatch, tmp_path)

        rollback(2025)

        captured = capsys.readouterr()
        assert "No rollback manifest found" in captured.out
