"""Boilerplate vs material triage rules."""

from __future__ import annotations

import re
from dataclasses import dataclass


BOILERPLATE_SIGNALS: tuple[tuple[str, str], ...] = (
    ("hypothetical_may", r"\bmay\b"),
    ("hypothetical_could", r"\bcould\b"),
    ("from_time_to_time", r"from time to time"),
    ("generic_adverse_effect", r"adversely affect"),
    ("cannot_assure", r"cannot assure"),
)

MATERIAL_SIGNALS: tuple[tuple[str, str], ...] = (
    ("actual_has_or_is", r"\b(has|have|is|are|was|were)\b"),
    ("received_notice", r"received (a )?(notice|subpoena|civil investigative demand)"),
    ("investigation", r"investigation|inquiry|subpoena"),
    ("default_or_breach", r"default|breach|event of default|waiver"),
    ("material_weakness", r"material weakness|ineffective internal control"),
    ("going_concern", r"going concern|substantial doubt"),
    ("accrual_or_liability", r"accrued liability|reasonably possible|probable loss"),
    ("specific_amount", r"(\$|usd|million|billion|thousand|\d+[.,]?\d*\s?%)"),
    ("named_regulator", r"\b(sec|doj|department of justice|ftc|fda|epa|irs)\b"),
    ("formal_proceeding", r"lawsuit|complaint|settlement|consent order|proceeding"),
    ("actual_commitment", r"committed to purchase|minimum purchase|guaranteed"),
)


@dataclass(frozen=True)
class TriageResult:
    """Result of boilerplate/material triage."""

    boilerplate_or_material: str
    reading_decision: str
    confidence: float
    signals: list[str]


def triage_paragraph(paragraph: str, section_type: str) -> TriageResult:
    """Classify paragraph materiality posture and reading decision.

    The output is a reading aid and intentionally avoids definitive legal
    conclusions.
    """

    text = paragraph.lower()
    boilerplate = [name for name, pattern in BOILERPLATE_SIGNALS if re.search(pattern, text)]
    material = [name for name, pattern in MATERIAL_SIGNALS if re.search(pattern, text)]

    if section_type == "forward_looking_statement" and not _has_specific_fact(material):
        return TriageResult(
            "likely_boilerplate",
            "SKIM",
            0.72,
            sorted(set(boilerplate + ["forward_looking_safe_harbor"])),
        )

    if section_type == "generic_boilerplate" and not _has_specific_fact(material):
        return TriageResult(
            "likely_boilerplate",
            "SKIP",
            0.7,
            sorted(set(boilerplate)),
        )

    if _requires_escalation(material, section_type):
        return TriageResult(
            "potentially_material",
            "ESCALATE",
            0.86,
            sorted(set(material + boilerplate)),
        )

    if material:
        return TriageResult(
            "potentially_material",
            "DEEP_READ",
            0.78,
            sorted(set(material + boilerplate)),
        )

    if boilerplate:
        return TriageResult(
            "likely_boilerplate",
            "SKIM",
            0.65,
            sorted(set(boilerplate)),
        )

    if section_type == "unknown":
        return TriageResult("uncertain", "READ", 0.45, [])

    return TriageResult("review_needed", "READ", 0.6, [])


def _has_specific_fact(signals: list[str]) -> bool:
    specific = {
        "received_notice",
        "investigation",
        "default_or_breach",
        "material_weakness",
        "going_concern",
        "accrual_or_liability",
        "specific_amount",
        "named_regulator",
        "formal_proceeding",
        "actual_commitment",
    }
    return bool(specific.intersection(signals))


def _requires_escalation(signals: list[str], section_type: str) -> bool:
    severe = {
        "received_notice",
        "investigation",
        "default_or_breach",
        "material_weakness",
        "going_concern",
        "accrual_or_liability",
    }
    if severe.intersection(signals):
        return True
    if section_type in {"debt_covenant_default", "internal_control"} and signals:
        return True
    return False
