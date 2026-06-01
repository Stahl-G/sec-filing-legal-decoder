"""Issuer-profile priority adjustments for source-only risk cards."""

from __future__ import annotations

import re

from .materiality_rules import _max_priority


DEFAULT_ISSUER_PROFILE = "general"

ISSUER_PROFILES = {
    "general",
    "small-issuer",
    "foreign-private-issuer",
    "spac-de-spac",
    "manufacturing",
    "solar-manufacturing",
}


PROFILE_PRIORITY_RULES: dict[str, tuple[tuple[str, str, str], ...]] = {
    "small-issuer": (
        ("audit_going_concern", r"going concern|substantial doubt|working capital deficit", "Critical"),
        ("internal_control_reporting", r"material weakness|unremediated|icfr|late filing|restatement|auditor", "Critical"),
        ("debt_liquidity_covenant", r"default|covenant|waiver|working capital|short[- ]term liquidity", "Critical"),
        ("related_party_governance", r"related[- ]part|affiliate|support|loan|guarantee", "High"),
        ("equity_dilution_control", r"warrants?|convertible|earnout|dilution", "High"),
    ),
    "foreign-private-issuer": (
        ("management_board_governance", r"foreign private issuer|fpi|home[- ]country|exemption", "High"),
        ("internal_control_reporting", r"sox|icfr|attestation|exemption|material weakness", "High"),
        ("related_party_governance", r"related[- ]part|affiliate|home[- ]country", "High"),
        ("tax_cross_border", r"cross[- ]border|withholding|deferred tax|valuation allowance|remittance", "High"),
        ("regulatory_trade_policy", r"trade|tariff|customs|export control|sanctions", "High"),
    ),
    "spac-de-spac": (
        ("equity_dilution_control", r"sponsor|earnout|warrants?|pipe|registration rights?|redemption|lock[- ]up", "High"),
        ("material_contracts", r"business combination|legacy|registration rights?|lock[- ]up", "High"),
        ("audit_going_concern", r"going concern|substantial doubt", "Critical"),
        ("internal_control_reporting", r"material weakness|icfr", "High"),
    ),
    "manufacturing": (
        ("guarantees_commitments", r"purchase obligations?|capacity commitments?|capex|factory|supplier|customer concentration", "High"),
        ("material_contracts", r"supply agreement|capacity|customer concentration|supplier concentration|factory ramp", "High"),
        ("regulatory_trade_policy", r"trade|tariff|customs|import|export|forced labor", "High"),
        ("debt_liquidity_covenant", r"liquidity strain|expansion|capex|working capital|covenant", "High"),
    ),
    "solar-manufacturing": (
        ("regulatory_trade_policy", r"tariff|customs|forced labor|uflpa|ad[/-]?cvd|itc|ira|tax credit", "High"),
        ("guarantees_commitments", r"factory ramp|capacity|purchase obligations?|capex|supplier|customer concentration", "High"),
        ("material_contracts", r"customer concentration|supplier concentration|offtake|supply agreement", "High"),
        ("debt_liquidity_covenant", r"liquidity|capex|working capital|expansion", "High"),
    ),
}


def validate_issuer_profile(profile: str) -> str:
    """Validate a CLI issuer profile."""

    if profile not in ISSUER_PROFILES:
        allowed = ", ".join(sorted(ISSUER_PROFILES))
        raise ValueError(f"Unsupported --issuer-profile: {profile}. Choose one of: {allowed}.")
    return profile


def apply_issuer_profile(profile: str, domain: str, text: str, priority: str) -> str:
    """Adjust priority based on issuer profile without creating unsupported cards."""

    validate_issuer_profile(profile)
    if profile == DEFAULT_ISSUER_PROFILE:
        return priority
    adjusted = priority
    lowered = text.lower()
    for rule_domain, pattern, target_priority in PROFILE_PRIORITY_RULES.get(profile, ()):
        if domain == rule_domain and re.search(pattern, lowered, flags=re.IGNORECASE):
            adjusted = _max_priority(adjusted, target_priority)
    return adjusted
