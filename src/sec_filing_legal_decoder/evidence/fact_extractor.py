"""Extract issuer-specific facts from accepted source evidence."""

from __future__ import annotations

import re


DOMAIN_HINTS: dict[str, tuple[str, ...]] = {
    "audit_going_concern": ("going concern", "substantial doubt", "ability to continue", "liquidity"),
    "internal_control_reporting": ("material weakness", "internal control", "disclosure controls", "ineffective", "remediation"),
    "equity_dilution_control": ("warrant", "rsu", "psu", "dilut", "convertible", "earnout"),
    "guarantees_commitments": ("guarantee", "commitment", "escrow", "maximum gross exposure", "indemnification"),
    "tax_cross_border": ("tax", "deferred", "valuation allowance", "uncertain", "transfer pricing"),
    "management_board_governance": ("board", "director", "officer", "fiduciary", "insider trading", "committee"),
    "disclosure_ir_consistency": ("uncertainties", "cannot", "differ materially", "forward-looking", "assure"),
    "related_party_governance": ("related", "affiliate", "common control", "controlled"),
    "legal_proceedings_litigation": ("litigation", "lawsuit", "claims", "proceeding", "probable", "reasonably possible"),
    "regulatory_trade_policy": ("uflpa", "ad/cvd", "anti-dumping", "countervailing", "tariff", "ieepa", "itc 337", "section 337", "customs", "sanctions"),
    "debt_liquidity_covenant": ("debt", "default", "covenant", "liquidity", "guarantee", "credit"),
    "cybersecurity_governance": ("cyber", "incident", "vendor", "board", "information security"),
    "material_contracts": ("license agreement", "non-exclusive", "customer contracts", "goodwill", "intangible", "useful life"),
}


def extract_issuer_facts(texts: list[str], domain: str, limit: int = 6) -> list[str]:
    """Extract concise source-backed facts from accepted evidence text."""

    hints = DOMAIN_HINTS.get(domain, ())
    facts: list[str] = []
    for text in texts:
        for sentence in _sentences(text):
            compact = " ".join(sentence.split())
            lowered = compact.lower()
            if _is_fact_candidate(compact, lowered, hints):
                facts.append(_trim_fact(compact))
            if len(facts) >= limit:
                return _dedupe(facts)
    return _dedupe(facts)[:limit]


def _is_fact_candidate(sentence: str, lowered: str, hints: tuple[str, ...]) -> bool:
    if len(sentence.split()) < 8:
        return False
    if any(hint in lowered for hint in hints):
        return True
    if re.search(r"\$[\d,.]+\s*(?:million|billion|thousand)?", sentence, flags=re.IGNORECASE):
        return True
    if re.search(r"\b\d+\s+to\s+\d+\s+years?\b", lowered):
        return True
    if re.search(r"\b(?:not material|not probable|reasonably possible|cannot be reasonably estimated|no accrued contingent liabilities)\b", lowered):
        return True
    return False


def _sentences(text: str) -> list[str]:
    normalized = " ".join(text.split())
    pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", normalized)
    if len(pieces) == 1 and len(normalized) > 280:
        pieces = re.split(r";\s+|,\s+(?=(?:and|while|which|with|including)\b)", normalized)
    return [piece.strip() for piece in pieces if piece.strip()]


def _trim_fact(text: str, limit: int = 280) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        key = value.lower()
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result
