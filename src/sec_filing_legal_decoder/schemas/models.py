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
