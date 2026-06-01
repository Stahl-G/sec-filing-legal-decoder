"""Role-specific escalation question generation."""

from __future__ import annotations


ROLE_ORDER = [
    "Ask Legal",
    "Ask Finance",
    "Ask Auditor",
    "Ask IR",
    "Ask Management / Board",
]


def generate_escalation_questions(
    section_type: str, reading_decision: str, signals: list[str]
) -> dict[str, list[str]]:
    """Generate questions that help the reader escalate without answering law."""

    questions = {role: [] for role in ROLE_ORDER}
    questions["Ask Legal"].append(
        "Does this wording describe a current matter, a threatened matter, or only generic risk language?"
    )
    questions["Ask Finance"].append(
        "Is there any accrual, disclosure, cash-flow impact, covenant impact, or sensitivity that should be reconciled?"
    )

    if section_type == "legal_proceedings":
        questions["Ask Legal"].extend(
            [
                "What is the current status, expected next milestone, and range of reasonably possible outcomes?",
                "Are any privilege or settlement constraints limiting what can be disclosed?",
            ]
        )
        questions["Ask Finance"].append(
            "Does the contingency footnote align with the legal matter status and any insurance recovery assumptions?"
        )
        questions["Ask Auditor"].append(
            "What evidence supports the accrual or no-accrual position for this matter?"
        )
        questions["Ask IR"].append(
            "Is external messaging consistent with the filing language and prior public statements?"
        )
    elif section_type == "internal_control":
        questions["Ask Finance"].append(
            "Which accounts, systems, locations, or processes are affected by the control issue?"
        )
        questions["Ask Auditor"].extend(
            [
                "How does the issue affect audit scope, reliance on controls, and remediation testing?",
                "Is the disclosure aligned with the auditor's ICFR opinion and management's remediation plan?",
            ]
        )
        questions["Ask Management / Board"].append(
            "What resources, owners, and deadlines are assigned to remediation?"
        )
    elif section_type == "debt_covenant_default":
        questions["Ask Legal"].append(
            "What remedies, waivers, cure periods, and acceleration rights apply under the credit documents?"
        )
        questions["Ask Finance"].extend(
            [
                "What is the latest covenant calculation and liquidity runway under base and downside cases?",
                "Does debt classification need reassessment based on waiver timing or default status?",
            ]
        )
        questions["Ask Auditor"].append(
            "How should covenant status affect going-concern and debt classification analysis?"
        )
    elif section_type == "related_party_transaction":
        questions["Ask Legal"].append(
            "Were required approvals, conflict procedures, and related-party disclosure requirements followed?"
        )
        questions["Ask Finance"].append(
            "Are pricing, balances, collectability, guarantees, and cash-flow effects clearly reconciled?"
        )
        questions["Ask Management / Board"].append(
            "Does the board need a refreshed conflict review or governance summary?"
        )
    elif section_type == "guarantee_commitment":
        questions["Ask Finance"].append(
            "What is the maximum exposure, expected cash timing, and recognition or disclosure treatment?"
        )
        questions["Ask Legal"].append(
            "What triggers the guarantee or commitment, and can the company terminate or cap exposure?"
        )
    elif section_type == "share_capital_dilution":
        questions["Ask Finance"].append(
            "What are the diluted share-count, EPS, conversion, warrant, and proceeds sensitivities?"
        )
        questions["Ask IR"].append(
            "How should dilution risk be explained consistently with investor materials?"
        )
    elif section_type == "regulatory_compliance":
        questions["Ask Legal"].append(
            "Which regulator, rule, license, or jurisdiction is involved, and what is the current procedural status?"
        )
        questions["Ask Finance"].append(
            "Are remediation costs, fines, revenue restrictions, or capex needs reflected in forecasts?"
        )
    elif section_type == "tax_risk":
        questions["Ask Finance"].append(
            "How does this affect tax reserves, effective tax rate, cash taxes, or deferred tax assets?"
        )
        questions["Ask Auditor"].append(
            "What support exists for recognition and measurement of uncertain tax positions?"
        )
    elif section_type == "material_contract":
        questions["Ask Legal"].append(
            "What termination, exclusivity, change-of-control, penalty, or minimum commitment terms matter most?"
        )
        questions["Ask Finance"].append(
            "Which revenue, margin, capex, working-capital, or cash forecast lines depend on this contract?"
        )
    elif section_type == "forward_looking_statement":
        questions["Ask IR"].append(
            "Are the forward-looking assumptions consistent with guidance, investor decks, and earnings scripts?"
        )

    if reading_decision == "ESCALATE" or signals:
        questions["Ask Management / Board"].append(
            "Does this matter require a management briefing, board update, or disclosure committee review?"
        )

    return {role: items for role, items in questions.items() if items}
