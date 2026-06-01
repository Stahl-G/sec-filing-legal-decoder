from sec_filing_legal_decoder.risk_cards import generate_risk_card_report
from sec_filing_legal_decoder.schemas import ParsedDocument


def _document(text: str, title: str = "Sample Filing") -> ParsedDocument:
    return ParsedDocument(
        source_path="sample.htm",
        content=f"Form 20-F Annual Report\n\n{text}",
        parser_backend="html",
        title=title,
    )


def test_small_issuer_profile_escalates_going_concern_and_equity():
    report = generate_risk_card_report(
        _document(
            "The auditor expressed substantial doubt about the company's ability to continue as a going concern.\n\n"
            "The company has warrants, convertible notes, and earnout shares that may dilute shareholders."
        ),
        issuer_profile="small-issuer",
    )

    cards = {card.risk_domain: card for card in report.risk_cards}
    assert cards["audit_going_concern"].priority == "Critical"
    assert cards["audit_going_concern"].recommended_review_posture == "read-first"
    assert cards["equity_dilution_control"].priority == "High"
    assert cards["equity_dilution_control"].recommended_review_posture == "read-first"


def test_foreign_private_issuer_profile_flags_home_country_and_attestation():
    report = generate_risk_card_report(
        _document(
            "As a foreign private issuer, the company follows home-country governance practices.\n\n"
            "The company relies on an auditor attestation exemption for internal control over financial reporting."
        ),
        issuer_profile="foreign-private-issuer",
    )

    cards = {card.risk_domain: card for card in report.risk_cards}
    assert cards["management_board_governance"].priority == "High"
    assert cards["management_board_governance"].recommended_review_posture == "read-first"
    assert cards["internal_control_reporting"].priority in {"High", "Critical"}


def test_spac_profile_flags_sponsor_pipe_warrants_and_registration_rights():
    report = generate_risk_card_report(
        _document(
            "Sponsor arrangements, PIPE financing, registration rights, public warrants, earnout shares, redemption history, and lock-up agreements may affect ownership and liquidity."
        ),
        issuer_profile="spac-de-spac",
    )

    card = next(card for card in report.risk_cards if card.risk_domain == "equity_dilution_control")
    assert card.priority == "High"
    assert card.recommended_review_posture == "read-first"


def test_manufacturing_profiles_raise_capacity_and_trade_policy_risk():
    manufacturing = generate_risk_card_report(
        _document(
            "The company entered into capacity commitments, purchase obligations, supplier concentration arrangements, and factory ramp commitments."
        ),
        issuer_profile="manufacturing",
    )
    solar = generate_risk_card_report(
        _document(
            "The company faces tariff, UFLPA, AD/CVD, ITC, IRA tax credit, customs, and forced labor compliance risks."
        ),
        issuer_profile="solar-manufacturing",
    )

    manufacturing_card = next(
        card for card in manufacturing.risk_cards if card.risk_domain == "guarantees_commitments"
    )
    solar_card = next(card for card in solar.risk_cards if card.risk_domain == "regulatory_trade_policy")
    assert manufacturing_card.priority == "High"
    assert manufacturing_card.recommended_review_posture == "read-first"
    assert solar_card.priority == "High"
    assert solar_card.recommended_review_posture == "read-first"
