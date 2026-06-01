"""Route filing paragraphs before generating v0.3 risk cards."""

from __future__ import annotations

from dataclasses import dataclass

from sec_filing_legal_decoder.risk_cards.risk_domain_classifier import classify_risk_domains
from sec_filing_legal_decoder.utils import source_ref

from .finance_kpi_rules import is_business_update, is_ordinary_financial_kpi
from .ignore_rules import is_filing_admin


@dataclass(frozen=True)
class ParagraphRoute:
    """A routed paragraph with enough context for card generation."""

    paragraph_id: int
    source_ref: str
    text: str
    content_type: str
    route_action: str
    reason: str
    risk_domains: list[str]


def route_paragraphs(
    paragraphs: list[str],
    source_path: str,
    document_mode: str,
) -> list[ParagraphRoute]:
    """Route paragraphs into skip, route-out, or risk-card analysis buckets."""

    return [
        route_paragraph(index, paragraph, source_path, document_mode)
        for index, paragraph in enumerate(paragraphs, start=1)
    ]


def route_paragraph(
    paragraph_id: int,
    paragraph: str,
    source_path: str,
    document_mode: str,
) -> ParagraphRoute:
    """Route one paragraph."""

    ref = source_ref(source_path, paragraph_id)
    if is_filing_admin(paragraph):
        return ParagraphRoute(
            paragraph_id=paragraph_id,
            source_ref=ref,
            text=paragraph,
            content_type="filing_admin",
            route_action="skip",
            reason="filing admin, cover/signature/index, or SEC boilerplate",
            risk_domains=[],
        )

    domains = classify_risk_domains(paragraph)
    if domains:
        filtered_domains = _mode_filtered_domains(domains, document_mode, paragraph)
        if not filtered_domains:
            return ParagraphRoute(
                paragraph_id=paragraph_id,
                source_ref=ref,
                text=paragraph,
                content_type="business_update",
                route_action="route_out",
                reason="earnings-release paragraph without a v0.3 legal-risk domain",
                risk_domains=[],
            )
        if (
            document_mode == "earnings_release_6k"
            and filtered_domains == ["disclosure_ir_consistency"]
            and is_ordinary_financial_kpi(paragraph)
            and not _has_disclosure_risk_trigger(paragraph)
        ):
            return ParagraphRoute(
                paragraph_id=paragraph_id,
                source_ref=ref,
                text=paragraph,
                content_type="ordinary_financial_kpi",
                route_action="route_out",
                reason="ordinary guidance-linked KPI without safe-harbor or disclosure-risk trigger",
                risk_domains=[],
            )
        return ParagraphRoute(
            paragraph_id=paragraph_id,
            source_ref=ref,
            text=paragraph,
            content_type="risk_candidate",
            route_action="analyze",
            reason="legal, regulatory, governance, audit, debt, dilution, disclosure, or contract risk language",
            risk_domains=filtered_domains,
        )

    if is_ordinary_financial_kpi(paragraph):
        return ParagraphRoute(
            paragraph_id=paragraph_id,
            source_ref=ref,
            text=paragraph,
            content_type="ordinary_financial_kpi",
            route_action="route_out",
            reason="ordinary revenue, margin, EPS, shipment, expense, or cash-flow KPI without legal-risk terms",
            risk_domains=[],
        )

    if document_mode == "earnings_release_6k" and is_business_update(paragraph):
        return ParagraphRoute(
            paragraph_id=paragraph_id,
            source_ref=ref,
            text=paragraph,
            content_type="business_update",
            route_action="route_out",
            reason="ordinary earnings-release business update without legal-risk terms",
            risk_domains=[],
        )

    return ParagraphRoute(
        paragraph_id=paragraph_id,
        source_ref=ref,
        text=paragraph,
        content_type="background",
        route_action="route_out",
        reason="no v0.3 legal-risk domain terms detected",
        risk_domains=[],
    )


def _mode_filtered_domains(domains: list[str], document_mode: str, paragraph: str) -> list[str]:
    """Keep 6-K earnings releases focused on risk terms rather than finance summary."""

    if document_mode != "earnings_release_6k":
        return domains
    if "safe harbor" in paragraph.lower():
        return ["disclosure_ir_consistency"]
    allowed = {
        "legal_proceedings_litigation",
        "regulatory_trade_policy",
        "management_board_governance",
        "debt_liquidity_covenant",
        "equity_dilution_control",
        "guarantees_commitments",
        "material_contracts",
        "disclosure_ir_consistency",
        "internal_control_reporting",
        "related_party_governance",
    }
    return [domain for domain in domains if domain in allowed]


def _has_disclosure_risk_trigger(paragraph: str) -> bool:
    text = paragraph.lower()
    triggers = (
        "safe harbor",
        "forward-looking",
        "materially differ",
        "cannot assure",
        "risk factor",
        "guidance assumes",
        "guidance is based",
        "subject to",
    )
    return any(trigger in text for trigger in triggers)
