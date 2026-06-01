"""Markdown rendering for v0.4 management follow-up notes."""

from __future__ import annotations

from sec_filing_legal_decoder.schemas import RiskCardReport


def render_management_follow_up_report(
    report: RiskCardReport,
    lang: str = "en",
    term_style: str = "bilingual",
) -> str:
    """Render a concise management follow-up note."""

    if lang == "zh-CN":
        from .zh_cn_reports import render_management_follow_up_report_zh_cn

        return render_management_follow_up_report_zh_cn(report, term_style)

    lines = [
        "---",
        f'title: "Management Follow-Up - {_yaml_escape(report.document.title)}"',
        "tags:",
        "  - sec-filing",
        "  - legal-risk",
        "  - management-follow-up",
        "---",
        "",
        f"# Management Follow-Up: {report.document.title}",
        "",
        "> [!summary] Purpose",
        "> Use this as a triage checklist for Legal, Finance, Auditor, IR, Management, and Board follow-up. It is not a professional conclusion.",
        "",
        "## Priority Follow-Up",
        "",
    ]
    if not report.management_follow_up:
        lines.extend(["No management follow-up items were generated.", ""])
    else:
        for item in report.management_follow_up:
            lines.append(f"- {item}")
        lines.append("")
    lines.extend(
        [
            "## Disclosure Calibration",
            "",
        ]
    )
    if report.disclosure_consistency_questions:
        for question in report.disclosure_consistency_questions:
            lines.append(f"- {question}")
    else:
        lines.append("- No disclosure calibration questions were generated.")
    lines.extend(["", "> [!caution] Disclaimer", f"> {report.disclaimer}", ""])
    return "\n".join(lines).rstrip() + "\n"


def _yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')
