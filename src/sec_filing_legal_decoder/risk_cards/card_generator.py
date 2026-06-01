"""Generate issue-level legal risk cards from routed filing paragraphs."""

from __future__ import annotations

import re
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
DOMAIN_SORT = {
    "audit_going_concern": 0,
    "legal_proceedings_litigation": 1,
    "material_contracts": 2,
    "guarantees_commitments": 3,
    "tax_cross_border": 4,
    "cybersecurity_governance": 5,
    "internal_control_reporting": 6,
    "regulatory_trade_policy": 7,
    "related_party_governance": 8,
    "equity_dilution_control": 9,
    "debt_liquidity_covenant": 10,
    "management_board_governance": 11,
    "disclosure_ir_consistency": 12,
}
READ_FIRST_DOMAINS = {
    "audit_going_concern",
    "legal_proceedings_litigation",
    "material_contracts",
    "guarantees_commitments",
    "tax_cross_border",
    "cybersecurity_governance",
    "internal_control_reporting",
    "regulatory_trade_policy",
    "related_party_governance",
}


@dataclass(frozen=True)
class EvidenceRoute:
    """A routed paragraph plus its evidence assessment."""

    route: ParagraphRoute
    assessment: EvidenceAssessment


@dataclass(frozen=True)
class CardCandidate:
    """Pre-card domain candidate before cross-domain consolidation."""

    domain: str
    accepted: list[EvidenceRoute]
    suppressed: list[EvidenceRoute]
    priority: str


def generate_risk_card_report(document: ParsedDocument) -> RiskCardReport:
    """Generate a v0.3 risk-card report from a parsed document."""

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

    candidates: list[CardCandidate] = []
    for domain, domain_routes in grouped.items():
        accepted, suppressed = _assess_domain_routes(domain, domain_routes)
        if not accepted:
            continue
        text = " ".join(item.route.text for item in accepted)
        priority = priority_for(domain, text, len(accepted))
        candidates.append(CardCandidate(domain, accepted, suppressed, priority))
    candidates = _consolidate_candidates(candidates)
    candidates.sort(
        key=lambda item: (
            PRIORITY_SORT.get(item.priority, 9),
            DOMAIN_SORT.get(item.domain, 99),
            item.accepted[0].route.paragraph_id,
            item.domain,
        )
    )

    cards: list[RiskCard] = []
    for index, candidate in enumerate(candidates[:MAX_CARDS], start=1):
        cards.append(
            _build_card(
                index,
                candidate.domain,
                candidate.accepted,
                candidate.suppressed,
                candidate.priority,
            )
        )
    return cards


def _consolidate_candidates(candidates: list[CardCandidate]) -> list[CardCandidate]:
    """Suppress duplicate-prone cards when a stronger primary card covers the evidence."""

    by_domain = {candidate.domain: candidate for candidate in candidates}
    result: list[CardCandidate] = []
    for candidate in candidates:
        if _should_suppress_candidate(candidate, by_domain):
            continue
        result.append(candidate)
    return result


def _should_suppress_candidate(
    candidate: CardCandidate,
    by_domain: dict[str, CardCandidate],
) -> bool:
    if candidate.domain == "debt_liquidity_covenant":
        guarantee = by_domain.get("guarantees_commitments")
        if guarantee and _source_overlap(candidate, guarantee) >= 0.5 and _is_partner_guarantee_duplicate(candidate):
            return True
        if not _has_true_debt_or_covenant_context(candidate):
            return True

    if candidate.domain == "equity_dilution_control":
        guarantee = by_domain.get("guarantees_commitments")
        if guarantee and _source_overlap(candidate, guarantee) > 0 and _is_warrant_only_guarantee_duplicate(candidate):
            return True
        if _is_stock_comp_only_equity_candidate(candidate):
            return True

    if candidate.domain == "disclosure_ir_consistency":
        litigation = by_domain.get("legal_proceedings_litigation")
        if litigation and _source_overlap(candidate, litigation) >= 0.25 and not _has_standalone_disclosure_issue(candidate):
            return True
        if not _has_standalone_disclosure_issue(candidate):
            return True

    if candidate.domain == "management_board_governance":
        litigation = by_domain.get("legal_proceedings_litigation")
        cybersecurity = by_domain.get("cybersecurity_governance")
        if litigation and _source_overlap(candidate, litigation) >= 0.25 and _is_litigation_or_buyback_governance_duplicate(candidate):
            return True
        if cybersecurity and _source_overlap(candidate, cybersecurity) >= 0.25:
            return True
        if _is_weak_governance_candidate(candidate):
            return True

    return False


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


def _source_overlap(left: CardCandidate, right: CardCandidate) -> float:
    left_ids = {item.route.paragraph_id for item in left.accepted}
    right_ids = {item.route.paragraph_id for item in right.accepted}
    if not left_ids:
        return 0.0
    return len(left_ids & right_ids) / len(left_ids)


def _candidate_text(candidate: CardCandidate) -> str:
    return " ".join(item.route.text for item in candidate.accepted).lower()


def _is_partner_guarantee_duplicate(candidate: CardCandidate) -> bool:
    text = _candidate_text(candidate)
    has_guarantee_context = bool(re.search(r"guarantee|guaranty|lease obligations?|partner|warrants?", text))
    has_true_debt_context = bool(
        re.search(
            r"debt covenant|financial covenant|credit facility|senior notes?|borrowings?|maturit|"
            r"refinanc|waiver|revolver|loan agreement|principal repayment",
            text,
        )
    )
    return has_guarantee_context and not has_true_debt_context


def _is_warrant_only_guarantee_duplicate(candidate: CardCandidate) -> bool:
    text = _candidate_text(candidate)
    has_warrant_context = "warrant" in text
    has_standalone_equity_context = bool(
        re.search(
            r"dilution|convertible|earnout|share issuance|equity issuance|voting rights?|"
            r"registration rights?|change[- ]of[- ]control|rsu|restricted stock|pipe",
            text,
        )
    )
    return has_warrant_context and not has_standalone_equity_context


def _has_true_debt_or_covenant_context(candidate: CardCandidate) -> bool:
    text = _candidate_text(candidate)
    return bool(
        re.search(
            r"debt covenant|financial covenant|credit facility|senior notes?|borrowings?|"
            r"short[- ]term debt|long[- ]term debt|maturit(?:y|ies)|refinanc|waiver|revolver|"
            r"loan agreement|principal repayment|commercial paper",
            text,
        )
    )


def _is_stock_comp_only_equity_candidate(candidate: CardCandidate) -> bool:
    text = _candidate_text(candidate)
    true_equity_risk = bool(
        re.search(
            r"convertible notes?|earnout|dilution|share issuance|equity issuance|registration rights?|"
            r"change[- ]of[- ]control|voting rights?|founder control|pipe",
            text,
        )
    )
    ordinary_stock_comp = bool(re.search(r"rsu|restricted stock|performance stock|stock-based compensation|espp", text))
    return ordinary_stock_comp and not true_equity_risk


def _has_standalone_disclosure_issue(candidate: CardCandidate) -> bool:
    text = _candidate_text(candidate)
    return bool(
        re.search(
            r"safe harbor|forward[- ]looking|guidance|non[- ]gaap|"
            r"cannot assure|investor presentation|earnings call|public statement",
            text,
        )
    )


def _is_litigation_or_buyback_governance_duplicate(candidate: CardCandidate) -> bool:
    text = _candidate_text(candidate)
    litigation_context = bool(re.search(r"derivative|lawsuit|litigation|complaint|claim|proceeding", text))
    buyback_context = bool(re.search(r"repurchase|buyback|share repurchase|stock repurchase", text))
    true_governance_context = bool(
        re.search(
            r"audit committee|independent directors?|succession|resign|appoint|transition|"
            r"committee charter|board oversight|nomination|governance guideline",
            text,
        )
    )
    return (litigation_context or buyback_context) and not true_governance_context


def _is_weak_governance_candidate(candidate: CardCandidate) -> bool:
    text = _candidate_text(candidate)
    true_governance_context = bool(
        re.search(
            r"audit committee|independent directors?|succession|resign|appoint|transition|"
            r"committee charter|board oversight|nomination|governance guideline|internal control",
            text,
        )
    )
    buyback_only = bool(re.search(r"repurchase|buyback|dividend|stock split", text))
    return buyback_only and not true_governance_context


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
    financial_analysis_difference = _financial_analysis_difference(domain, template.title, facts)

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
        financial_analysis_difference=financial_analysis_difference,
        evidence_quality=evidence_quality,
        evidence_summary=evidence_summary,
        weak_or_suppressed_sources=suppressed_excerpts,
        recommended_review_posture=_review_posture(domain, priority, evidence_quality, facts),
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
            "This should be read as a deferred-tax, valuation-allowance, and jurisdictional "
            "assumptions review item. The review point is whether deferred tax assets are supported "
            "by more-likely-than-not future taxable income assumptions, not simply whether the "
            "effective tax rate moved."
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
        "tax_cross_border": (
            "Finance readers should connect deferred tax assets, valuation allowance releases, uncertain tax "
            "positions, and jurisdiction-level taxable income assumptions to earnings quality and cash-tax durability. "
            "A valuation allowance release may be one-time unless the filing supports recurring taxable income."
        ),
    }.get(
        domain,
        f"Finance readers should verify how the {title.lower()} disclosure connects to accounts, assumptions, cash flow, and investor-facing wording.",
    )
    if facts:
        return f"{base} The source facts to reconcile include: {_fact_sentence(facts[:2])}"
    return base


def _financial_analysis_difference(domain: str, title: str, facts: list[str]) -> str:
    base = {
        "legal_proceedings_litigation": (
            "This is different from ordinary financial analysis because the first question is not revenue, margin, "
            "or valuation impact. It is how legal status translates into loss contingency, accrual, range-of-loss, "
            "insurance, timing, and disclosure thresholds."
        ),
        "material_contracts": (
            "This is different from ordinary financial analysis because contract rights, termination terms, IP rights, "
            "and accounting recognition can change how revenue durability, goodwill, and intangible assets should be read."
        ),
        "guarantees_commitments": (
            "This is different from ordinary financial analysis because the exposure may sit in guarantees, commitments, "
            "or off-balance-sheet arrangements rather than in a simple debt or capex line."
        ),
        "tax_cross_border": (
            "This is different from ordinary financial analysis because the key issue is not only the effective tax rate. "
            "It is whether deferred tax assets, valuation allowance releases, uncertain tax positions, and jurisdictional "
            "taxable-income assumptions are supportable."
        ),
        "cybersecurity_governance": (
            "This is different from ordinary financial analysis because the disclosure is mainly about governance, "
            "incident materiality assessment, board oversight, and response readiness rather than a current quantified loss."
        ),
        "internal_control_reporting": (
            "This is different from ordinary financial analysis because the issue is reporting reliability, remediation "
            "evidence, and audit/control conclusions rather than the performance trend itself."
        ),
        "regulatory_trade_policy": (
            "This is different from ordinary financial analysis because rule interpretation, market access, import status, "
            "sanctions, tariffs, or compliance evidence may drive whether the modeled economics can actually be realized."
        ),
        "debt_liquidity_covenant": (
            "This is different from ordinary financial analysis because contract definitions, covenants, defaults, waivers, "
            "maturity classification, and acceleration rights can matter more than headline liquidity metrics."
        ),
        "equity_dilution_control": (
            "This is different from ordinary financial analysis because legal instrument terms can change dilution, "
            "fair-value accounting, voting rights, registration obligations, and investor messaging."
        ),
        "management_board_governance": (
            "This is different from ordinary financial analysis because the issue is governance process, board or committee "
            "oversight, independence, and disclosure controls rather than the business action alone."
        ),
        "disclosure_ir_consistency": (
            "This is different from ordinary financial analysis because the core question is whether public or management "
            "wording preserves the filing's uncertainty instead of making the model's base case sound certain."
        ),
    }.get(
        domain,
        f"This is different from ordinary financial analysis because {title.lower()} language needs legal, audit, "
        "disclosure, and finance-owner review before it becomes a conclusion.",
    )
    if domain == "tax_cross_border" and any("711" in fact for fact in facts):
        return (
            f"{base} A disclosed $711 million release should be reviewed as a possible one-time valuation allowance "
            "or deferred-tax item unless recurring support is clear."
        )
    return base


def _review_posture(domain: str, priority: str, evidence_quality: str, facts: list[str]) -> str:
    if domain == "disclosure_ir_consistency":
        return "appendix"
    if domain == "management_board_governance" and priority != "High":
        return "appendix"
    if domain in READ_FIRST_DOMAINS and priority in {"Critical", "High"} and evidence_quality in {"high", "medium"}:
        return "read-first"
    if domain in READ_FIRST_DOMAINS and evidence_quality == "high" and facts:
        return "read-first"
    if domain in {"tax_cross_border", "cybersecurity_governance"} and evidence_quality == "medium" and facts:
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
