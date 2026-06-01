"""Markdown rendering for v0.2 legal risk cards."""

from __future__ import annotations

from collections import Counter

from sec_filing_legal_decoder.schemas import RiskCard, RiskCardReport


def render_legal_risk_cards_report(report: RiskCardReport) -> str:
    """Render the main v0.2 Markdown report in Obsidian-friendly format."""

    lines: list[str] = [
        *_frontmatter(report),
        f"# Legal Risk Cards: {report.document.title}",
        "",
        "> [!summary] v0.2 Scope",
        "> This report does not summarize ordinary revenue, margin, EPS, valuation, or peer-comparison topics.",
        "> It converts legal, regulatory, governance, audit, disclosure, debt, related-party, dilution, and material-contract language into finance-readable risk cards.",
        "",
        "## Filing Context",
        "",
        f"- Source: `{report.document.source_path}`",
        f"- Parser backend: `{report.document.parser_backend}`",
        f"- Form type: `{report.document.form_type}`",
        f"- Document mode: `{report.document.mode}`",
        "",
    ]
    lines.extend(_coverage_table(report))
    lines.extend(_priority_snapshot(report))
    lines.extend(_cards(report.risk_cards))
    lines.extend(_disclosure_questions(report))
    lines.extend(["> [!caution] Disclaimer", *_quote_lines(report.disclaimer), ""])
    return "\n".join(lines).rstrip() + "\n"


def _frontmatter(report: RiskCardReport) -> list[str]:
    return [
        "---",
        f'title: "{_yaml_escape("Legal Risk Cards - " + report.document.title)}"',
        "tags:",
        "  - sec-filing",
        "  - legal-risk",
        "  - sec-filing-legal-decoder/v0.2",
        f'form_type: "{_yaml_escape(report.document.form_type)}"',
        f'document_mode: "{_yaml_escape(report.document.mode)}"',
        f'source_path: "{_yaml_escape(report.document.source_path)}"',
        f"risk_cards: {len(report.risk_cards)}",
        "---",
        "",
    ]


def _coverage_table(report: RiskCardReport) -> list[str]:
    coverage = report.coverage_summary
    return [
        "## Coverage Summary",
        "",
        "| Routing bucket | Count |",
        "| --- | ---: |",
        f"| Total paragraphs | {coverage.paragraphs_total} |",
        f"| Filing admin skipped | {coverage.paragraphs_skipped_admin} |",
        f"| Ordinary financial KPI routed out | {coverage.financial_kpi_routed_out} |",
        f"| Business update routed out | {coverage.business_update_routed_out} |",
        f"| Risk-relevant paragraphs | {coverage.risk_relevant_paragraphs} |",
        f"| Risk cards generated | {coverage.risk_cards_generated} |",
        "",
    ]


def _priority_snapshot(report: RiskCardReport) -> list[str]:
    counts = Counter(card.priority for card in report.risk_cards)
    lines = ["## Priority Snapshot", "", "| Priority | Cards |", "| --- | ---: |"]
    for priority in ["Critical", "High", "Medium", "Low", "Monitor"]:
        lines.append(f"| {priority} | {counts.get(priority, 0)} |")
    lines.append("")
    return lines


def _cards(cards: list[RiskCard]) -> list[str]:
    lines = ["## Risk Cards", ""]
    if not cards:
        return lines + [
            "No legal-risk cards were generated. Ordinary finance KPI paragraphs may have been routed out.",
            "",
        ]
    for card in cards:
        lines.extend(_card(card))
    return lines


def _card(card: RiskCard) -> list[str]:
    callout = _callout(card.priority)
    lines = [
        f"### {card.card_id} - {card.title}",
        "",
        f"> [!{callout}] {card.priority} / {card.reading_decision}",
        f"> Domain: `{card.risk_domain}`",
        f"> Owners: {', '.join(card.owners)}",
        f"> Confidence: {card.confidence:.2f}",
        f"> Evidence quality: `{card.evidence_quality}`",
        f"> Review posture: `{card.recommended_review_posture}`",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Risk domain | `{card.risk_domain}` |",
        f"| Subdomains | {', '.join(f'`{item}`' for item in card.subdomains) or 'none detected'} |",
        f"| Boilerplate or material? | `{card.boilerplate_or_material}` |",
        f"| Evidence quality | `{card.evidence_quality}` |",
        f"| Review posture | `{card.recommended_review_posture}` |",
        f"| Source paragraphs | {', '.join(f'P{pid:04d}' for pid in card.source_paragraphs)} |",
        "",
        "#### Issuer-Specific Interpretation",
        "",
        card.issuer_specific_interpretation or card.plain_language_meaning,
        "",
        "#### Finance-Reader Implication",
        "",
        card.finance_reader_implication or card.why_finance_readers_should_care,
        "",
        "#### What The Filing Says",
        "",
        *([f"- {fact}" for fact in card.issuer_specific_facts] or ["- No concise issuer-specific facts were extracted."]),
        "",
        "#### Plain-Language Meaning",
        "",
        card.plain_language_meaning,
        "",
        "#### Why Finance Readers Should Care",
        "",
        card.why_finance_readers_should_care,
        "",
        "#### Legal / Regulatory / Audit / Governance Relevance",
        "",
        card.legal_or_audit_relevance,
        "",
        "#### Financial Statement Linkage",
        "",
        *[f"- {item}" for item in card.financial_statement_linkage],
        "",
        "#### Disclosure / IR Relevance",
        "",
        card.disclosure_ir_relevance,
        "",
        "#### Questions To Ask",
        "",
    ]
    for role, questions in card.questions.items():
        lines.extend([f"> [!question] {role}"])
        for question in questions:
            lines.append(f"> - {question}")
        lines.append("")
    lines.extend(
        [
            "#### Suggested Management Follow-Up",
            "",
            card.suggested_management_follow_up,
            "",
            "#### What Not To Overstate",
            "",
            card.what_not_to_overstate,
            "",
            "#### Source Excerpts",
            "",
        ]
    )
    for excerpt in card.source_excerpts:
        lines.extend(
            [
                f"> [!quote] P{excerpt.paragraph_id:04d} `{excerpt.source_ref}` / evidence `{excerpt.evidence_quality}`",
                *_quote_lines(excerpt.excerpt),
                "",
            ]
        )
    return lines


def _disclosure_questions(report: RiskCardReport) -> list[str]:
    lines = ["## Disclosure Consistency Questions", ""]
    if not report.disclosure_consistency_questions:
        return lines + ["No disclosure consistency questions were generated.", ""]
    for question in report.disclosure_consistency_questions:
        lines.append(f"- {question}")
    lines.append("")
    return lines


def _callout(priority: str) -> str:
    return {
        "Critical": "danger",
        "High": "warning",
        "Medium": "attention",
        "Low": "info",
        "Monitor": "note",
    }.get(priority, "info")


def _quote_lines(text: str) -> list[str]:
    return [f"> {line}" if line else ">" for line in text.splitlines()]


def _yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')
