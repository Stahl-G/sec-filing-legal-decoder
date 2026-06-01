from pathlib import Path

from sec_filing_legal_decoder.crosswalk import analyze_document
from sec_filing_legal_decoder.parser_backends.mock_backend import MockParserBackend
from sec_filing_legal_decoder.reports import (
    render_evidence_audit_report,
    render_integrated_legal_risk_review,
    render_json_report,
    render_legal_risk_cards_report,
    render_markdown_report,
    render_risk_cards_json_report,
)
from sec_filing_legal_decoder.risk_cards import generate_risk_card_report


def test_markdown_report_contains_required_sections():
    document = MockParserBackend().parse(Path("missing.md"))
    report = analyze_document(document)
    markdown = render_markdown_report(report)
    assert markdown.startswith("---\n")
    assert "tags:" in markdown
    assert "> [!summary] Executive Summary" in markdown
    assert "## Priority Paragraphs" in markdown
    assert "> [!danger]" in markdown
    assert "Escalation Questions" in markdown
    assert "> [!caution] Disclaimer" in markdown


def test_json_report_contains_disclaimer():
    document = MockParserBackend().parse(Path("missing.md"))
    report = analyze_document(document)
    payload = render_json_report(report)
    assert "not legal advice" in payload
    assert "analyses" in payload


def test_legal_risk_cards_report_contains_cards_and_scope():
    document = MockParserBackend().parse(Path("missing.md"))
    report = generate_risk_card_report(document)
    markdown = render_legal_risk_cards_report(report)
    review = render_integrated_legal_risk_review(report)
    audit = render_evidence_audit_report(report)
    payload = render_risk_cards_json_report(report)

    assert markdown.startswith("---\n")
    assert "v0.4 Source-Only Scope" in markdown
    assert "## Risk Cards" in markdown
    assert "## Executive Takeaway" in review
    assert "## Evidence Audit" in audit or "# Evidence Audit" in audit
    assert "issuer_specific_interpretation" in payload
    assert "evidence_quality" in payload
    assert "source_excerpts" in payload
    assert "risk_cards" in payload
