"""Rules for ordinary finance KPI text routed away from legal decoding."""

from __future__ import annotations

import re


KPI_PATTERNS: tuple[str, ...] = (
    r"\brevenues?\b|\bnet sales\b",
    r"gross profit|gross margin",
    r"\beps\b|earnings per share",
    r"shipment volume|shipments?",
    r"operating expenses?",
    r"cash flow from operations|operating cash flow",
    r"net income|net loss",
    r"segment revenue",
    r"cost of revenue|cost of sales",
    r"adjusted ebitda|\bebitda\b",
    r"\bguidance\b",
)


BUSINESS_UPDATE_PATTERNS: tuple[str, ...] = (
    r"reports? .* quarter results?",
    r"announces? .* financial results?",
    r"first quarter results?",
    r"second quarter results?",
    r"third quarter results?",
    r"fourth quarter results?",
    r"fiscal year results?",
)


def is_ordinary_financial_kpi(text: str) -> bool:
    """Return True for KPI-only finance analysis content."""

    lowered = " ".join(text.lower().split())
    return any(re.search(pattern, lowered) for pattern in KPI_PATTERNS)


def is_business_update(text: str) -> bool:
    """Return True for ordinary earnings-release update language."""

    lowered = " ".join(text.lower().split())
    return any(re.search(pattern, lowered) for pattern in BUSINESS_UPDATE_PATTERNS)
