"""Markdown rendering for v0.4 escalation questions."""

from __future__ import annotations

from collections import defaultdict

from sec_filing_legal_decoder.schemas import RiskCard, RiskCardReport


def render_escalation_questions_report(
    report: RiskCardReport,
    lang: str = "en",
    term_style: str = "bilingual",
) -> str:
    """Render issue-level escalation questions."""

    if lang == "zh-CN":
        from .zh_cn_reports import render_escalation_questions_report_zh_cn

        return render_escalation_questions_report_zh_cn(report, term_style)

    lines = [
        "---",
        f'title: "Escalation Questions - {_yaml_escape(report.document.title)}"',
        "tags:",
        "  - sec-filing",
        "  - legal-risk",
        "  - escalation-questions",
        "---",
        "",
        f"# Escalation Questions: {report.document.title}",
        "",
    ]
    by_owner = _questions_by_owner(report.risk_cards)
    if not by_owner:
        lines.extend(["No escalation questions were generated.", ""])
        return "\n".join(lines)
    for owner, entries in by_owner.items():
        lines.extend([f"## {owner}", ""])
        for card, question in entries:
            lines.append(f"- **{card.card_id} {card.title}** (`{card.priority}`): {question}")
        lines.append("")
    lines.extend(["> [!caution] Disclaimer", f"> {report.disclaimer}", ""])
    return "\n".join(lines).rstrip() + "\n"


def _questions_by_owner(cards: list[RiskCard]) -> dict[str, list[tuple[RiskCard, str]]]:
    by_owner: dict[str, list[tuple[RiskCard, str]]] = defaultdict(list)
    for card in cards:
        for owner, questions in card.questions.items():
            cleaned_owner = owner.replace("Ask ", "")
            for question in questions:
                by_owner[cleaned_owner].append((card, question))
    return dict(by_owner)


def _yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')
