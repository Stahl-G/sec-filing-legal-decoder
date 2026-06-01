from pathlib import Path

from sec_filing_legal_decoder.crosswalk import analyze_document
from sec_filing_legal_decoder.parser_backends.mock_backend import MockParserBackend
from sec_filing_legal_decoder.reports import render_json_report, render_markdown_report


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
