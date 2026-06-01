"""Rule-based risk-domain taxonomy for v0.2 risk cards."""

from __future__ import annotations

import re


RISK_DOMAIN_PATTERNS: dict[str, tuple[str, ...]] = {
    "audit_going_concern": (
        r"going concern",
        r"substantial doubt",
        r"continue as a going concern",
        r"ability to continue",
    ),
    "internal_control_reporting": (
        r"material weakness",
        r"internal control over financial reporting",
        r"\bicfr\b",
        r"\bsox\b|\bsarbanes[- ]oxley\b",
        r"disclosure controls? and procedures",
        r"controls? .* ineffective",
        r"remediation plan",
        r"significant deficiency",
    ),
    "legal_proceedings_litigation": (
        r"legal proceedings?",
        r"litigation",
        r"lawsuit",
        r"patent (?:infringement|litigation|matter|proceeding)",
        r"\bptab\b",
        r"\bitc\s*337\b|section\s+337",
        r"subpoena",
        r"investigation",
        r"complaint",
        r"settlement",
        r"arbitration",
        r"civil investigative demand",
    ),
    "regulatory_trade_policy": (
        r"\buflpa\b|uyghur forced labor prevention act",
        r"\bad[/-]?cvd\b|anti[- ]dumping|countervailing dut",
        r"tariff",
        r"\bieepa\b|international emergency economic powers act",
        r"export controls?",
        r"sanctions?",
        r"\bcbp\b|customs and border protection",
        r"forced labor",
        r"trade polic",
        r"tax credit eligibility",
        r"local content",
    ),
    "related_party_governance": (
        r"related[- ]part",
        r"affiliate",
        r"common control",
        r"controlling shareholder",
        r"director .* interest",
        r"executive .* interest",
        r"variable interest entit",
        r"\bvie\b",
    ),
    "debt_liquidity_covenant": (
        r"debt covenant",
        r"financial covenant",
        r"event of default",
        r"\bdefault\b",
        r"breach of covenant",
        r"waiver",
        r"credit facility",
        r"working capital deficit",
        r"liquidity",
        r"short[- ]term borrowings?",
        r"refinanc",
        r"senior notes?",
        r"convertible notes?",
    ),
    "guarantees_commitments": (
        r"guarantee",
        r"guaranty",
        r"commitment",
        r"purchase obligation",
        r"minimum purchase",
        r"off[- ]balance",
        r"standby letter of credit",
        r"indemnification",
        r"binding backlog",
        r"binding contract",
    ),
    "equity_dilution_control": (
        r"dilution",
        r"warrants?",
        r"convertible notes?",
        r"earnout",
        r"\bpipe\b",
        r"voting rights?",
        r"founder control",
        r"\brsu\b|restricted stock units?",
        r"share issuance",
        r"equity issuance",
    ),
    "tax_cross_border": (
        r"\btax\b",
        r"transfer pricing",
        r"tax authority",
        r"withholding",
        r"cross[- ]border",
        r"uncertain tax",
        r"tax audit",
        r"foreign exchange control",
        r"\bvat\b",
    ),
    "management_board_governance": (
        r"board of directors?",
        r"audit committee",
        r"(appoint(?:ed|ment)?|resign(?:ed|ation)?|transition).{0,80}(chief executive officer|\bceo\b|chief financial officer|\bcfo\b)",
        r"(chief executive officer|\bceo\b|chief financial officer|\bcfo\b).{0,80}(appoint(?:ed|ment)?|resign(?:ed|ation)?|transition)",
        r"resign(?:ed|ation)?",
        r"appoint(?:ed|ment)?",
        r"transition",
        r"corporate governance",
        r"independent directors?",
    ),
    "disclosure_ir_consistency": (
        r"safe harbor",
        r"forward[- ]looking statements?",
        r"guidance",
        r"non[- ]gaap",
        r"disclosure",
        r"materially differ",
        r"cannot assure",
        r"risk factors?",
    ),
    "cybersecurity_governance": (
        r"cybersecurity",
        r"cyber security",
        r"data breach",
        r"information security",
        r"ransomware",
        r"incident response",
    ),
    "material_contracts": (
        r"material contract",
        r"material agreement",
        r"supply agreement",
        r"license agreement",
        r"offtake",
        r"termination right",
        r"change of control",
        r"exclusive",
        r"long[- ]term agreement",
    ),
}


SUBDOMAIN_PATTERNS: dict[str, tuple[tuple[str, str], ...]] = {
    "regulatory_trade_policy": (
        ("UFLPA", r"\buflpa\b|uyghur forced labor prevention act|forced labor"),
        ("AD_CVD", r"\bad[/-]?cvd\b|anti[- ]dumping|countervailing"),
        ("ITC_337", r"\bitc\s*337\b|section\s+337"),
        ("tariff_refund", r"tariff|refund|\bieepa\b"),
        ("export_control", r"export controls?"),
        ("sanctions", r"sanctions?"),
        ("local_content", r"local content"),
        ("tax_credit_eligibility", r"tax credit eligibility"),
    ),
    "equity_dilution_control": (
        ("earnout_shares", r"earnout"),
        ("warrants", r"warrants?"),
        ("convertible_notes", r"convertible notes?"),
        ("RSU", r"\brsu\b|restricted stock units?"),
        ("PIPE", r"\bpipe\b"),
        ("founder_control", r"founder control"),
        ("voting_rights", r"voting rights?"),
    ),
    "legal_proceedings_litigation": (
        ("PTAB", r"\bptab\b"),
        ("ITC_337", r"\bitc\s*337\b|section\s+337"),
        ("patent_litigation", r"patent"),
        ("investigation_subpoena", r"investigation|subpoena|civil investigative demand"),
        ("settlement", r"settlement"),
    ),
    "internal_control_reporting": (
        ("SOX_404", r"\bsox\b|\bsarbanes[- ]oxley\b|404"),
        ("ICFR", r"\bicfr\b|internal control over financial reporting"),
        ("material_weakness", r"material weakness"),
        ("disclosure_controls", r"disclosure controls?"),
    ),
    "related_party_governance": (
        ("related_party_transactions", r"related[- ]part"),
        ("affiliate_transactions", r"affiliate"),
        ("control_conflict", r"common control|controlling shareholder|director .* interest"),
        ("VIE", r"variable interest entit|\bvie\b"),
    ),
}


def classify_risk_domains(text: str) -> list[str]:
    """Return risk domains supported by the text."""

    lowered = text.lower()
    domains = [
        domain
        for domain, patterns in RISK_DOMAIN_PATTERNS.items()
        if any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in patterns)
    ]
    return _dedupe(domains)


def detect_subdomains(domain: str, text: str) -> list[str]:
    """Return domain-specific subdomains supported by the text."""

    lowered = text.lower()
    patterns = SUBDOMAIN_PATTERNS.get(domain, ())
    subdomains = [
        name
        for name, pattern in patterns
        if re.search(pattern, lowered, flags=re.IGNORECASE)
    ]
    return _dedupe(subdomains)


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
