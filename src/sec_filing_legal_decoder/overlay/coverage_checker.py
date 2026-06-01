"""Compare risk-card coverage against an existing finance analysis."""

from __future__ import annotations

import re
from pathlib import Path

from sec_filing_legal_decoder.risk_cards import generate_risk_card_report
from sec_filing_legal_decoder.schemas import OverlayFinding, OverlayReport, ParsedDocument, RiskCard

from .analysis_reader import read_analysis


OVERLY_CERTAIN_PATTERNS: tuple[str, ...] = (
    r"\bresolved\b",
    r"\beliminates?\b",
    r"\bwill\b",
    r"\bguaranteed\b",
    r"\bno material risk\b",
    r"\bnot a risk\b",
    r"\bfully mitigated\b",
)


def build_overlay_report(document: ParsedDocument, analysis_path: Path) -> OverlayReport:
    """Build an overlay report using v0.3 risk cards as the review spine."""

    risk_report = generate_risk_card_report(document)
    analysis_text = read_analysis(analysis_path)
    findings = [_finding_for_card(card, analysis_text) for card in risk_report.risk_cards]
    return OverlayReport(
        document=risk_report.document,
        analysis_path=str(analysis_path),
        risk_card_report=risk_report,
        findings=findings,
    )


def _finding_for_card(card: RiskCard, analysis_text: str) -> OverlayFinding:
    lowered = analysis_text.lower()
    terms = _coverage_terms(card)
    matched_terms = [term for term in terms if term and term.lower() in lowered]
    has_overly_certain_language = any(
        re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in OVERLY_CERTAIN_PATTERNS
    )

    if not matched_terms:
        return OverlayFinding(
            risk_card_id=card.card_id,
            risk_card_title=card.title,
            status="not_covered",
            finding=(
                f"The existing analysis does not appear to discuss {card.title}. "
                "Consider adding legal, governance, audit, disclosure, or management follow-up context if material."
            ),
            suggested_safer_wording=_safer_wording(card),
        )
    if has_overly_certain_language:
        return OverlayFinding(
            risk_card_id=card.card_id,
            risk_card_title=card.title,
            status="needs_wording_review",
            finding=(
                f"The existing analysis mentions terms related to {card.title}, but may use language that sounds more certain "
                "than a filing triage note should support."
            ),
            suggested_safer_wording=_safer_wording(card),
        )
    if len(matched_terms) <= 2:
        return OverlayFinding(
            risk_card_id=card.card_id,
            risk_card_title=card.title,
            status="mentioned_but_under_explained",
            finding=(
                f"The existing analysis appears to mention {card.title}, but may not explain the legal, governance, audit, "
                "or disclosure meaning for finance readers."
            ),
            suggested_safer_wording=_safer_wording(card),
        )
    return OverlayFinding(
        risk_card_id=card.card_id,
        risk_card_title=card.title,
        status="covered_for_triage",
        finding=(
            f"The existing analysis appears to cover {card.title}. Confirm that it preserves uncertainty and includes "
            "role-specific follow-up where needed."
        ),
        suggested_safer_wording=_safer_wording(card),
    )


def _coverage_terms(card: RiskCard) -> list[str]:
    terms = [card.risk_domain.replace("_", " "), card.title.lower()]
    terms.extend(item.lower().replace("_", " ") for item in card.subdomains)
    for word in re.split(r"[^a-zA-Z0-9]+", card.title.lower()):
        if len(word) >= 5:
            terms.append(word)
    return list(dict.fromkeys(terms))


def _safer_wording(card: RiskCard) -> str:
    return (
        f"{card.title} should be described as a filing review item that may affect "
        "finance, disclosure, governance, or audit interpretation. Management should "
        "confirm the underlying facts and avoid treating the matter as resolved unless "
        "the filing and qualified reviewers support that conclusion."
    )
