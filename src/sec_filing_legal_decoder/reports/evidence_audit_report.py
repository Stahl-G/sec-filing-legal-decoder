"""Evidence audit report for risk-card generation."""

from __future__ import annotations

from sec_filing_legal_decoder.schemas import RiskCardReport


def render_evidence_audit_report(report: RiskCardReport, lang: str = "en") -> str:
    """Render accepted and suppressed evidence for debugging card quality."""

    if lang == "zh-CN":
        return _render_zh_cn(report)

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


def _render_zh_cn(report: RiskCardReport) -> str:
    lines = [
        "---",
        f'title: "证据审计 - {_yaml_escape(report.document.title)}"',
        "tags:",
        "  - sec-filing",
        "  - legal-risk",
        "  - evidence-audit",
        "  - zh-CN",
        "---",
        "",
        f"# 证据审计: {report.document.title}",
        "",
        "## 汇总",
        "",
        "| 卡片 | 风险域 | 证据质量 | 保留原文 | 压低或排除原文 |",
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
                f"- 证据质量：`{card.evidence_quality}`",
                f"- 阅读位置：`{_posture(card.recommended_review_posture)}`",
                f"- 摘要：{card.evidence_summary}",
                "",
                "### 保留证据",
                "",
            ]
        )
        if card.source_excerpts:
            for excerpt in card.source_excerpts:
                notes = ", ".join(excerpt.evidence_notes) or "无"
                lines.extend(
                    [
                        f"- P{excerpt.paragraph_id:04d} `{excerpt.evidence_quality}` notes: {notes}",
                        f"  - {_trim(excerpt.excerpt, 240)}",
                    ]
                )
        else:
            lines.append("- 无保留证据。")
        lines.extend(["", "### 压低或弱证据", ""])
        if card.weak_or_suppressed_sources:
            for excerpt in card.weak_or_suppressed_sources:
                notes = ", ".join(excerpt.evidence_notes) or "无"
                lines.extend(
                    [
                        f"- P{excerpt.paragraph_id:04d} `{excerpt.evidence_quality}` notes: {notes}",
                        f"  - {_trim(excerpt.excerpt, 240)}",
                    ]
                )
        else:
            lines.append("- 审计样本中没有保留压低证据。")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _posture(value: str) -> str:
    if value == "read-first":
        return "优先阅读"
    if value == "appendix":
        return "附录级"
    return value


def _trim(value: str, limit: int) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def _yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')
