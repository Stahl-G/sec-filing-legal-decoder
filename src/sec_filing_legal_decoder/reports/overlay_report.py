"""Markdown rendering for v0.2 review-overlay reports."""

from __future__ import annotations

from collections import Counter

from sec_filing_legal_decoder.schemas import OverlayReport


def render_overlay_report(report: OverlayReport) -> str:
    """Render an overlay report comparing filing risk cards to existing analysis."""

    counts = Counter(finding.status for finding in report.findings)
    lines = [
        "---",
        f'title: "Review Overlay - {_yaml_escape(report.document.title)}"',
        "tags:",
        "  - sec-filing",
        "  - legal-risk",
        "  - review-overlay",
        "---",
        "",
        f"# Review Overlay: {report.document.title}",
        "",
        "> [!summary] Purpose",
        "> This report checks whether an existing finance or earnings analysis leaves legal, governance, audit, or disclosure risk under-explained.",
        "",
        "## Inputs",
        "",
        f"- Filing source: `{report.document.source_path}`",
        f"- Existing analysis: `{report.analysis_path}`",
        f"- Document mode: `{report.document.mode}`",
        "",
        "## Overlay Status Snapshot",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for status in [
        "not_covered",
        "mentioned_but_under_explained",
        "needs_wording_review",
        "covered_for_triage",
    ]:
        lines.append(f"| `{status}` | {counts.get(status, 0)} |")
    lines.extend(["", "## Findings", ""])
    if not report.findings:
        lines.extend(["No risk-card overlay findings were generated.", ""])
    for finding in report.findings:
        lines.extend(
            [
                f"### {finding.risk_card_id} - {finding.risk_card_title}",
                "",
                f"- Status: `{finding.status}`",
                f"- Finding: {finding.finding}",
                f"- Suggested safer wording: {finding.suggested_safer_wording}",
                "",
            ]
        )
    lines.extend(["> [!caution] Disclaimer", f"> {report.disclaimer}", ""])
    return "\n".join(lines).rstrip() + "\n"


def _yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')
