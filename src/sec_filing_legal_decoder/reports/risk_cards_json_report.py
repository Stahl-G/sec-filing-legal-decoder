"""JSON rendering for v0.4 risk-card reports."""

from __future__ import annotations

import json

from sec_filing_legal_decoder.schemas import OverlayReport, RiskCardReport


def render_risk_cards_json_report(report: RiskCardReport | OverlayReport) -> str:
    """Render a risk-card or overlay report as pretty JSON."""

    return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)
