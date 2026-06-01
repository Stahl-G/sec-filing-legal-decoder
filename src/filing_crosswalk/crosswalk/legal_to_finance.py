"""Generate legal-to-finance crosswalk notes from parsed text."""

from __future__ import annotations

from filing_crosswalk.classifiers import classify_section, triage_paragraph
from filing_crosswalk.schemas import ParagraphAnalysis, ParsedDocument, ReviewReport
from filing_crosswalk.utils import source_ref, split_paragraphs

from .escalation_questions import generate_escalation_questions
from .finance_relevance_map import guidance_for
from .reading_decision import is_flagged


def analyze_document(document: ParsedDocument) -> ReviewReport:
    """Analyze a parsed document and return a structured review report."""

    paragraphs = split_paragraphs(document.content)
    analyses = [
        analyze_paragraph(index, paragraph, document.source_path)
        for index, paragraph in enumerate(paragraphs, start=1)
    ]
    top_flagged = [
        analysis.paragraph_id
        for analysis in analyses
        if is_flagged(analysis.reading_decision)
    ][:10]
    summary = _executive_summary(analyses)

    return ReviewReport(
        document_title=document.title or "Untitled Filing Review",
        source_path=document.source_path,
        parser_backend=document.parser_backend,
        executive_summary=summary,
        top_flagged_paragraphs=top_flagged,
        analyses=analyses,
    )


def analyze_paragraph(
    paragraph_id: int, paragraph: str, source_path: str = "input"
) -> ParagraphAnalysis:
    """Analyze a single paragraph."""

    section_type = classify_section(paragraph)
    triage = triage_paragraph(paragraph, section_type)
    guidance = guidance_for(section_type)
    questions = generate_escalation_questions(
        section_type, triage.reading_decision, triage.signals
    )
    suggested_sentence = _briefing_sentence(
        section_type, triage.reading_decision, triage.boilerplate_or_material
    )

    return ParagraphAnalysis(
        paragraph_id=paragraph_id,
        source_ref=source_ref(source_path, paragraph_id),
        section_type=section_type,
        plain_english_meaning=str(guidance["plain"]),
        boilerplate_or_material=triage.boilerplate_or_material,
        reading_decision=triage.reading_decision,
        business_relevance=str(guidance["business"]),
        financial_relevance=str(guidance["financial"]),
        what_to_compare=list(guidance["compare"]),
        escalation_questions=questions,
        suggested_management_briefing_sentence=suggested_sentence,
        confidence=triage.confidence,
        source_excerpt=_excerpt(paragraph),
        signals=triage.signals,
    )


def _executive_summary(analyses: list[ParagraphAnalysis]) -> str:
    if not analyses:
        return "No analysis-ready paragraphs were found."

    flagged = [item for item in analyses if is_flagged(item.reading_decision)]
    escalations = [item for item in analyses if item.reading_decision == "ESCALATE"]
    categories = sorted({item.section_type for item in analyses})
    return (
        f"Reviewed {len(analyses)} paragraphs across {len(categories)} detected "
        f"section type(s). {len(flagged)} paragraph(s) were flagged for deep "
        f"review and {len(escalations)} require escalation-style follow-up. "
        "Outputs are triage aids and should be reconciled with qualified "
        "professional review."
    )


def _briefing_sentence(
    section_type: str, reading_decision: str, boilerplate_or_material: str
) -> str:
    section_label = section_type.replace("_", " ")
    if reading_decision == "ESCALATE":
        return (
            f"Management should review this {section_label} disclosure because "
            f"the v0.1 rules flagged it as {boilerplate_or_material} and suitable "
            "for role-specific escalation questions."
        )
    if reading_decision == "DEEP_READ":
        return (
            f"This {section_label} language should be deep-read and reconciled "
            "against financial statement notes, MD&A, and prior-year wording."
        )
    if boilerplate_or_material == "likely_boilerplate":
        return (
            f"This {section_label} language appears likely boilerplate under "
            "v0.1 rules, but wording changes or specific facts should still be checked."
        )
    return (
        f"This {section_label} language should be read in context before drawing "
        "any business or finance conclusion."
    )


def _excerpt(paragraph: str, limit: int = 420) -> str:
    text = " ".join(paragraph.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."
