"""Management memo Markdown rendering."""

from __future__ import annotations

from sec_filing_legal_decoder.schemas import ReviewReport


def render_management_memo(report: ReviewReport) -> str:
    """Render a concise management memo from a review report."""

    flagged = [
        item
        for item in report.analyses
        if item.reading_decision in {"DEEP_READ", "ESCALATE"}
    ]
    lines: list[str] = [
        f"# Management Memo: {report.document_title}",
        "",
        "## Purpose",
        "",
        "Summarize legal-heavy filing language that may need finance, legal, audit, IR, or management follow-up.",
        "",
        "## Executive Takeaway",
        "",
        report.executive_summary,
        "",
        "## Priority Items",
        "",
    ]

    if not flagged:
        lines.extend(
            [
                "No paragraphs were flagged for deep review or escalation by v0.1 rules.",
                "",
            ]
        )
    else:
        for item in flagged[:8]:
            lines.extend(
                [
                    f"### Paragraph {item.paragraph_id}: {item.section_type}",
                    "",
                    f"- Decision: `{item.reading_decision}`",
                    f"- Finance relevance: {item.financial_relevance}",
                    f"- Briefing sentence: {item.suggested_management_briefing_sentence}",
                    f"- Compare against: {', '.join(item.what_to_compare)}",
                    "",
                ]
            )

    lines.extend(["## Disclaimer", "", report.disclaimer, ""])
    return "\n".join(lines)
