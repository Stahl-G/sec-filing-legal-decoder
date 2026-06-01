"""Role-specific question bank for v0.3 risk cards."""

from __future__ import annotations


QUESTION_BANK: dict[str, dict[str, list[str]]] = {
    "audit_going_concern": {
        "Ask Finance": [
            "Does the 12-month cash-flow forecast cover short-term debt, working-capital needs, and committed capex?",
            "Which mitigation measures are committed versus dependent on future financing or operating improvements?",
        ],
        "Ask Auditor": [
            "Which assumptions were necessary to support or avoid the going-concern conclusion?",
            "Were management's mitigation plans sufficient to alleviate substantial doubt, or only disclosed as plans?",
        ],
        "Ask Legal": [
            "Is the liquidity and mitigation-plan disclosure complete and not overly optimistic?",
        ],
        "Ask Board": [
            "Has the board reviewed downside scenarios, financing alternatives, and covenant/liquidity triggers?",
        ],
    },
    "internal_control_reporting": {
        "Ask Auditor": [
            "What control gaps drove the ICFR or disclosure-control conclusion?",
            "What evidence is needed before remediation can be considered effective?",
        ],
        "Ask Finance": [
            "Which accounts, estimates, systems, or reporting processes are affected by the weakness?",
        ],
        "Ask Legal": [
            "Does the disclosure clearly distinguish identified weaknesses from remediation plans?",
        ],
    },
    "legal_proceedings_litigation": {
        "Ask Legal": [
            "What stage is the proceeding in, and what outcomes are reasonably possible?",
            "Is any loss probable, reasonably possible, remote, accrued, or not estimable?",
        ],
        "Ask Finance": [
            "Is there an accrual, range of loss, insurance recovery, indemnity, or cash-flow timing issue?",
        ],
        "Ask IR": [
            "Does external messaging avoid overstating dismissal, settlement, or non-materiality before support exists?",
        ],
    },
    "regulatory_trade_policy": {
        "Ask Legal": [
            "Which authority, rule, investigation, or trade action applies, and what compliance evidence is needed?",
            "Are import bans, tariff refunds, AD/CVD, UFLPA, ITC 337, sanctions, or export-control risks still open?",
        ],
        "Ask Finance": [
            "What margin, inventory, customer, supplier, and cash-flow exposure depends on the regulatory outcome?",
        ],
        "Ask IR": [
            "Should the risk be framed as an unresolved regulatory exposure rather than a resolved financial item?",
        ],
    },
    "related_party_governance": {
        "Ask Legal": [
            "Were the transactions reviewed under the company's related-party policy and approved by disinterested directors or the audit committee?",
        ],
        "Ask Finance": [
            "Are pricing, payment terms, collectability, and revenue recognition comparable to third-party transactions?",
        ],
        "Ask Auditor": [
            "Has management identified all related parties, balances, guarantees, and side arrangements?",
        ],
        "Ask Board": [
            "Does the board have a plan to monitor or reduce conflicts and related-party dependency?",
        ],
    },
    "debt_liquidity_covenant": {
        "Ask Finance": [
            "Which covenants, maturities, defaults, waivers, refinancing assumptions, and liquidity sources are most sensitive?",
            "Are covenant compliance and repayment capacity supported by current forecasts?",
        ],
        "Ask Legal": [
            "Do debt agreements contain acceleration, cross-default, guarantee, or change-of-control triggers?",
        ],
        "Ask Auditor": [
            "Does debt classification and going-concern analysis reflect the covenant and waiver facts?",
        ],
    },
    "guarantees_commitments": {
        "Ask Finance": [
            "Are purchase obligations, guarantees, backlog, and minimum commitments reflected in liquidity and margin planning?",
        ],
        "Ask Legal": [
            "Are termination, indemnity, guarantee, and performance obligations clearly disclosed?",
        ],
        "Ask Management": [
            "Which commitments are firm, cancellable, customer-dependent, or subject to counterparty performance?",
        ],
    },
    "equity_dilution_control": {
        "Ask Finance": [
            "What is the potential dilution under earnout, warrant, convertible, RSU, PIPE, or other equity instruments?",
        ],
        "Ask Legal": [
            "Are conversion, exercise, voting, registration, and change-of-control terms fully reflected in disclosure?",
        ],
        "Ask IR": [
            "Does investor messaging distinguish accounting fair-value volatility from cash operating performance?",
        ],
    },
    "tax_cross_border": {
        "Ask Finance": [
            "Which tax exposures are booked, unrecognized, indemnified, or dependent on cross-border assumptions?",
        ],
        "Ask Legal": [
            "Are tax authority challenges, transfer-pricing positions, and repatriation restrictions described with enough context?",
        ],
        "Ask Auditor": [
            "Does the tax reserve or uncertain-tax-position analysis match the filing language?",
        ],
    },
    "management_board_governance": {
        "Ask Board": [
            "What succession, independence, committee oversight, and transition controls are in place?",
        ],
        "Ask Legal": [
            "Are governance changes and independence disclosures complete and consistent with exchange requirements?",
        ],
        "Ask IR": [
            "Should messaging explain continuity, oversight, and transition risk without overstating certainty?",
        ],
    },
    "disclosure_ir_consistency": {
        "Ask Legal": [
            "Does the filing language support the level of certainty used in investor or management-facing analysis?",
        ],
        "Ask IR": [
            "Should public messaging use more cautious wording around guidance, assumptions, and unresolved risk?",
        ],
        "Ask Finance": [
            "Which financial conclusions depend on assumptions that the filing itself frames as uncertain?",
        ],
    },
    "cybersecurity_governance": {
        "Ask Legal": [
            "Does incident, control, and governance disclosure match current cybersecurity rules and board oversight facts?",
        ],
        "Ask Management": [
            "Who owns remediation, incident response, vendor risk, and board reporting?",
        ],
    },
    "material_contracts": {
        "Ask Legal": [
            "What termination rights, exclusivity, change-of-control, indemnity, or performance obligations are embedded in the agreement?",
        ],
        "Ask Finance": [
            "How does the agreement affect revenue durability, margin, working capital, backlog, capex, and concentration risk?",
        ],
        "Ask Management": [
            "Which contract assumptions should be stress-tested under downside scenarios?",
        ],
    },
}
