"""Evidence audit report for risk-card generation."""

from __future__ import annotations

from sec_filing_legal_decoder.schemas import RiskCardReport


def render_evidence_audit_report(report: RiskCardReport) -> str:
    """Render accepted and suppressed evidence for debugging card quality."""

    lines = [
        "---",
        f'title: "Evidence Audit - {_yaml_escape(report.document.title)}"',
        "tags:",
        "  - sec-filing",
        "  - legal-risk",
        "  - evidence-audit",
        "---",
        "",
        f"# Evidence Audit: {report.document.title}",
        "",
        "## Summary",
        "",
        "| Card | Domain | Evidence quality | Kept excerpts | Suppressed excerpts |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for card in report.risk_cards:
        lines.append(
            f"| {card.card_id} {card.title} | `{card.risk_domain}` | `{card.evidence_quality}` | "
            f"{len(card.source_excerpts)} | {len(card.weak_or_suppressed_sources)} |"
        )
    lines.append("")
    for card in report.risk_cards:
        lines.extend(
            [
                f"## {card.card_id} - {card.title}",
                "",
                f"- Evidence quality: `{card.evidence_quality}`",
                f"- Review posture: `{card.recommended_review_posture}`",
                f"- Summary: {card.evidence_summary}",
                "",
                "### Accepted Evidence",
                "",
            ]
        )
        if card.source_excerpts:
            for excerpt in card.source_excerpts:
                lines.extend(
                    [
                        f"- P{excerpt.paragraph_id:04d} `{excerpt.evidence_quality}` notes: {', '.join(excerpt.evidence_notes) or 'none'}",
                        f"  - {_trim(excerpt.excerpt, 240)}",
                    ]
                )
        else:
            lines.append("- No accepted evidence.")
        lines.extend(["", "### Suppressed Or Weak Evidence", ""])
        if card.weak_or_suppressed_sources:
            for excerpt in card.weak_or_suppressed_sources:
                lines.extend(
                    [
                        f"- P{excerpt.paragraph_id:04d} `{excerpt.evidence_quality}` notes: {', '.join(excerpt.evidence_notes) or 'none'}",
                        f"  - {_trim(excerpt.excerpt, 240)}",
                    ]
                )
        else:
            lines.append("- No suppressed evidence kept in the audit sample.")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _trim(value: str, limit: int) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def _yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')
