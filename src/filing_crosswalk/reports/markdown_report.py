"""Markdown review report rendering."""

from __future__ import annotations

from collections import Counter, defaultdict

from filing_crosswalk.schemas import ReviewReport


def render_markdown_report(report: ReviewReport) -> str:
    """Render a full filing review report in Markdown."""

    lines: list[str] = [
        f"# Filing Crosswalk Review: {report.document_title}",
        "",
        "## Executive Summary",
        "",
        report.executive_summary,
        "",
        f"- Source: `{report.source_path}`",
        f"- Parser backend: `{report.parser_backend}`",
        f"- Paragraphs analyzed: {len(report.analyses)}",
        "",
    ]
    lines.extend(_section_summary(report))
    lines.extend(_top_flagged(report))
    lines.extend(_escalation_matrix(report))
    lines.extend(_notes(report))
    lines.extend(_next_actions())
    lines.extend(["## Disclaimer", "", report.disclaimer, ""])
    return "\n".join(lines)


def _section_summary(report: ReviewReport) -> list[str]:
    counts = Counter(item.section_type for item in report.analyses)
    decisions = Counter(item.reading_decision for item in report.analyses)
    lines = ["## Classification Snapshot", ""]
    if not report.analyses:
        return lines + ["No paragraphs were analyzed.", ""]

    lines.append("Section types:")
    for section_type, count in sorted(counts.items()):
        lines.append(f"- {section_type}: {count}")
    lines.append("")
    lines.append("Reading decisions:")
    for decision, count in sorted(decisions.items()):
        lines.append(f"- {decision}: {count}")
    lines.append("")
    return lines


def _top_flagged(report: ReviewReport) -> list[str]:
    lines = ["## Top Flagged Paragraphs", ""]
    if not report.top_flagged_paragraphs:
        return lines + ["No paragraphs were flagged for deep review or escalation.", ""]

    by_id = {item.paragraph_id: item for item in report.analyses}
    for paragraph_id in report.top_flagged_paragraphs:
        item = by_id[paragraph_id]
        lines.extend(
            [
                f"### Paragraph {item.paragraph_id}: {item.reading_decision}",
                "",
                f"- Section type: `{item.section_type}`",
                f"- Boilerplate/material: `{item.boilerplate_or_material}`",
                f"- Source: `{item.source_ref}`",
                f"- Signals: {', '.join(item.signals) if item.signals else 'none'}",
                "",
                f"> {item.source_excerpt}",
                "",
            ]
        )
    return lines


def _escalation_matrix(report: ReviewReport) -> list[str]:
    matrix: dict[str, list[str]] = defaultdict(list)
    for item in report.analyses:
        if item.reading_decision not in {"DEEP_READ", "ESCALATE"}:
            continue
        for role in item.escalation_questions:
            matrix[role].append(f"Paragraph {item.paragraph_id} ({item.section_type})")

    lines = ["## Escalation Matrix", ""]
    if not matrix:
        return lines + ["No escalation-style follow-up was flagged by v0.1 rules.", ""]

    for role, refs in matrix.items():
        unique_refs = sorted(set(refs))
        lines.append(f"- {role}: {', '.join(unique_refs)}")
    lines.append("")
    return lines


def _notes(report: ReviewReport) -> list[str]:
    lines = ["## Legal-to-Finance Notes", ""]
    if not report.analyses:
        return lines + ["No legal-to-finance notes were generated.", ""]

    for item in report.analyses:
        lines.extend(
            [
                f"### Paragraph {item.paragraph_id}",
                "",
                f"- Reading decision: `{item.reading_decision}`",
                f"- Section type: `{item.section_type}`",
                f"- Boilerplate/material: `{item.boilerplate_or_material}`",
                f"- Confidence: {item.confidence:.2f}",
                f"- Plain-English meaning: {item.plain_english_meaning}",
                f"- Business relevance: {item.business_relevance}",
                f"- Financial relevance: {item.financial_relevance}",
                f"- What to compare: {', '.join(item.what_to_compare)}",
                f"- Suggested management briefing sentence: {item.suggested_management_briefing_sentence}",
                "",
                "Escalation questions:",
            ]
        )
        for role, questions in item.escalation_questions.items():
            lines.append(f"- {role}:")
            for question in questions:
                lines.append(f"  - {question}")
        lines.extend(["", f"> {item.source_excerpt}", ""])
    return lines


def _next_actions() -> list[str]:
    return [
        "## Suggested Next Actions",
        "",
        "- Reconcile flagged paragraphs against financial statement footnotes, MD&A, and prior-year wording.",
        "- Route role-specific questions to Legal, Finance, Auditor, IR, or Management / Board as appropriate.",
        "- Do not treat this report as a legal, accounting, audit, investment, or disclosure conclusion.",
        "",
    ]
