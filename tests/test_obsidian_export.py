from pathlib import Path

from sec_filing_legal_decoder.cli import main
from sec_filing_legal_decoder.crosswalk import analyze_document
from sec_filing_legal_decoder.obsidian import RiskCardObsidianOptions, export_risk_cards_to_obsidian
from sec_filing_legal_decoder.parser_backends.mock_backend import MockParserBackend
from sec_filing_legal_decoder.reports import ObsidianExportOptions, export_obsidian_vault
from sec_filing_legal_decoder.risk_cards import generate_risk_card_report
from sec_filing_legal_decoder.schemas import ParsedDocument


def test_obsidian_export_writes_linked_note_set(tmp_path: Path):
    report = analyze_document(MockParserBackend().parse(Path("mock.md")))
    written = export_obsidian_vault(
        report,
        ObsidianExportOptions(
            vault=tmp_path,
            folder="SEC Filings/TSLA/2025 10-K",
            company="Tesla, Inc.",
            ticker="TSLA",
            form="10-K",
            year="2025",
        ),
    )

    base = tmp_path / "SEC Filings" / "TSLA" / "2025 10-K"
    assert base.joinpath("00 Dashboard.md").exists()
    assert base.joinpath("02 Reading Decision Index.md").exists()
    assert base.joinpath("03 Escalation Matrix.md").exists()
    assert base.joinpath("data", "report.json").exists()
    assert base.joinpath("paragraphs").is_dir()
    assert written

    dashboard = base.joinpath("00 Dashboard.md").read_text(encoding="utf-8")
    assert "[[01 Executive Summary]]" in dashboard
    assert "Tesla, Inc." in dashboard
    assert "ESCALATE" in dashboard

    index = base.joinpath("02 Reading Decision Index.md").read_text(encoding="utf-8")
    assert "does not require the Dataview plugin" in index
    assert "[[paragraphs/" in index

    paragraph_notes = list(base.joinpath("paragraphs").glob("*.md"))
    assert paragraph_notes
    paragraph_text = paragraph_notes[-1].read_text(encoding="utf-8")
    assert "## Review Properties" in paragraph_text
    assert "> [!danger] Reading Decision" in paragraph_text
    assert "## Escalation Questions" in paragraph_text


def test_cli_analyze_obsidian_export(tmp_path: Path):
    input_path = tmp_path / "sample.htm"
    input_path.write_text(
        "<html><body><p>The company received a subpoena from the SEC and has accrued a liability of $4.2 million.</p></body></html>",
        encoding="utf-8",
    )
    vault = tmp_path / "vault"
    result = main(
        [
            "analyze",
            str(input_path),
            "--obsidian-vault",
            str(vault),
            "--obsidian-folder",
            "SEC Filings/TSLA/2025 10-K",
            "--company",
            "Tesla, Inc.",
            "--ticker",
            "TSLA",
            "--form",
            "10-K",
            "--year",
            "2025",
        ]
    )

    assert result == 0
    assert vault.joinpath("SEC Filings", "TSLA", "2025 10-K", "00 Dashboard.md").exists()


def test_risk_card_obsidian_export_writes_cards(tmp_path: Path):
    document = ParsedDocument(
        source_path="toyo-20f.htm",
        content=(
            "Form 20-F Annual Report\n\n"
            "The company disclosed UFLPA, AD/CVD, tariff, and ITC 337 patent litigation risk.\n\n"
            "The company has warrants and earnout shares that may dilute shareholders."
        ),
        parser_backend="html",
        title="TOYO 20-F",
    )
    report = generate_risk_card_report(document)
    written = export_risk_cards_to_obsidian(
        report,
        RiskCardObsidianOptions(
            output_dir=tmp_path / "obsidian",
            company="TOYO Co., Ltd.",
            ticker="TOYO",
            form="20-F",
            year="2025",
        ),
    )

    base = tmp_path / "obsidian"
    assert base.joinpath("00 Legal Risk Dashboard.md").exists()
    assert base.joinpath("01 Escalation Matrix.md").exists()
    assert base.joinpath("02 Management Follow-up.md").exists()
    assert base.joinpath("cards").is_dir()
    assert base.joinpath("data", "legal-risk-cards.json").exists()
    assert written

    card_text = next(base.joinpath("cards").glob("*.md")).read_text(encoding="utf-8")
    assert "risk_domain:" in card_text
    assert "priority:" in card_text
    assert "## Source Excerpts" in card_text
