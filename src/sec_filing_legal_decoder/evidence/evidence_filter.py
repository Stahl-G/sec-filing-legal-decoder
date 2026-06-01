"""Score whether a paragraph is useful source evidence for a risk card."""

from __future__ import annotations

import re
from dataclasses import dataclass


TAXONOMY_PATTERNS: tuple[str, ...] = (
    r"\[line items?\]$",
    r"\[text block\]$",
    r"\[abstract\]$",
    r"\(details\)$",
    r"\(tables?\)$",
    r"\(polic(?:y|ies)\)$",
    r"^amount of\b",
    r"^aggregate (?:par|total|market|fair) value\b",
    r"^carrying value as of the balance sheet date\b",
    r"^maximum borrowing capacity under the credit facility\b",
    r"^boolean flag\b",
    r"^the tax identification number\b",
    r"^a unique \d+[- ]digit sec-issued value\b",
    r"^for the edgar submission types\b",
    r"^the entire disclosure for information about\b",
    r"^the aggregate total costs related to\b",
    r"^business combination, asset acquisition, transaction between entities under common control\b",
)

HEADING_ONLY_PATTERNS: tuple[str, ...] = (
    r"^[a-z0-9 ,/&().'-]+ - [a-z0-9 ,/&().'-]+$",
    r"^[a-z0-9 ,/&().'-]+ \| [a-z0-9 ,/&().'-]+$",
)

GENERIC_POLICY_PATTERNS: tuple[str, ...] = (
    r"the preparation of financial statements in conformity with u\.s\. gaap requires management to make estimates",
    r"actual results could differ materially from our estimates",
    r"we evaluate our estimates, including those related to accounts receivable",
)

DOMAIN_SUPPORT_PATTERNS: dict[str, tuple[str, ...]] = {
    "audit_going_concern": (
        r"\bgoing concern\b",
        r"\bsubstantial doubt\b",
        r"\bability to continue\b",
        r"\bliquidity\b",
        r"\bworking capital deficit\b",
    ),
    "internal_control_reporting": (
        r"\bmaterial weakness\b",
        r"\binternal control over financial reporting\b",
        r"\bdisclosure controls?\b",
        r"\bineffective\b",
        r"\bremediation\b",
        r"\bicfr\b",
        r"\bsox\b",
    ),
    "equity_dilution_control": (
        r"\bwarrants?\b",
        r"\brsus?\b|restricted stock units?",
        r"\bpsus?\b|performance stock units?",
        r"\bdilut(?:e|ion)\b",
        r"\bconvertible notes?\b",
        r"\bearnout\b",
        r"\bin exchange for warrants?\b",
    ),
    "guarantees_commitments": (
        r"\bguarantee(?:d|s)?\b",
        r"\bmaximum gross exposure\b",
        r"\bescrow\b",
        r"\bindemnification\b",
        r"\bpurchase obligations?\b",
        r"\bcommitments?\b",
        r"\bcontingenc(?:y|ies)\b",
    ),
    "tax_cross_border": (
        r"\buncertain tax positions?\b",
        r"\bincome tax expense\b",
        r"\bdeferred tax\b",
        r"\btax authority\b",
        r"\btransfer pricing\b",
        r"\bvaluation allowance\b",
        r"\brepatriation\b",
    ),
    "management_board_governance": (
        r"\bboard\b",
        r"\baudit committee\b",
        r"\bdirectors?\b",
        r"\bofficers?\b",
        r"\bbreach of fiduciary duty\b",
        r"\binsider trading\b",
        r"\bindependence\b",
    ),
    "disclosure_ir_consistency": (
        r"\bcannot assure\b",
        r"\bno assurance\b",
        r"\bcould differ materially\b",
        r"\bforward-looking\b",
        r"\brisk factors?\b",
        r"\buncertainties\b",
    ),
    "related_party_governance": (
        r"\brelated[- ]part(?:y|ies)\b",
        r"(?<!non-)affiliates?\b",
        r"\bcommon control\b",
        r"\bcontrolled by\b",
        r"\bvariable interest entit",
    ),
    "legal_proceedings_litigation": (
        r"\blitigation\b",
        r"\blawsuits?\b",
        r"\bclaims?\b",
        r"\bproceedings?\b",
        r"\binvestigation\b",
        r"\bcomplaint\b",
        r"\bsettlement\b",
        r"\bprobable\b",
        r"\breasonably possible\b",
    ),
    "regulatory_trade_policy": (
        r"\buflpa\b",
        r"\bad[/-]?cvd\b",
        r"\banti[- ]dumping\b",
        r"\bcountervailing\b",
        r"\btariff\b",
        r"\bieepa\b",
        r"\bitc\s*337\b|section\s+337\b",
        r"\bexport controls?\b",
        r"\bsanctions?\b",
        r"\bcustoms\b",
        r"\bforced labor\b",
    ),
    "debt_liquidity_covenant": (
        r"\bdebt\b",
        r"\bcovenants?\b",
        r"\bdefault\b",
        r"\bcredit facilit",
        r"\bborrowings?\b",
        r"\bliquidity\b",
        r"\bmaximum gross exposure\b",
    ),
    "cybersecurity_governance": (
        r"\bcybersecurity\b",
        r"\bcyber security\b",
        r"\bcybersecurity incident\b",
        r"\bvendor risk\b",
        r"\bboard\b",
        r"\binformation security\b",
    ),
    "material_contracts": (
        r"\bmaterial agreement\b",
        r"\blicense agreement\b",
        r"\bnon[- ]exclusive license\b",
        r"\btermination rights?\b",
        r"\bexclusiv",
        r"\bperformance obligations?\b",
        r"\bcustomer contracts?\b",
    ),
}


@dataclass(frozen=True)
class EvidenceAssessment:
    """Evidence quality assessment for one paragraph/domain pair."""

    score: int
    quality: str
    notes: list[str]
    keep: bool


def assess_evidence(text: str, domain: str) -> EvidenceAssessment:
    """Assess whether ``text`` is strong enough to support ``domain``."""

    compact = " ".join(text.split())
    lowered = compact.lower()
    notes: list[str] = []
    score = 0

    if _matches(lowered, TAXONOMY_PATTERNS):
        notes.append("taxonomy_or_xbrl_definition")
        score -= 4
    if _matches(lowered, HEADING_ONLY_PATTERNS) and len(lowered.split()) <= 12:
        notes.append("heading_or_label_only")
        score -= 3
    if _matches(lowered, GENERIC_POLICY_PATTERNS):
        notes.append("generic_accounting_policy")
        score -= 2
    if _domain_false_positive(lowered, domain):
        notes.append("domain_false_positive")
        score -= 4

    support_patterns = DOMAIN_SUPPORT_PATTERNS.get(domain, ())
    support_hits = [pattern for pattern in support_patterns if re.search(pattern, lowered)]
    if support_hits:
        score += min(len(support_hits), 4)
        notes.append(f"domain_support_hits:{len(support_hits)}")
    if re.search(r"\$[\d,.]+\s*(?:million|billion|thousand)?", compact, flags=re.IGNORECASE):
        score += 2
        notes.append("specific_amount")
    if re.search(r"\b(?:fiscal year|as of|during|in|on)\s+(?:20\d{2}|january|february|march|april|may|june|july|august|september|october|november|december)\b", lowered):
        score += 1
        notes.append("specific_timing")
    if re.search(r"\b(?:not material|not probable|reasonably possible|cannot be reasonably estimated|no accrued contingent liabilities)\b", lowered):
        score += 2
        notes.append("accounting_or_disclosure_posture")
    if len(compact.split()) >= 35:
        score += 1
        notes.append("substantive_paragraph")

    has_domain_support = bool(support_hits)
    has_disclosure_posture = "accounting_or_disclosure_posture" in notes
    posture_can_support_domain = domain in {
        "legal_proceedings_litigation",
        "disclosure_ir_consistency",
    }
    if not has_domain_support and not (has_disclosure_posture and posture_can_support_domain):
        return EvidenceAssessment(score, "suppressed", notes or ["insufficient_domain_specific_evidence"], False)

    if score >= 4:
        return EvidenceAssessment(score, "high", notes, True)
    if score >= 2:
        return EvidenceAssessment(score, "medium", notes, True)
    if score >= 0 and support_hits and not _matches(lowered, TAXONOMY_PATTERNS):
        return EvidenceAssessment(score, "low", notes, True)
    return EvidenceAssessment(score, "suppressed", notes or ["insufficient_domain_specific_evidence"], False)


def _domain_false_positive(text: str, domain: str) -> bool:
    if domain == "equity_dilution_control" and "warranty" in text and not re.search(r"\bwarrants?\b", text):
        return True
    if domain == "related_party_governance" and "non-affiliates" in text and "related" not in text:
        return True
    if domain == "related_party_governance" and "equity in losses of affiliates" in text and "related" not in text:
        return True
    if domain == "legal_proceedings_litigation" and "form of settlement in cash" in text:
        return True
    if domain == "debt_liquidity_covenant" and "time to liquidity" in text and "debt" not in text and "default" not in text:
        return True
    if domain == "debt_liquidity_covenant" and "lack of liquidity" in text and not re.search(
        r"\bdebt\b|\bcovenants?\b|\bdefault\b|\bcredit facilit|\bborrowings?\b|\bwaiver\b",
        text,
    ):
        return True
    if domain == "debt_liquidity_covenant" and "legal proceedings" in text and not re.search(
        r"\bdebt\b|\bcovenants?\b|\bdefault\b|\bcredit facilit|\bborrowings?\b|\bwaiver\b|\brefinanc",
        text,
    ):
        return True
    return False


def _matches(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)
