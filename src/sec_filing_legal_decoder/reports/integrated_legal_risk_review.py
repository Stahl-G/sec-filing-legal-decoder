"""Integrated read-through legal risk review report."""

from __future__ import annotations

from collections import defaultdict

from sec_filing_legal_decoder.schemas import RiskCard, RiskCardReport


def render_integrated_legal_risk_review(
    report: RiskCardReport,
    lang: str = "en",
    term_style: str = "bilingual",
) -> str:
    """Render the first-read narrative report for v0.3.0+ workflows."""

    if lang == "zh-CN":
        from .zh_cn_reports import render_integrated_legal_risk_review_zh_cn

        return render_integrated_legal_risk_review_zh_cn(report, term_style)

    read_first = [card for card in report.risk_cards if card.recommended_review_posture == "read-first"]
    appendix = [card for card in report.risk_cards if card.recommended_review_posture != "read-first"]
    lines = [
        *_frontmatter(report),
        f"# Legal Risk Review: {report.document.title}",
        "",
        "> [!summary] Purpose",
        "> This is the read-first legal-to-finance review. It synthesizes risk cards into a narrative review and keeps card-level details in the appendix.",
        "",
        "## Executive Takeaway",
        "",
        _executive_takeaway(report, read_first, appendix),
        "",
    ]
    lines.extend(_priority_map(read_first, appendix))
    lines.extend(_themes(read_first))
    lines.extend(_cross_risk_connections(read_first))
    lines.extend(_management_checklist(report))
    lines.extend(_appendix_notes(appendix))
    lines.extend(["> [!caution] Disclaimer", *_quote_lines(report.disclaimer), ""])
    return "\n".join(lines).rstrip() + "\n"


def _frontmatter(report: RiskCardReport) -> list[str]:
    return [
        "---",
        f'title: "{_yaml_escape("Legal Risk Review - " + report.document.title)}"',
        "tags:",
        "  - sec-filing",
        "  - legal-risk",
        "  - integrated-review",
        "  - sec-filing-legal-decoder/v0.3.0",
        f'form_type: "{_yaml_escape(report.document.form_type)}"',
        f'document_mode: "{_yaml_escape(report.document.mode)}"',
        f'source_path: "{_yaml_escape(report.document.source_path)}"',
        f"risk_cards: {len(report.risk_cards)}",
        "---",
        "",
    ]


def _executive_takeaway(
    report: RiskCardReport,
    read_first: list[RiskCard],
    appendix: list[RiskCard],
) -> str:
    if not report.risk_cards:
        return "No legal-risk cards were generated after evidence filtering."
    theme_names = ", ".join(card.title for card in read_first[:5])
    if not theme_names:
        theme_names = ", ".join(card.title for card in report.risk_cards[:5])
    suppressed = sum(len(card.weak_or_suppressed_sources) for card in report.risk_cards)
    return (
        f"The main read-first legal-risk themes are {theme_names}. "
        f"The report analyzed {report.coverage_summary.paragraphs_total} paragraph(s), routed out "
        f"{report.coverage_summary.financial_kpi_routed_out} ordinary finance KPI paragraph(s), and generated "
        f"{len(report.risk_cards)} issue-level card(s). {len(appendix)} card(s) are appendix-level or lower-priority. "
        f"{suppressed} weak, taxonomy-like, or non-issuer-specific source excerpt(s) were suppressed from the main narrative."
    )


def _priority_map(read_first: list[RiskCard], appendix: list[RiskCard]) -> list[str]:
    lines = [
        "## Risk Priority Map",
        "",
        "| Posture | Priority | Risk | Why it matters | Primary owners |",
        "| --- | --- | --- | --- | --- |",
    ]
    for card in read_first + appendix:
        lines.append(
            f"| {card.recommended_review_posture} | {card.priority} | {card.card_id} {card.title} | "
            f"{_table_cell(card.finance_reader_implication)} | {', '.join(card.owners)} |"
        )
    lines.append("")
    return lines


def _themes(cards: list[RiskCard]) -> list[str]:
    lines = ["## Read-First Legal Risk Themes", ""]
    if not cards:
        return lines + ["No cards met the read-first evidence threshold.", ""]
    for index, card in enumerate(cards, start=1):
        lines.extend(_theme(index, card))
    return lines


def _theme(index: int, card: RiskCard) -> list[str]:
    lines = [
        f"### {index}. {card.title}",
        "",
        f"- Card: `{card.card_id}`",
        f"- Domain: `{card.risk_domain}`",
        f"- Priority: `{card.priority}`",
        f"- Evidence quality: `{card.evidence_quality}`",
        f"- Owners: {', '.join(card.owners)}",
        "",
        "#### How This Differs From Ordinary Financial Analysis",
        "",
        card.financial_analysis_difference,
        "",
        "#### What The Filing Says",
        "",
    ]
    if card.issuer_specific_facts:
        lines.extend([f"- {fact}" for fact in card.issuer_specific_facts[:6]])
    else:
        lines.append("- No concise issuer-specific fact was extracted; inspect source excerpts before relying on this card.")
    lines.extend(
        [
            "",
            "#### Finance-Reader Implication",
            "",
            card.finance_reader_implication,
            "",
            "#### Legal / Audit / Disclosure Read",
            "",
            card.issuer_specific_interpretation,
            "",
            "#### What To Verify",
            "",
        ]
    )
    questions = _first_questions(card)
    if questions:
        lines.extend([f"- {question}" for question in questions])
    else:
        lines.append("- Assign Legal, Finance, Auditor, IR, or Management to confirm the source facts and disclosure posture.")
    lines.extend(
        [
            "",
            "#### What Not To Overstate",
            "",
            card.what_not_to_overstate,
            "",
            "#### Source Support",
            "",
        ]
    )
    for excerpt in card.source_excerpts[:3]:
        lines.append(
            f"- P{excerpt.paragraph_id:04d} (`{excerpt.evidence_quality}`): {_trim(excerpt.excerpt, 260)}"
        )
    lines.append("")
    return lines


def _cross_risk_connections(cards: list[RiskCard]) -> list[str]:
    lines = ["## Cross-Risk Connections", ""]
    domains = {card.risk_domain for card in cards}
    connections: list[str] = []
    if {"guarantees_commitments", "equity_dilution_control"}.issubset(domains):
        connections.append(
            "Guarantees or partner commitments should be reconciled with any warrants or equity-linked consideration, because the legal exposure and dilution/fair-value story may be connected."
        )
    if {"legal_proceedings_litigation", "disclosure_ir_consistency"}.issubset(domains):
        connections.append(
            "Litigation posture should be reconciled with public or management-facing wording so unresolved matters are not described as resolved or immaterial without support."
        )
    if {"material_contracts", "tax_cross_border"}.issubset(domains):
        connections.append(
            "Contract or acquisition-like arrangements should be checked against intangible asset, goodwill, amortization, and tax assumptions."
        )
    if {"cybersecurity_governance", "disclosure_ir_consistency"}.issubset(domains):
        connections.append(
            "Cybersecurity governance language should be framed as process and oversight disclosure unless the filing supports a material incident conclusion."
        )
    if not connections:
        connections.append("No strong cross-risk pattern was detected by the deterministic rules.")
    lines.extend([f"- {item}" for item in connections])
    lines.append("")
    return lines


def _management_checklist(report: RiskCardReport) -> list[str]:
    by_owner: dict[str, list[str]] = defaultdict(list)
    for card in report.risk_cards:
        if card.recommended_review_posture != "read-first":
            continue
        for owner in card.owners:
            by_owner[owner].append(f"{card.card_id} {card.title}: {card.suggested_management_follow_up}")

    lines = ["## Management Follow-Up Checklist", ""]
    if not by_owner:
        return lines + ["No read-first management follow-up items were generated.", ""]
    for owner, items in sorted(by_owner.items()):
        lines.extend([f"### {owner}", ""])
        lines.extend([f"- {item}" for item in items[:6]])
        lines.append("")
    return lines


def _appendix_notes(cards: list[RiskCard]) -> list[str]:
    lines = ["## Appendix-Level Or Lower-Confidence Cards", ""]
    if not cards:
        return lines + ["No appendix-level cards were generated.", ""]
    for card in cards:
        lines.append(
            f"- {card.card_id} {card.title}: `{card.priority}`, evidence `{card.evidence_quality}`. "
            f"{card.evidence_summary}"
        )
    lines.append("")
    return lines


def _first_questions(card: RiskCard) -> list[str]:
    result: list[str] = []
    for role, questions in card.questions.items():
        for question in questions[:1]:
            result.append(f"{role}: {question}")
    return result[:5]


def _quote_lines(text: str) -> list[str]:
    return [f"> {line}" if line else ">" for line in text.splitlines()]


def _table_cell(value: str) -> str:
    return _trim(value.replace("|", "/"), 170)


def _trim(value: str, limit: int) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def _yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')
