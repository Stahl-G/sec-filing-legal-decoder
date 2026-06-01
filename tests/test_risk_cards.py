from pathlib import Path

from sec_filing_legal_decoder.cli import main
from sec_filing_legal_decoder.content_routing import route_paragraphs
from sec_filing_legal_decoder.document_modes import detect_document_mode
from sec_filing_legal_decoder.risk_cards import generate_risk_card_report
from sec_filing_legal_decoder.schemas import ParsedDocument


def test_detects_earnings_release_6k():
    document = ParsedDocument(
        source_path="CSIQ 26Q1.html",
        content="Form 6-K Exhibit 99.1 Canadian Solar Reports First Quarter Results.",
        parser_backend="html",
        title="Form 6-K",
    )

    assert detect_document_mode(document) == ("6-K", "earnings_release_6k")


def test_router_routes_ordinary_finance_kpi_out():
    routes = route_paragraphs(
        [
            "Revenue increased 12% and gross margin improved due to higher shipment volume in the quarter.",
            "The company received an IEEPA tariff refund notice and continues to evaluate customs exposure.",
        ],
        "sample.htm",
        "earnings_release_6k",
    )

    assert routes[0].content_type == "ordinary_financial_kpi"
    assert routes[0].route_action == "route_out"
    assert routes[1].route_action == "analyze"
    assert "regulatory_trade_policy" in routes[1].risk_domains


def test_router_does_not_treat_guidance_kpi_as_disclosure_risk():
    routes = route_paragraphs(
        [
            "Net revenues were at the high end of guidance and shipments exceeded guidance for the quarter.",
            "This safe harbor statement includes forward-looking guidance assumptions that could materially differ.",
        ],
        "sample.htm",
        "earnings_release_6k",
    )

    assert routes[0].content_type == "ordinary_financial_kpi"
    assert routes[0].route_action == "route_out"
    assert routes[1].route_action == "analyze"
    assert routes[1].risk_domains == ["disclosure_ir_consistency"]


def test_risk_card_report_groups_issue_level_cards():
    document = ParsedDocument(
        source_path="toyo-20f.htm",
        content=(
            "Form 20-F Annual Report\n\n"
            "The auditor expressed substantial doubt about the company's ability to continue as a going concern.\n\n"
            "Related-party transactions with affiliates represented material sales and receivables.\n\n"
            "The company disclosed warrants, earnout shares, and convertible notes that may dilute shareholders.\n\n"
            "Revenue increased 12% and gross margin improved due to shipment growth."
        ),
        parser_backend="html",
        title="TOYO 20-F",
    )

    report = generate_risk_card_report(document)
    domains = {card.risk_domain for card in report.risk_cards}

    assert report.document.mode == "annual_report_20f"
    assert "audit_going_concern" in domains
    assert "related_party_governance" in domains
    assert "equity_dilution_control" in domains
    assert report.coverage_summary.financial_kpi_routed_out == 1
    assert all(4 not in card.source_paragraphs for card in report.risk_cards)
    assert all(card.source_excerpts for card in report.risk_cards)


def test_cli_risk_cards_writes_default_output_set(tmp_path: Path):
    input_path = tmp_path / "sample.htm"
    input_path.write_text(
        "<html><body><p>Form 20-F Annual Report</p>"
        "<p>Management identified a material weakness in internal control over financial reporting.</p>"
        "<p>Revenue increased 12% and gross margin improved.</p></body></html>",
        encoding="utf-8",
    )
    output_dir = tmp_path / "outputs"
    result = main(["risk-cards", str(input_path), "--output-dir", str(output_dir)])

    assert result == 0
    assert output_dir.joinpath("legal-risk-cards.md").exists()
    assert output_dir.joinpath("legal-risk-cards.json").exists()
    assert output_dir.joinpath("escalation-questions.md").exists()
    assert output_dir.joinpath("management-follow-up.md").exists()
    assert "Internal Control" in output_dir.joinpath("legal-risk-cards.md").read_text(encoding="utf-8")


def test_cli_review_overlay_writes_overlay(tmp_path: Path):
    input_path = tmp_path / "sample.htm"
    analysis_path = tmp_path / "analysis.md"
    input_path.write_text(
        "<html><body><p>Form 20-F Annual Report</p>"
        "<p>The company has received a subpoena in a patent litigation matter.</p></body></html>",
        encoding="utf-8",
    )
    analysis_path.write_text("The company reported revenue growth and margin expansion.", encoding="utf-8")
    output_dir = tmp_path / "overlay"

    result = main(
        [
            "review-overlay",
            str(input_path),
            "--analysis",
            str(analysis_path),
            "--output-dir",
            str(output_dir),
        ]
    )

    assert result == 0
    overlay = output_dir.joinpath("review-overlay.md").read_text(encoding="utf-8")
    assert "not_covered" in overlay
    assert output_dir.joinpath("review-overlay.json").exists()
