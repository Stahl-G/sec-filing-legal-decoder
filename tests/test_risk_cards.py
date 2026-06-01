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
    assert all(card.evidence_quality in {"high", "medium", "low"} for card in report.risk_cards)
    assert all(card.issuer_specific_interpretation for card in report.risk_cards)


def test_nvidia_like_evidence_filtering_and_synthesis():
    document = ParsedDocument(
        source_path="nvda-10k.htm",
        content=(
            "Form 10-K Annual Report\n\n"
            "The Tax Identification Number (TIN), also known as an Employer Identification Number (EIN), is a unique 9-digit value assigned by the IRS.\n\n"
            "The aggregate market value of the voting and non-voting common equity held by non-affiliates was computed by reference to market price.\n\n"
            "We offer a limited warranty to end-users ranging from one to three years for products to repair or replace products for manufacturing defects.\n\n"
            "In fiscal year 2026, we entered into agreements to guarantee partners' facility lease obligations in the event of their default in exchange for warrants. "
            "The maximum gross exposure under all agreements is $3.5 billion, which is reduced as the partners make payments to the lessors over terms ranging from 5 to 7 years. "
            "The partners have placed $712 million in escrow to mitigate our potential exposure. "
            "The guarantees, classified as credit derivatives with changes in fair value recognized in Other income and expense, were not material.\n\n"
            "Groq In December 2025, we entered into a non-exclusive license agreement with Groq, Inc. for its language processing unit technology and hired certain Groq employees. "
            "No customer contracts, existing products, or equity interests were purchased. "
            "We recorded $14.4 billion of goodwill and a $2.5 billion developed technology intangible asset, valued using a cost-to-recreate methodology with a five-year useful life.\n\n"
            "As of January 25, 2026, there are no accrued contingent liabilities associated with the legal proceedings described above based on our belief that liabilities, while reasonably possible, are not probable. "
            "Further, any possible loss or range of loss in these matters cannot be reasonably estimated at this time.\n\n"
            "In fiscal year 2026, we released $711 million of valuation allowance on deferred tax assets based on more-likely-than-not future taxable income in certain jurisdictions, while other deferred tax assets remain subject to valuation allowance.\n\n"
            "Our Board of Directors oversees cybersecurity governance, incident response, vendor risk, and materiality assessment for cybersecurity incidents."
        ),
        parser_backend="html",
        title="NVIDIA 10-K",
    )

    report = generate_risk_card_report(document)
    domains = {card.risk_domain for card in report.risk_cards}
    all_sources = [excerpt.excerpt for card in report.risk_cards for excerpt in card.source_excerpts]

    assert "guarantees_commitments" in domains
    assert "material_contracts" in domains
    assert "legal_proceedings_litigation" in domains
    assert "tax_cross_border" in domains
    assert "cybersecurity_governance" in domains
    assert "debt_liquidity_covenant" not in domains
    assert "equity_dilution_control" not in domains
    assert "management_board_governance" not in domains
    assert "related_party_governance" not in domains
    assert not any("Tax Identification Number" in source for source in all_sources)
    assert not any("non-affiliates" in source for source in all_sources)

    guarantee_card = next(card for card in report.risk_cards if card.risk_domain == "guarantees_commitments")
    material_card = next(card for card in report.risk_cards if card.risk_domain == "material_contracts")
    litigation_card = next(card for card in report.risk_cards if card.risk_domain == "legal_proceedings_litigation")
    tax_card = next(card for card in report.risk_cards if card.risk_domain == "tax_cross_border")

    assert "$3.5 billion" in " ".join(guarantee_card.issuer_specific_facts)
    assert "$712 million" in " ".join(guarantee_card.issuer_specific_facts)
    assert "credit derivatives" in " ".join(guarantee_card.issuer_specific_facts)
    assert "$14.4 billion" in " ".join(material_card.issuer_specific_facts)
    assert "$2.5 billion" in " ".join(material_card.issuer_specific_facts)
    assert "reasonably possible" in " ".join(litigation_card.issuer_specific_facts)
    assert "$711 million" in " ".join(tax_card.issuer_specific_facts)
    assert all(card.financial_analysis_difference for card in report.risk_cards)
    assert [card.risk_domain for card in report.risk_cards if card.recommended_review_posture == "read-first"] == [
        "legal_proceedings_litigation",
        "material_contracts",
        "guarantees_commitments",
        "tax_cross_border",
        "cybersecurity_governance",
    ]


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
    assert output_dir.joinpath("legal-risk-review.md").exists()
    assert output_dir.joinpath("evidence-audit.md").exists()
    assert output_dir.joinpath("escalation-questions.md").exists()
    assert output_dir.joinpath("management-follow-up.md").exists()
    assert "Executive Takeaway" in output_dir.joinpath("legal-risk-review.md").read_text(encoding="utf-8")
    assert "Internal Control" in output_dir.joinpath("legal-risk-cards.md").read_text(encoding="utf-8")


def test_cli_risk_cards_supports_zh_cn_bilingual_output(tmp_path: Path):
    input_path = tmp_path / "sample.htm"
    input_path.write_text(
        "<html><body><p>Form 10-K Annual Report</p>"
        "<p>As of January 25, 2026, there are no accrued contingent liabilities associated with the legal proceedings described above because liabilities, while reasonably possible, are not probable.</p>"
        "<p>Groq In December 2025, we entered into a non-exclusive license agreement and recorded $14.4 billion of goodwill and a $2.5 billion developed technology intangible asset.</p>"
        "</body></html>",
        encoding="utf-8",
    )
    output_dir = tmp_path / "outputs"
    result = main(
        [
            "risk-cards",
            str(input_path),
            "--output-dir",
            str(output_dir),
            "--lang",
            "zh-CN",
            "--term-style",
            "bilingual",
        ]
    )

    assert result == 0
    review = output_dir.joinpath("legal-risk-review.md").read_text(encoding="utf-8")
    cards = output_dir.joinpath("legal-risk-cards.md").read_text(encoding="utf-8")
    assert "法律风险复核" in review
    assert "重点法务风险主题" in review
    assert "诉讼及法律程序（Legal Proceedings / Litigation）" in review
    assert "不宜过度表述" in cards
    assert "reasonably possible" in cards


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
