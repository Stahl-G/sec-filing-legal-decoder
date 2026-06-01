"""Generate issue-level legal risk cards from routed filing paragraphs."""

from __future__ import annotations

from collections import defaultdict

from sec_filing_legal_decoder.content_routing import ParagraphRoute, route_paragraphs
from sec_filing_legal_decoder.document_modes import detect_document_mode
from sec_filing_legal_decoder.schemas import (
    CoverageSummary,
    DocumentInfo,
    ParsedDocument,
    RiskCard,
    RiskCardReport,
    SourceExcerpt,
)
from sec_filing_legal_decoder.utils import split_paragraphs

from .card_templates import template_for
from .materiality_rules import (
    confidence_for,
    materiality_for,
    priority_for,
    reading_decision_for,
)
from .question_bank import QUESTION_BANK
from .risk_domain_classifier import detect_subdomains


MAX_CARDS = 12
MAX_EXCERPTS_PER_CARD = 5
PRIORITY_SORT = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Monitor": 4}


def generate_risk_card_report(document: ParsedDocument) -> RiskCardReport:
    """Generate a v0.2 risk-card report from a parsed document."""

    form_type, mode = detect_document_mode(document)
    paragraphs = split_paragraphs(document.content)
    routes = route_paragraphs(paragraphs, document.source_path, mode)
    cards = _generate_cards(routes)
    coverage = _coverage_summary(routes, cards)
    doc_info = DocumentInfo(
        title=document.title or "Untitled Filing Review",
        form_type=form_type,
        mode=mode,
        source_path=document.source_path,
        parser_backend=document.parser_backend,
    )

    return RiskCardReport(
        document=doc_info,
        coverage_summary=coverage,
        risk_cards=cards,
        escalation_matrix=_escalation_matrix(cards),
        management_follow_up=_management_follow_up(cards),
        disclosure_consistency_questions=_disclosure_consistency_questions(cards),
    )


def _generate_cards(routes: list[ParagraphRoute]) -> list[RiskCard]:
    grouped: dict[str, list[ParagraphRoute]] = defaultdict(list)
    for route in routes:
        if route.route_action != "analyze":
            continue
        for domain in route.risk_domains:
            grouped[domain].append(route)

    candidates: list[tuple[str, list[ParagraphRoute], str]] = []
    for domain, domain_routes in grouped.items():
        text = " ".join(route.text for route in domain_routes)
        priority = priority_for(domain, text, len(domain_routes))
        candidates.append((domain, domain_routes, priority))
    candidates.sort(key=lambda item: (PRIORITY_SORT.get(item[2], 9), item[1][0].paragraph_id, item[0]))

    cards: list[RiskCard] = []
    for index, (domain, domain_routes, priority) in enumerate(candidates[:MAX_CARDS], start=1):
        cards.append(_build_card(index, domain, domain_routes, priority))
    return cards


def _build_card(
    index: int,
    domain: str,
    routes: list[ParagraphRoute],
    priority: str,
) -> RiskCard:
    text = " ".join(route.text for route in routes)
    template = template_for(domain)
    subdomains = _subdomains(domain, routes)
    questions = QUESTION_BANK.get(domain, {})
    reading_decision = reading_decision_for(priority)
    source_excerpts = [
        SourceExcerpt(
            paragraph_id=route.paragraph_id,
            source_ref=route.source_ref,
            excerpt=_excerpt(route.text),
        )
        for route in routes[:MAX_EXCERPTS_PER_CARD]
    ]

    return RiskCard(
        card_id=f"RC-{index:03d}",
        title=template.title,
        risk_domain=domain,
        subdomains=subdomains,
        priority=priority,
        reading_decision=reading_decision,
        owners=template.owners,
        source_paragraphs=[route.paragraph_id for route in routes],
        plain_language_meaning=template.plain_language_meaning,
        why_finance_readers_should_care=template.why_finance_readers_should_care,
        legal_or_audit_relevance=template.legal_or_audit_relevance,
        financial_statement_linkage=template.financial_statement_linkage,
        disclosure_ir_relevance=template.disclosure_ir_relevance,
        boilerplate_or_material=materiality_for(text, priority),
        questions=questions,
        suggested_management_follow_up=template.suggested_management_follow_up,
        what_not_to_overstate=template.what_not_to_overstate,
        source_excerpts=source_excerpts,
        confidence=confidence_for(text, len(routes), len(subdomains)),
    )


def _subdomains(domain: str, routes: list[ParagraphRoute]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for route in routes:
        for subdomain in detect_subdomains(domain, route.text):
            if subdomain not in seen:
                seen.add(subdomain)
                result.append(subdomain)
    return result


def _coverage_summary(routes: list[ParagraphRoute], cards: list[RiskCard]) -> CoverageSummary:
    return CoverageSummary(
        paragraphs_total=len(routes),
        paragraphs_skipped_admin=sum(1 for route in routes if route.content_type == "filing_admin"),
        financial_kpi_routed_out=sum(1 for route in routes if route.content_type == "ordinary_financial_kpi"),
        business_update_routed_out=sum(1 for route in routes if route.content_type == "business_update"),
        risk_relevant_paragraphs=sum(1 for route in routes if route.route_action == "analyze"),
        risk_cards_generated=len(cards),
    )


def _escalation_matrix(cards: list[RiskCard]) -> list[dict[str, object]]:
    matrix: list[dict[str, object]] = []
    for card in cards:
        first_questions = []
        for questions in card.questions.values():
            first_questions.extend(questions[:1])
        matrix.append(
            {
                "risk_card": card.title,
                "card_id": card.card_id,
                "owners": card.owners,
                "priority": card.priority,
                "reading_decision": card.reading_decision,
                "why": card.legal_or_audit_relevance,
                "questions": first_questions[:4],
            }
        )
    return matrix


def _management_follow_up(cards: list[RiskCard]) -> list[str]:
    return [
        f"{card.card_id} {card.title}: {card.suggested_management_follow_up}"
        for card in cards
        if card.priority in {"Critical", "High", "Medium"}
    ]


def _disclosure_consistency_questions(cards: list[RiskCard]) -> list[str]:
    questions: list[str] = []
    for card in cards:
        questions.append(
            f"{card.card_id} {card.title}: Does management or IR wording preserve the filing's uncertainty, "
            "or does it turn a review item into a more certain conclusion than the source supports?"
        )
    return questions


def _excerpt(text: str, limit: int = 560) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."
