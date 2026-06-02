"""Materiality and priority heuristics for risk cards."""

from __future__ import annotations

import re


PRIORITY_ORDER = {
    "Monitor": 0,
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4,
}


DOMAIN_BASE_PRIORITY = {
    "audit_going_concern": "Critical",
    "internal_control_reporting": "High",
    "legal_proceedings_litigation": "High",
    "regulatory_trade_policy": "High",
    "related_party_governance": "High",
    "debt_liquidity_covenant": "High",
    "guarantees_commitments": "Medium",
    "equity_dilution_control": "Medium",
    "tax_cross_border": "Medium",
    "management_board_governance": "Medium",
    "disclosure_ir_consistency": "Medium",
    "cybersecurity_governance": "Medium",
    "material_contracts": "Medium",
}


ESCALATION_TERMS = (
    r"substantial doubt",
    r"going concern",
    r"material weakness",
    r"event of default",
    r"breach",
    r"subpoena",
    r"investigation",
    r"sanctions?",
    r"uflpa",
    r"section\s+337|\bitc\s*337\b",
)

MATERIAL_TERMS = (
    r"accrued liability",
    r"reasonably possible",
    r"probable loss",
    r"default",
    r"waiver",
    r"material adverse",
    r"not in compliance",
    r"cannot assure",
    r"minimum purchase",
    r"guarantee",
    r"convertible notes?",
    r"earnout",
)


def priority_for(domain: str, text: str, paragraph_count: int) -> str:
    """Return reader-review priority for a risk card."""

    priority = DOMAIN_BASE_PRIORITY.get(domain, "Medium")
    lowered = text.lower()
    if _has_any(lowered, ESCALATION_TERMS):
        priority = _max_priority(priority, "High")
    if domain == "audit_going_concern" and re.search(r"substantial doubt|going concern", lowered):
        priority = "Critical"
    if domain == "legal_proceedings_litigation" and re.search(r"subpoena|investigation|section\s+337|\bptab\b", lowered):
        priority = _max_priority(priority, "High")
    if domain in {"material_contracts", "guarantees_commitments", "equity_dilution_control"} and re.search(
        r"\$[\d,.]+\s*(?:million|billion)", text, flags=re.IGNORECASE
    ):
        priority = _max_priority(priority, "High")
    if domain == "tax_cross_border" and re.search(
        r"valuation allowance|deferred tax assets?|uncertain tax|tax benefit|more[- ]likely[- ]than[- ]not",
        lowered,
    ):
        priority = _max_priority(priority, "High")
    if domain == "disclosure_ir_consistency" and not _has_any(lowered, ESCALATION_TERMS):
        priority = _max_priority("Low", priority)
    if paragraph_count >= 4:
        priority = _max_priority(priority, "High")
    return priority


def reading_decision_for(priority: str) -> str:
    """Map issue priority to reader action."""

    if priority == "Critical":
        return "ESCALATE"
    if priority == "High":
        return "DEEP_READ"
    if priority == "Medium":
        return "READ"
    if priority == "Low":
        return "SKIM"
    return "SKIM"


def materiality_for(text: str, priority: str) -> str:
    """Return boilerplate/material posture without legal conclusions."""

    lowered = text.lower()
    if priority in {"Critical", "High"}:
        return "potentially_material"
    if _has_any(lowered, MATERIAL_TERMS):
        return "potentially_material"
    if "safe harbor" in lowered or "forward-looking" in lowered:
        return "likely_boilerplate_but_disclosure_relevant"
    return "review_needed"


def confidence_for(text: str, paragraph_count: int, subdomain_count: int) -> float:
    """Score support strength for a deterministic card."""

    score = 0.66
    if paragraph_count >= 2:
        score += 0.06
    if paragraph_count >= 4:
        score += 0.05
    if subdomain_count:
        score += min(subdomain_count, 3) * 0.03
    if _has_any(text.lower(), ESCALATION_TERMS):
        score += 0.08
    return min(round(score, 2), 0.92)


def _has_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _max_priority(left: str, right: str) -> str:
    return left if PRIORITY_ORDER[left] >= PRIORITY_ORDER[right] else right
