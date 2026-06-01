"""Generate issue-level legal risk cards from routed filing paragraphs."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from sec_filing_legal_decoder.content_routing import ParagraphRoute, route_paragraphs
from sec_filing_legal_decoder.document_modes import detect_document_mode
from sec_filing_legal_decoder.evidence import EvidenceAssessment, assess_evidence, extract_issuer_facts
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


@dataclass(frozen=True)
class EvidenceRoute:
    """A routed paragraph plus its evidence assessment."""

    route: ParagraphRoute
    assessment: EvidenceAssessment


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

    candidates: list[tuple[str, list[EvidenceRoute], list[EvidenceRoute], str]] = []
    for domain, domain_routes in grouped.items():
        accepted, suppressed = _assess_domain_routes(domain, domain_routes)
        if not accepted:
            continue
        text = " ".join(item.route.text for item in accepted)
        priority = priority_for(domain, text, len(accepted))
        candidates.append((domain, accepted, suppressed, priority))
    candidates.sort(key=lambda item: (PRIORITY_SORT.get(item[3], 9), item[1][0].route.paragraph_id, item[0]))

    cards: list[RiskCard] = []
    for index, (domain, accepted, suppressed, priority) in enumerate(candidates[:MAX_CARDS], start=1):
        cards.append(_build_card(index, domain, accepted, suppressed, priority))
    return cards


def _assess_domain_routes(
    domain: str,
    routes: list[ParagraphRoute],
) -> tuple[list[EvidenceRoute], list[EvidenceRoute]]:
    accepted: list[EvidenceRoute] = []
    suppressed: list[EvidenceRoute] = []
    for route in routes:
        assessment = assess_evidence(route.text, domain)
        item = EvidenceRoute(route, assessment)
        if assessment.keep:
            accepted.append(item)
        else:
            suppressed.append(item)
    accepted.sort(key=lambda item: (-item.assessment.score, item.route.paragraph_id))
    suppressed.sort(key=lambda item: (item.route.paragraph_id, item.assessment.score))
    return accepted, suppressed


def _build_card(
    index: int,
    domain: str,
    accepted: list[EvidenceRoute],
    suppressed: list[EvidenceRoute],
    priority: str,
) -> RiskCard:
    routes = [item.route for item in accepted]
    text = " ".join(route.text for route in routes)
    template = template_for(domain)
    subdomains = _subdomains(domain, routes)
    questions = QUESTION_BANK.get(domain, {})
    reading_decision = reading_decision_for(priority)
    source_excerpts = [
        SourceExcerpt(
            paragraph_id=item.route.paragraph_id,
            source_ref=item.route.source_ref,
            excerpt=_excerpt(item.route.text),
            evidence_quality=item.assessment.quality,
            evidence_notes=item.assessment.notes,
        )
        for item in accepted[:MAX_EXCERPTS_PER_CARD]
    ]
    suppressed_excerpts = [
        SourceExcerpt(
            paragraph_id=item.route.paragraph_id,
            source_ref=item.route.source_ref,
            excerpt=_excerpt(item.route.text),
            evidence_quality=item.assessment.quality,
            evidence_notes=item.assessment.notes,
        )
        for item in suppressed[:MAX_EXCERPTS_PER_CARD]
    ]
    facts = extract_issuer_facts([item.route.text for item in accepted], domain)
    evidence_quality = _overall_evidence_quality(accepted)
    evidence_summary = _evidence_summary(domain, facts, accepted, suppressed)
    issuer_specific_interpretation = _issuer_specific_interpretation(domain, template.title, facts)
    finance_reader_implication = _finance_reader_implication(domain, template.title, facts)

    return RiskCard(
        card_id=f"RC-{index:03d}",
        title=template.title,
        risk_domain=domain,
        subdomains=subdomains,
        priority=priority,
        reading_decision=reading_decision,
        owners=template.owners,
        source_paragraphs=sorted(route.paragraph_id for route in routes),
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
        issuer_specific_facts=facts,
        issuer_specific_interpretation=issuer_specific_interpretation,
        finance_reader_implication=finance_reader_implication,
        evidence_quality=evidence_quality,
        evidence_summary=evidence_summary,
        weak_or_suppressed_sources=suppressed_excerpts,
        recommended_review_posture=_review_posture(priority, evidence_quality, facts),
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


def _overall_evidence_quality(items: list[EvidenceRoute]) -> str:
    if any(item.assessment.quality == "high" for item in items):
        return "high"
    if any(item.assessment.quality == "medium" for item in items):
        return "medium"
    return "low"


def _evidence_summary(
    domain: str,
    facts: list[str],
    accepted: list[EvidenceRoute],
    suppressed: list[EvidenceRoute],
) -> str:
    if facts:
        return (
            f"{len(accepted)} source paragraph(s) survived evidence filtering for `{domain}`. "
            f"The strongest issuer-specific support is: {facts[0]}"
        )
    return (
        f"{len(accepted)} source paragraph(s) survived evidence filtering for `{domain}`, "
        f"with {len(suppressed)} weak or taxonomy-like source paragraph(s) suppressed."
    )


def _issuer_specific_interpretation(domain: str, title: str, facts: list[str]) -> str:
    fact_text = _fact_sentence(facts)
    domain_intro = {
        "guarantees_commitments": (
            "This should be read as a contingent-obligation and commitment review item, "
            "not as ordinary operating commentary."
        ),
        "equity_dilution_control": (
            "This should be read as an equity-linked instrument and potential dilution review item."
        ),
        "material_contracts": (
            "This should be read as a contract-dependency and intangible-accounting review item, "
            "not as proof that the contract guarantees future revenue."
        ),
        "legal_proceedings_litigation": (
            "This should be read as a litigation-contingency review item that connects legal posture "
            "to accrual, loss-range, and disclosure questions."
        ),
        "cybersecurity_governance": (
            "This should be read as cybersecurity governance and incident-readiness disclosure, "
            "not as evidence of a cyber incident by itself."
        ),
        "tax_cross_border": (
            "This should be read as a tax and jurisdictional assumptions review item only to the extent "
            "issuer-specific tax positions or reserves are disclosed."
        ),
    }.get(domain, f"This should be read as an issuer-specific {title.lower()} review item.")
    if fact_text:
        return f"{domain_intro} Filing-specific support: {fact_text}"
    return domain_intro


def _finance_reader_implication(domain: str, title: str, facts: list[str]) -> str:
    base = {
        "guarantees_commitments": (
            "Finance readers should separate maximum exposure, mitigation such as escrow or partner payments, "
            "fair-value treatment, and actual expected cash outflow."
        ),
        "equity_dilution_control": (
            "Finance readers should separate current shares outstanding from contingent or equity-linked instruments "
            "that may affect dilution, fair value, or investor messaging."
        ),
        "material_contracts": (
            "Finance readers should connect the disclosed agreement to intangible assets, goodwill, amortization, "
            "customer-contract assumptions, and whether revenue durability is actually supported."
        ),
        "legal_proceedings_litigation": (
            "Finance readers should connect legal status to accrual, reasonably possible loss, cash timing, and "
            "whether management can estimate a range of loss."
        ),
        "cybersecurity_governance": (
            "Finance readers should treat the disclosure as a governance and process-readiness item, with attention "
            "to material incident assessment, vendor risk, and oversight."
        ),
    }.get(
        domain,
        f"Finance readers should verify how the {title.lower()} disclosure connects to accounts, assumptions, cash flow, and investor-facing wording.",
    )
    if facts:
        return f"{base} The source facts to reconcile include: {_fact_sentence(facts[:2])}"
    return base


def _review_posture(priority: str, evidence_quality: str, facts: list[str]) -> str:
    if priority in {"Critical", "High"} and evidence_quality in {"high", "medium"}:
        return "read-first"
    if evidence_quality == "high" and facts:
        return "read-first"
    if evidence_quality == "low":
        return "appendix"
    return "appendix"


def _fact_sentence(facts: list[str]) -> str:
    return "; ".join(facts[:3])


def _excerpt(text: str, limit: int = 560) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."
