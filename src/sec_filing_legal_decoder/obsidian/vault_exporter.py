"""Obsidian note export for v0.2 legal risk cards."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from sec_filing_legal_decoder.reports import (
    render_escalation_questions_report,
    render_management_follow_up_report,
    render_risk_cards_json_report,
)
from sec_filing_legal_decoder.schemas import RiskCard, RiskCardReport


@dataclass(frozen=True)
class RiskCardObsidianOptions:
    """Options for writing v0.2 risk-card notes."""

    output_dir: Path
    company: str | None = None
    ticker: str | None = None
    form: str | None = None
    year: str | None = None


def export_risk_cards_to_obsidian(
    report: RiskCardReport,
    options: RiskCardObsidianOptions,
) -> list[Path]:
    """Write a compact Obsidian note set centered on risk cards."""

    base_dir = options.output_dir.expanduser()
    cards_dir = base_dir / "cards"
    data_dir = base_dir / "data"
    cards_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    context = _context(report, options)
    card_files = {card.card_id: _card_file_name(card) for card in report.risk_cards}
    payloads = {
        base_dir / "00 Legal Risk Dashboard.md": _dashboard(report, context, card_files),
        base_dir / "01 Escalation Matrix.md": render_escalation_questions_report(report),
        base_dir / "02 Management Follow-up.md": render_management_follow_up_report(report),
        data_dir / "legal-risk-cards.json": render_risk_cards_json_report(report),
    }
    written: list[Path] = []
    for path, content in payloads.items():
        _write(path, content)
        written.append(path)
    for card in report.risk_cards:
        path = cards_dir / card_files[card.card_id]
        _write(path, _card_note(card, context))
        written.append(path)
    return written


def _context(report: RiskCardReport, options: RiskCardObsidianOptions) -> dict[str, str]:
    return {
        "company": options.company or report.document.title,
        "ticker": options.ticker or "",
        "form": options.form or report.document.form_type,
        "year": options.year or "",
        "document_title": report.document.title,
        "source": report.document.source_path,
    }


def _dashboard(
    report: RiskCardReport,
    context: dict[str, str],
    card_files: dict[str, str],
) -> str:
    lines = [
        *_frontmatter("legal-risk-dashboard", context),
        f"# {context['company']} Legal Risk Dashboard".strip(),
        "",
        "> [!summary] v0.2 Legal Risk Cards",
        "> This dashboard links issue-level legal, regulatory, governance, audit, disclosure, debt, related-party, dilution, and material-contract risk cards.",
        "",
        "## Key Outputs",
        "",
        "- [[01 Escalation Matrix]]",
        "- [[02 Management Follow-up]]",
        "- [[data/legal-risk-cards.json|Structured JSON Archive]]",
        "",
        "## Filing Metadata",
        "",
        f"- Company: {context['company']}",
        f"- Ticker: {context['ticker'] or 'not specified'}",
        f"- Form: {context['form'] or report.document.form_type}",
        f"- Year: {context['year'] or 'not specified'}",
        f"- Document mode: `{report.document.mode}`",
        f"- Source: `{context['source']}`",
        "",
        "## Coverage Summary",
        "",
        "| Bucket | Count |",
        "| --- | ---: |",
        f"| Total paragraphs | {report.coverage_summary.paragraphs_total} |",
        f"| Filing admin skipped | {report.coverage_summary.paragraphs_skipped_admin} |",
        f"| Financial KPI routed out | {report.coverage_summary.financial_kpi_routed_out} |",
        f"| Risk-relevant paragraphs | {report.coverage_summary.risk_relevant_paragraphs} |",
        f"| Risk cards generated | {report.coverage_summary.risk_cards_generated} |",
        "",
        "## Risk Cards",
        "",
    ]
    if report.risk_cards:
        for card in report.risk_cards:
            lines.append(
                f"- [[cards/{_link_stem(card_files[card.card_id])}|{card.card_id} - {card.title}]] "
                f"(`{card.priority}`, `{card.risk_domain}`)"
            )
    else:
        lines.append("- No risk cards were generated.")
    lines.extend(["", "> [!caution] Disclaimer", f"> {report.disclaimer}", ""])
    return "\n".join(lines)


def _card_note(card: RiskCard, context: dict[str, str]) -> str:
    lines = [
        "---",
        f"title: {_yaml_scalar(card.title)}",
        f"company: {_yaml_scalar(context['company'])}",
        f"ticker: {_yaml_scalar(context['ticker'])}",
        f"form: {_yaml_scalar(context['form'])}",
        f"year: {_yaml_scalar(context['year'])}",
        f"risk_domain: {card.risk_domain}",
        f"priority: {card.priority}",
        f"reading_decision: {card.reading_decision}",
        f"confidence: {card.confidence:.2f}",
        "owners:",
        *[f"  - {owner}" for owner in card.owners],
        "tags:",
        "  - sec-filing",
        "  - legal-risk",
        f"  - risk-domain/{_tag_value(card.risk_domain)}",
        f"  - priority/{_tag_value(card.priority)}",
        *[f"  - owner/{_tag_value(owner)}" for owner in card.owners],
        "aliases:",
        f"  - {_yaml_scalar(card.card_id + ' ' + card.title)}",
        "---",
        "",
        f"# {card.card_id} - {card.title}",
        "",
        f"> [!{_callout(card.priority)}] {card.priority} / {card.reading_decision}",
        f"> Risk domain: `{card.risk_domain}`",
        "",
        "## Plain-Language Meaning",
        "",
        card.plain_language_meaning,
        "",
        "## Why Finance Readers Should Care",
        "",
        card.why_finance_readers_should_care,
        "",
        "## Legal / Regulatory / Audit / Governance Relevance",
        "",
        card.legal_or_audit_relevance,
        "",
        "## Financial Statement Linkage",
        "",
        *[f"- {item}" for item in card.financial_statement_linkage],
        "",
        "## Disclosure / IR Relevance",
        "",
        card.disclosure_ir_relevance,
        "",
        "## Questions To Ask",
        "",
    ]
    for role, questions in card.questions.items():
        lines.append(f"### {role}")
        lines.append("")
        for question in questions:
            lines.append(f"- {question}")
        lines.append("")
    lines.extend(
        [
            "## Suggested Management Follow-Up",
            "",
            card.suggested_management_follow_up,
            "",
            "## What Not To Overstate",
            "",
            card.what_not_to_overstate,
            "",
            "## Source Excerpts",
            "",
        ]
    )
    for excerpt in card.source_excerpts:
        lines.extend(
            [
                f"> [!quote] P{excerpt.paragraph_id:04d} `{excerpt.source_ref}`",
                f"> {excerpt.excerpt}",
                "",
            ]
        )
    return "\n".join(lines)


def _frontmatter(note_type: str, context: dict[str, str]) -> list[str]:
    return [
        "---",
        f"note_type: {note_type}",
        f"company: {_yaml_scalar(context['company'])}",
        f"ticker: {_yaml_scalar(context['ticker'])}",
        f"form: {_yaml_scalar(context['form'])}",
        f"year: {_yaml_scalar(context['year'])}",
        "tags:",
        "  - sec-filing",
        "  - legal-risk",
        f"  - note/{note_type}",
        "---",
        "",
    ]


def _card_file_name(card: RiskCard) -> str:
    return _sanitize_file_name(f"{card.card_id} - {card.title}.md")


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _callout(priority: str) -> str:
    return {
        "Critical": "danger",
        "High": "warning",
        "Medium": "info",
        "Low": "note",
        "Monitor": "note",
    }.get(priority, "info")


def _link_stem(file_name: str) -> str:
    return file_name[:-3] if file_name.endswith(".md") else file_name


def _sanitize_file_name(value: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]+', "-", value)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:160]


def _tag_value(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower().replace("_", "-")).strip("-")


def _yaml_scalar(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'
