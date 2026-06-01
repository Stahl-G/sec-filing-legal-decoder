"""Obsidian-friendly Markdown review report rendering."""

from __future__ import annotations

from collections import Counter, defaultdict

from sec_filing_legal_decoder.schemas import ParagraphAnalysis, ReviewReport


def render_markdown_report(report: ReviewReport) -> str:
    """Render the default report as Obsidian-friendly Markdown."""

    priority = _priority_analyses(report)
    lines: list[str] = [
        * _frontmatter(report, priority),
        f"# SEC Filing Legal Decoder Review: {report.document_title}",
        "",
        "> [!summary] Executive Summary",
        * _quote_lines(report.executive_summary),
        "",
        "## Source",
        "",
        f"- Source path: `{report.source_path}`",
        f"- Parser backend: `{report.parser_backend}`",
        f"- Paragraphs analyzed: {len(report.analyses)}",
        f"- Priority paragraphs: {len(priority)}",
        "",
    ]
    lines.extend(_decision_snapshot(report))
    lines.extend(_section_snapshot(report))
    lines.extend(_priority_paragraphs(priority))
    lines.extend(_escalation_matrix(priority))
    lines.extend(_all_paragraph_index(report))
    lines.extend(_next_actions())
    lines.extend(["> [!caution] Disclaimer", * _quote_lines(report.disclaimer), ""])
    return "\n".join(lines).rstrip() + "\n"


def _frontmatter(report: ReviewReport, priority: list[ParagraphAnalysis]) -> list[str]:
    return [
        "---",
        f'title: "{_yaml_escape("SEC Filing Legal Decoder Review - " + report.document_title)}"',
        "aliases:",
        f'  - "{_yaml_escape(report.document_title + " filing review")}"',
        "tags:",
        "  - sec-filing",
        "  - legal-to-finance",
        "  - sec-filing-legal-decoder/report",
        f'source_path: "{_yaml_escape(report.source_path)}"',
        f"parser_backend: {report.parser_backend}",
        f"paragraphs_analyzed: {len(report.analyses)}",
        f"priority_paragraphs: {len(priority)}",
        "---",
        "",
    ]


def _decision_snapshot(report: ReviewReport) -> list[str]:
    counts = Counter(item.reading_decision for item in report.analyses)
    lines = ["## Reading Decision Snapshot", "", "| Decision | Count |", "| --- | ---: |"]
    for decision in ["ESCALATE", "DEEP_READ", "READ", "SKIM", "SKIP"]:
        lines.append(f"| {decision} | {counts.get(decision, 0)} |")
    lines.append("")
    return lines


def _section_snapshot(report: ReviewReport) -> list[str]:
    counts = Counter(item.section_type for item in report.analyses)
    lines = ["## Section Type Snapshot", "", "| Section Type | Count |", "| --- | ---: |"]
    for section_type, count in sorted(counts.items()):
        lines.append(f"| `{section_type}` | {count} |")
    lines.append("")
    return lines


def _priority_paragraphs(priority: list[ParagraphAnalysis]) -> list[str]:
    lines = ["## Priority Paragraphs", ""]
    if not priority:
        return lines + ["No paragraphs were flagged for deep review or escalation.", ""]

    for item in priority:
        callout = _callout_for_decision(item.reading_decision)
        lines.extend(
            [
                f"> [!{callout}] P{item.paragraph_id:04d} - {item.section_type} - {item.reading_decision}",
                f"> **Materiality posture:** `{item.boilerplate_or_material}`",
                f"> **Confidence:** {item.confidence:.2f}",
                f"> **Source:** `{item.source_ref}`",
                ">",
                * _quote_lines(item.source_excerpt),
                "",
                "### Legal-to-Finance Note",
                "",
                f"- Plain-English meaning: {item.plain_english_meaning}",
                f"- Business relevance: {item.business_relevance}",
                f"- Financial relevance: {item.financial_relevance}",
                f"- What to compare: {', '.join(item.what_to_compare)}",
                f"- Suggested management briefing sentence: {item.suggested_management_briefing_sentence}",
                "",
            ]
        )
        lines.extend(_questions_for_item(item))
    return lines


def _questions_for_item(item: ParagraphAnalysis) -> list[str]:
    if not item.escalation_questions:
        return ["No role-specific escalation questions were generated.", ""]
    lines = ["### Escalation Questions", ""]
    for role, questions in item.escalation_questions.items():
        lines.extend([f"> [!question] {role}"])
        for question in questions:
            lines.append(f"> - {question}")
        lines.append("")
    return lines


def _escalation_matrix(priority: list[ParagraphAnalysis]) -> list[str]:
    matrix: dict[str, list[ParagraphAnalysis]] = defaultdict(list)
    for item in priority:
        for role in item.escalation_questions:
            matrix[role].append(item)

    lines = ["## Escalation Matrix", ""]
    if not matrix:
        return lines + ["No priority escalation questions were generated.", ""]

    for role, items in matrix.items():
        lines.extend([f"### {role}", ""])
        for item in items:
            lines.append(f"- P{item.paragraph_id:04d}: `{item.section_type}` / `{item.reading_decision}`")
        lines.append("")
    return lines


def _all_paragraph_index(report: ReviewReport) -> list[str]:
    lines = [
        "## All Paragraph Index",
        "",
        "| Paragraph | Decision | Section Type | Materiality | Confidence |",
        "| ---: | --- | --- | --- | ---: |",
    ]
    for item in report.analyses:
        lines.append(
            f"| P{item.paragraph_id:04d} | {item.reading_decision} | "
            f"`{item.section_type}` | `{item.boilerplate_or_material}` | {item.confidence:.2f} |"
        )
    lines.append("")
    return lines


def _next_actions() -> list[str]:
    return [
        "## Suggested Next Actions",
        "",
        "- Reconcile priority paragraphs against financial statement footnotes, MD&A, and prior-year wording.",
        "- Route role-specific questions to Legal, Finance, Auditor, IR, or Management / Board as appropriate.",
        "- Do not treat this report as a legal, accounting, audit, investment, or disclosure conclusion.",
        "",
    ]


def _priority_analyses(report: ReviewReport) -> list[ParagraphAnalysis]:
    return [
        item
        for item in report.analyses
        if item.reading_decision in {"DEEP_READ", "ESCALATE"}
    ]


def _callout_for_decision(decision: str) -> str:
    return {
        "SKIP": "quote",
        "SKIM": "note",
        "READ": "info",
        "DEEP_READ": "warning",
        "ESCALATE": "danger",
    }.get(decision, "info")


def _quote_lines(text: str) -> list[str]:
    return [f"> {line}" if line else ">" for line in text.splitlines()]


def _yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')
