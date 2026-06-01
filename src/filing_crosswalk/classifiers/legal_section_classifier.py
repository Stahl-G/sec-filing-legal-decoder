"""Rule-based legal-heavy filing paragraph classifier."""

from __future__ import annotations

import re


CATEGORY_PATTERNS: list[tuple[str, tuple[str, ...]]] = [
    (
        "internal_control",
        (
            r"material weakness",
            r"internal control",
            r"disclosure controls?",
            r"remediation plan",
            r"ineffective",
            r"significant deficiency",
        ),
    ),
    (
        "debt_covenant_default",
        (
            r"debt covenant",
            r"financial covenant",
            r"default",
            r"event of default",
            r"waiver",
            r"breach of covenant",
            r"going concern",
            r"substantial doubt",
        ),
    ),
    (
        "legal_proceedings",
        (
            r"legal proceedings?",
            r"litigation",
            r"lawsuit",
            r"claim",
            r"settlement",
            r"subpoena",
            r"investigation",
            r"complaint",
            r"proceeding",
        ),
    ),
    (
        "regulatory_compliance",
        (
            r"regulatory",
            r"compliance",
            r"sec\b",
            r"department of justice",
            r"doj\b",
            r"ftc\b",
            r"fda\b",
            r"environmental protection agency",
            r"epa\b",
            r"sanctions?",
            r"export controls?",
        ),
    ),
    (
        "tax_risk",
        (
            r"tax",
            r"irs\b",
            r"uncertain tax",
            r"tax audit",
            r"transfer pricing",
            r"tax authority",
        ),
    ),
    (
        "related_party_transaction",
        (
            r"related[- ]party",
            r"affiliate",
            r"controlled by",
            r"common control",
            r"director .* interest",
            r"executive .* interest",
        ),
    ),
    (
        "guarantee_commitment",
        (
            r"guarantee",
            r"guaranty",
            r"commitment",
            r"purchase obligation",
            r"off[- ]balance",
            r"standby letter of credit",
            r"indemnification",
        ),
    ),
    (
        "share_capital_dilution",
        (
            r"dilution",
            r"warrant",
            r"convertible",
            r"share capital",
            r"common stock",
            r"preferred stock",
            r"equity issuance",
            r"at-the-market",
            r"\batm\b",
        ),
    ),
    (
        "material_contract",
        (
            r"material contract",
            r"material agreement",
            r"supply agreement",
            r"license agreement",
            r"termination right",
            r"change of control",
            r"exclusive",
        ),
    ),
    (
        "risk_factor",
        (
            r"risk factor",
            r"adversely affect",
            r"material adverse",
            r"we face risks?",
            r"could materially",
            r"may materially",
        ),
    ),
    (
        "forward_looking_statement",
        (
            r"forward[- ]looking statements?",
            r"safe harbor",
            r"expect",
            r"anticipate",
            r"believe",
            r"intend",
            r"plan",
            r"estimate",
            r"project",
        ),
    ),
]

BOILERPLATE_PATTERNS = (
    r"from time to time",
    r"may",
    r"could",
    r"might",
    r"cannot assure",
    r"uncertain",
)


def classify_section(paragraph: str) -> str:
    """Classify a filing paragraph into one legal-heavy category."""

    text = paragraph.lower()
    for category, patterns in CATEGORY_PATTERNS:
        if any(re.search(pattern, text) for pattern in patterns):
            return category

    boilerplate_hits = sum(1 for pattern in BOILERPLATE_PATTERNS if re.search(pattern, text))
    if boilerplate_hits >= 2 and len(text.split()) >= 18:
        return "generic_boilerplate"

    return "unknown"
