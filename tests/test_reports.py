from pathlib import Path

from sec_filing_legal_decoder.crosswalk import analyze_document
from sec_filing_legal_decoder.parser_backends.mock_backend import MockParserBackend
from sec_filing_legal_decoder.reports import render_json_report, render_markdown_report


def test_markdown_report_contains_required_sections():
    document = MockParserBackend().parse(Path("missing.md"))
    report = analyze_document(document)
    markdown = render_markdown_report(report)
    assert "Reading decision" in markdown
    assert "Legal-to-Finance Notes" in markdown
    assert "Escalation questions" in markdown
    assert "Disclaimer" in markdown


def test_json_report_contains_disclaimer():
    document = MockParserBackend().parse(Path("missing.md"))
    report = analyze_document(document)
    payload = render_json_report(report)
    assert "not legal advice" in payload
    assert "analyses" in payload
