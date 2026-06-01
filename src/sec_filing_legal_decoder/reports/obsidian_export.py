"""Obsidian vault export for SEC filing review reports."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from sec_filing_legal_decoder.schemas import ParagraphAnalysis, ReviewReport

from .json_report import render_json_report
from .memo_writer import render_management_memo


@dataclass(frozen=True)
class ObsidianExportOptions:
    """Options controlling an Obsidian export."""

    vault: Path
    folder: str
    company: str | None = None
    ticker: str | None = None
    form: str | None = None
    year: str | None = None


def export_obsidian_vault(report: ReviewReport, options: ObsidianExportOptions) -> list[Path]:
    """Export a review report as a linked set of Obsidian notes."""

    base_dir = _safe_join(options.vault, options.folder)
    paragraphs_dir = base_dir / "paragraphs"
    data_dir = base_dir / "data"
    paragraphs_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    context = _context(report, options)
    paragraph_files = {
        item.paragraph_id: _paragraph_file_name(item) for item in report.analyses
    }

    written: list[Path] = []
    file_payloads = {
        base_dir / "00 Dashboard.md": _dashboard(report, context, paragraph_files),
        base_dir / "01 Executive Summary.md": _executive_summary(report, context),
        base_dir / "02 Reading Decision Index.md": _reading_decision_index(
            report, context, paragraph_files
        ),
        base_dir / "03 Escalation Matrix.md": _escalation_matrix(
            report, context, paragraph_files
        ),
        base_dir / "04 Management Memo.md": _management_memo(report, context),
        base_dir / "05 Legal-to-Finance Notes.md": _legal_to_finance_notes(
            report, context, paragraph_files
        ),
        base_dir / "06 Suggested Questions.md": _suggested_questions(
            report, context, paragraph_files
        ),
        data_dir / "report.json": render_json_report(report),
    }

    for path, content in file_payloads.items():
        _write(path, content)
        written.append(path)

    for item in report.analyses:
        path = paragraphs_dir / paragraph_files[item.paragraph_id]
        _write(path, _paragraph_note(item, context))
        written.append(path)

    return written


def _context(report: ReviewReport, options: ObsidianExportOptions) -> dict[str, str]:
    title = report.document_title or "SEC Filing Review"
    return {
        "company": options.company or title,
        "ticker": options.ticker or "",
        "form": options.form or "",
        "year": options.year or "",
        "source": report.source_path,
        "title": title,
        "folder": options.folder.strip("/"),
    }


def _dashboard(
    report: ReviewReport, context: dict[str, str], paragraph_files: dict[int, str]
) -> str:
    decisions = Counter(item.reading_decision for item in report.analyses)
    owners = _owner_counts(report)
    lines = [
        * _frontmatter("dashboard", context),
        f"# {context['company']} {context['year']} {context['form']} Dashboard".strip(),
        "",
        "## Key Outputs",
        "",
        "- [[01 Executive Summary]]",
        "- [[02 Reading Decision Index]]",
        "- [[03 Escalation Matrix]]",
        "- [[04 Management Memo]]",
        "- [[05 Legal-to-Finance Notes]]",
        "- [[06 Suggested Questions]]",
        "- [[data/report.json|Structured JSON Archive]]",
        "",
        "## Filing Metadata",
        "",
        f"- Company: {context['company']}",
        f"- Ticker: {context['ticker'] or 'not specified'}",
        f"- Form: {context['form'] or 'not specified'}",
        f"- Year: {context['year'] or 'not specified'}",
        f"- Source: `{context['source']}`",
        f"- Paragraphs analyzed: {len(report.analyses)}",
        "",
        "## Reading Decision Snapshot",
        "",
    ]
    for decision in ["SKIP", "SKIM", "READ", "DEEP_READ", "ESCALATE"]:
        lines.append(f"- {decision}: {decisions.get(decision, 0)}")
    lines.extend(["", "## Escalation Owner Snapshot", ""])
    if owners:
        for owner, count in sorted(owners.items()):
            lines.append(f"- {owner}: {count}")
    else:
        lines.append("- No owner-specific escalation questions were generated.")
    lines.extend(["", "## Top Flagged", ""])
    if report.top_flagged_paragraphs:
        for paragraph_id in report.top_flagged_paragraphs:
            item = _analysis_by_id(report)[paragraph_id]
            lines.append(
                f"- [[paragraphs/{_link_stem(paragraph_files[paragraph_id])}|"
                f"P{paragraph_id:04d} - {item.section_type} - {item.reading_decision}]]"
            )
    else:
        lines.append("- No paragraphs were flagged for deep review or escalation.")
    lines.extend(["", _disclaimer_callout(report)])
    return "\n".join(lines)


def _executive_summary(report: ReviewReport, context: dict[str, str]) -> str:
    lines = [
        * _frontmatter("summary", context),
        "# Executive Summary",
        "",
        report.executive_summary,
        "",
        "## Source",
        "",
        f"- Source: `{report.source_path}`",
        f"- Parser backend: `{report.parser_backend}`",
        f"- Paragraphs analyzed: {len(report.analyses)}",
        "",
        _disclaimer_callout(report),
    ]
    return "\n".join(lines)


def _reading_decision_index(
    report: ReviewReport, context: dict[str, str], paragraph_files: dict[int, str]
) -> str:
    grouped: dict[str, list[ParagraphAnalysis]] = defaultdict(list)
    for item in report.analyses:
        grouped[item.reading_decision].append(item)

    lines = [
        * _frontmatter("reading-index", context),
        "# Reading Decision Index",
        "",
        "```dataview",
        'TABLE decision, section_type, owner, confidence',
        f'FROM "{context["folder"]}/paragraphs"',
        'WHERE decision = "ESCALATE" OR decision = "DEEP_READ"',
        "SORT decision DESC",
        "```",
        "",
    ]
    for decision in ["ESCALATE", "DEEP_READ", "READ", "SKIM", "SKIP"]:
        lines.extend([f"## {decision}", ""])
        items = grouped.get(decision, [])
        if not items:
            lines.extend(["No paragraphs in this category.", ""])
            continue
        for item in items:
            lines.append(
                f"- [[paragraphs/{_link_stem(paragraph_files[item.paragraph_id])}|"
                f"P{item.paragraph_id:04d} - {item.section_type}]]"
                f" - confidence {item.confidence:.2f}"
            )
        lines.append("")
    return "\n".join(lines)


def _escalation_matrix(
    report: ReviewReport, context: dict[str, str], paragraph_files: dict[int, str]
) -> str:
    matrix: dict[str, list[ParagraphAnalysis]] = defaultdict(list)
    for item in report.analyses:
        for role in item.escalation_questions:
            matrix[role].append(item)

    lines = [* _frontmatter("escalation-matrix", context), "# Escalation Matrix", ""]
    if not matrix:
        lines.append("No role-specific escalation questions were generated.")
        return "\n".join(lines)
    for role, items in matrix.items():
        lines.extend([f"## {role}", ""])
        for item in items:
            lines.append(
                f"- [[paragraphs/{_link_stem(paragraph_files[item.paragraph_id])}|"
                f"P{item.paragraph_id:04d} - {item.section_type} - {item.reading_decision}]]"
            )
        lines.append("")
    return "\n".join(lines)


def _management_memo(report: ReviewReport, context: dict[str, str]) -> str:
    memo = render_management_memo(report)
    return "\n".join([* _frontmatter("management-memo", context), memo])


def _legal_to_finance_notes(
    report: ReviewReport, context: dict[str, str], paragraph_files: dict[int, str]
) -> str:
    lines = [* _frontmatter("legal-to-finance-notes", context), "# Legal-to-Finance Notes", ""]
    for item in report.analyses:
        lines.extend(
            [
                f"## [[paragraphs/{_link_stem(paragraph_files[item.paragraph_id])}|P{item.paragraph_id:04d} - {item.section_type}]]",
                "",
                f"- Decision: `{item.reading_decision}`",
                f"- Plain-English meaning: {item.plain_english_meaning}",
                f"- Financial relevance: {item.financial_relevance}",
                f"- Briefing sentence: {item.suggested_management_briefing_sentence}",
                "",
            ]
        )
    return "\n".join(lines)


def _suggested_questions(
    report: ReviewReport, context: dict[str, str], paragraph_files: dict[int, str]
) -> str:
    lines = [* _frontmatter("suggested-questions", context), "# Suggested Questions", ""]
    by_role: dict[str, list[tuple[ParagraphAnalysis, str]]] = defaultdict(list)
    for item in report.analyses:
        for role, questions in item.escalation_questions.items():
            for question in questions:
                by_role[role].append((item, question))

    if not by_role:
        lines.append("No escalation questions were generated.")
        return "\n".join(lines)
    for role, entries in by_role.items():
        lines.extend([f"## {role}", ""])
        for item, question in entries:
            lines.append(
                f"- [[paragraphs/{_link_stem(paragraph_files[item.paragraph_id])}|"
                f"P{item.paragraph_id:04d}]] {question}"
            )
        lines.append("")
    return "\n".join(lines)


def _paragraph_note(item: ParagraphAnalysis, context: dict[str, str]) -> str:
    owners = _owners(item)
    owner_text = ", ".join(owners) if owners else "None"
    callout = _callout_for_decision(item.reading_decision)
    lines = [
        "---",
        f"title: { _yaml_scalar(_paragraph_title(item)) }",
        f"company: { _yaml_scalar(context['company']) }",
        f"ticker: { _yaml_scalar(context['ticker']) }",
        f"form: { _yaml_scalar(context['form']) }",
        f"year: { _yaml_scalar(context['year']) }",
        f"section_type: {item.section_type}",
        f"reading_decision: {item.reading_decision}",
        f"boilerplate_or_material: {item.boilerplate_or_material}",
        f"confidence: {item.confidence:.2f}",
        "tags:",
        "  - sec-filing",
        "  - legal-to-finance",
        f"  - decision/{_tag_value(item.reading_decision)}",
        f"  - section/{_tag_value(item.section_type)}",
        *[f"  - owner/{_tag_value(owner)}" for owner in owners],
        "---",
        "",
        f"# {_paragraph_title(item)}",
        "",
        f"> [!{callout}] Reading Decision",
        f"> {item.reading_decision}",
        "",
        f"decision:: {item.reading_decision}",
        f"section_type:: {item.section_type}",
        f"owner:: {owner_text}",
        f"confidence:: {item.confidence:.2f}",
        f"source:: {context['title']}",
        f"source_ref:: {item.source_ref}",
        "",
        "## Plain-English Meaning",
        "",
        item.plain_english_meaning,
        "",
        "## Business Relevance",
        "",
        item.business_relevance,
        "",
        "## Financial Relevance",
        "",
        item.financial_relevance,
        "",
        "## What To Compare",
        "",
        *[f"- {value}" for value in item.what_to_compare],
        "",
        "## Escalation Questions",
        "",
    ]
    if item.escalation_questions:
        for role, questions in item.escalation_questions.items():
            lines.extend([f"> [!question] {role}"])
            for question in questions:
                lines.append(f"> - {question}")
            lines.append("")
    else:
        lines.extend(["No role-specific escalation questions were generated.", ""])
    lines.extend(
        [
            "## Suggested Management Briefing Sentence",
            "",
            item.suggested_management_briefing_sentence,
            "",
            "## Source Excerpt",
            "",
            f"> {item.source_excerpt}",
            "",
        ]
    )
    return "\n".join(lines)


def _frontmatter(note_type: str, context: dict[str, str]) -> list[str]:
    lines = [
        "---",
        f"note_type: {note_type}",
        f"company: { _yaml_scalar(context['company']) }",
        f"ticker: { _yaml_scalar(context['ticker']) }",
        f"form: { _yaml_scalar(context['form']) }",
        f"year: { _yaml_scalar(context['year']) }",
        "tags:",
        "  - sec-filing",
        "  - legal-to-finance",
        f"  - note/{note_type}",
        "---",
        "",
    ]
    return lines


def _paragraph_file_name(item: ParagraphAnalysis) -> str:
    name = f"P{item.paragraph_id:04d} - {_file_label(item.section_type)} - {item.reading_decision}.md"
    return _sanitize_file_name(name)


def _paragraph_title(item: ParagraphAnalysis) -> str:
    return f"P{item.paragraph_id:04d} - {item.section_type.replace('_', ' ').title()} - {item.reading_decision}"


def _analysis_by_id(report: ReviewReport) -> dict[int, ParagraphAnalysis]:
    return {item.paragraph_id: item for item in report.analyses}


def _owner_counts(report: ReviewReport) -> Counter[str]:
    counts: Counter[str] = Counter()
    for item in report.analyses:
        for owner in _owners(item):
            counts[owner] += 1
    return counts


def _owners(item: ParagraphAnalysis) -> list[str]:
    owners = []
    for role in item.escalation_questions:
        cleaned = role.replace("Ask ", "").replace(" / ", "-")
        owners.append(cleaned)
    return owners


def _callout_for_decision(decision: str) -> str:
    return {
        "SKIP": "quote",
        "SKIM": "note",
        "READ": "info",
        "DEEP_READ": "warning",
        "ESCALATE": "danger",
    }.get(decision, "info")


def _disclaimer_callout(report: ReviewReport) -> str:
    return "\n".join(["> [!caution] Disclaimer", f"> {report.disclaimer}"])


def _safe_join(vault: Path, folder: str) -> Path:
    folder_path = Path(folder)
    if folder_path.is_absolute() or ".." in folder_path.parts:
        raise ValueError("Obsidian folder must be a relative path inside the vault.")
    return vault / folder_path


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _link_stem(file_name: str) -> str:
    return file_name[:-3] if file_name.endswith(".md") else file_name


def _file_label(value: str) -> str:
    return value.replace("_", "-")


def _tag_value(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower().replace("_", "-")).strip("-")


def _sanitize_file_name(value: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]+', "-", value)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:160]


def _yaml_scalar(value: str) -> str:
    escaped = value.replace('"', '\\"')
    return f'"{escaped}"'
