"""Dataclass models used across parser, analysis, and report layers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


DISCLAIMER = (
    "This project is not legal advice, investment advice, accounting advice, "
    "audit advice, or a substitute for qualified professional review. It is "
    "designed to help readers classify, simplify, and triage legal-heavy filing "
    "language and generate better escalation questions. Users should consult "
    "qualified legal, accounting, audit, or investment professionals before "
    "relying on any output."
)


@dataclass(frozen=True)
class ParsedDocument:
    """Text extracted from an input document by a parser backend."""

    source_path: str
    content: str
    parser_backend: str
    title: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ParagraphAnalysis:
    """Legal-to-finance crosswalk result for one paragraph."""

    paragraph_id: int
    source_ref: str
    section_type: str
    plain_english_meaning: str
    boilerplate_or_material: str
    reading_decision: str
    business_relevance: str
    financial_relevance: str
    what_to_compare: list[str]
    escalation_questions: dict[str, list[str]]
    suggested_management_briefing_sentence: str
    confidence: float
    source_excerpt: str
    signals: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewReport:
    """Document-level report containing paragraph analyses."""

    document_title: str
    source_path: str
    parser_backend: str
    executive_summary: str
    top_flagged_paragraphs: list[int]
    analyses: list[ParagraphAnalysis]
    disclaimer: str = DISCLAIMER

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DocumentInfo:
    """Document identity and filing mode for v0.4 risk-card reports."""

    title: str
    form_type: str
    mode: str
    source_path: str
    parser_backend: str


@dataclass(frozen=True)
class CoverageSummary:
    """Routing counts for the risk-card analysis pipeline."""

    paragraphs_total: int
    paragraphs_skipped_admin: int
    financial_kpi_routed_out: int
    business_update_routed_out: int
    risk_relevant_paragraphs: int
    risk_cards_generated: int


@dataclass(frozen=True)
class SourceExcerpt:
    """Short source excerpt supporting a risk card."""

    paragraph_id: int
    source_ref: str
    excerpt: str
    evidence_quality: str = "medium"
    evidence_notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RiskCard:
    """Issue-level legal risk card for finance readers."""

    card_id: str
    title: str
    risk_domain: str
    subdomains: list[str]
    priority: str
    reading_decision: str
    owners: list[str]
    source_paragraphs: list[int]
    plain_language_meaning: str
    why_finance_readers_should_care: str
    legal_or_audit_relevance: str
    financial_statement_linkage: list[str]
    disclosure_ir_relevance: str
    boilerplate_or_material: str
    questions: dict[str, list[str]]
    suggested_management_follow_up: str
    what_not_to_overstate: str
    source_excerpts: list[SourceExcerpt]
    confidence: float
    issuer_specific_facts: list[str] = field(default_factory=list)
    issuer_specific_interpretation: str = ""
    finance_reader_implication: str = ""
    financial_analysis_difference: str = ""
    evidence_quality: str = "medium"
    evidence_summary: str = ""
    weak_or_suppressed_sources: list[SourceExcerpt] = field(default_factory=list)
    recommended_review_posture: str = "appendix"


@dataclass(frozen=True)
class RiskCardReport:
    """Document-level v0.4 report centered on risk cards."""

    document: DocumentInfo
    coverage_summary: CoverageSummary
    risk_cards: list[RiskCard]
    escalation_matrix: list[dict[str, Any]]
    management_follow_up: list[str]
    disclosure_consistency_questions: list[str]
    review_mode: str = "source-only"
    external_enrichment: bool = False
    issuer_profile: str = "general"
    disclaimer: str = DISCLAIMER

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OverlayFinding:
    """Finding from comparing a filing against an existing analysis."""

    risk_card_id: str
    risk_card_title: str
    status: str
    finding: str
    suggested_safer_wording: str


@dataclass(frozen=True)
class OverlayReport:
    """Review overlay report for an existing earnings or filing analysis."""

    document: DocumentInfo
    analysis_path: str
    risk_card_report: RiskCardReport
    findings: list[OverlayFinding]
    disclaimer: str = DISCLAIMER

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
