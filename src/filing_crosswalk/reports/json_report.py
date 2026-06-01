"""JSON report rendering."""

from __future__ import annotations

import json

from filing_crosswalk.schemas import ReviewReport


def render_json_report(report: ReviewReport) -> str:
    """Render a structured review report as pretty JSON."""

    return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)
