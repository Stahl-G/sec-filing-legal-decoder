"""Domain templates for finance-readable legal risk cards."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CardTemplate:
    """Reusable language for one risk-card domain."""

    title: str
    owners: list[str]
    plain_language_meaning: str
    why_finance_readers_should_care: str
    legal_or_audit_relevance: str
    financial_statement_linkage: list[str]
    disclosure_ir_relevance: str
    suggested_management_follow_up: str
    what_not_to_overstate: str


TEMPLATES: dict[str, CardTemplate] = {
    "audit_going_concern": CardTemplate(
        title="Going Concern / Substantial Doubt",
        owners=["Finance", "Auditor", "Legal", "Board"],
        plain_language_meaning=(
            "The filing language is not merely describing weak liquidity. It may indicate "
            "audit-level concern about whether the company can continue as a going concern "
            "unless disclosed mitigation plans are successful."
        ),
        why_finance_readers_should_care=(
            "This affects how liquidity, refinancing capacity, supplier credit, customer "
            "prepayments, capex plans, and management forecasts should be interpreted."
        ),
        legal_or_audit_relevance=(
            "Going-concern language is an audit and disclosure warning signal. The review "
            "question is whether management's mitigation plan is sufficiently supported and "
            "adequately disclosed."
        ),
        financial_statement_linkage=[
            "working capital deficit",
            "short-term borrowings and maturities",
            "operating cash flow",
            "capex commitments",
            "related-party or external financing",
            "subsequent financing events",
        ],
        disclosure_ir_relevance=(
            "Investor-facing language should avoid presenting mitigation plans as certain "
            "unless the filing supports that certainty."
        ),
        suggested_management_follow_up=(
            "Prepare a liquidity bridge that separates committed funding from planned or "
            "conditional mitigation actions."
        ),
        what_not_to_overstate=(
            "Do not say the company will fail. The correct posture is that substantial doubt "
            "or going-concern uncertainty should be evaluated against disclosed mitigation plans."
        ),
    ),
    "internal_control_reporting": CardTemplate(
        title="Internal Control / SOX / ICFR",
        owners=["Auditor", "Finance", "Legal"],
        plain_language_meaning=(
            "Internal-control language points to reporting process risk, not simply a finance "
            "KPI issue. It may affect reliability of financial reporting and remediation timing."
        ),
        why_finance_readers_should_care=(
            "A material weakness or ineffective control conclusion can affect confidence in "
            "reported numbers, close processes, estimates, and remediation costs."
        ),
        legal_or_audit_relevance=(
            "This is audit and disclosure-control territory. Readers should check whether the "
            "filing distinguishes identified deficiencies from remediation plans."
        ),
        financial_statement_linkage=[
            "affected accounts and estimates",
            "close and consolidation process",
            "IT systems and access controls",
            "audit adjustments",
            "remediation cost and timing",
        ],
        disclosure_ir_relevance=(
            "IR language should not imply controls are fixed until remediation has been tested "
            "and disclosed as effective."
        ),
        suggested_management_follow_up=(
            "Document affected processes, remediation owners, target dates, and evidence needed "
            "for auditor review."
        ),
        what_not_to_overstate=(
            "Do not equate a control weakness with proven fraud or misstated financials unless "
            "the filing says that."
        ),
    ),
    "legal_proceedings_litigation": CardTemplate(
        title="Legal Proceedings / Litigation",
        owners=["Legal", "Finance", "IR"],
        plain_language_meaning=(
            "The language identifies an actual or potential dispute, investigation, claim, or "
            "proceeding that should be translated into stage, exposure, timing, and disclosure questions."
        ),
        why_finance_readers_should_care=(
            "Proceedings can affect accruals, contingent liabilities, legal spend, insurance "
            "recoveries, product access, customer relationships, and management credibility."
        ),
        legal_or_audit_relevance=(
            "The key legal/accounting bridge is whether loss is probable, reasonably possible, "
            "remote, accrued, disclosed, or not estimable."
        ),
        financial_statement_linkage=[
            "loss contingencies",
            "legal expense",
            "accruals and disclosure ranges",
            "insurance or indemnity",
            "cash-flow timing",
        ],
        disclosure_ir_relevance=(
            "External messaging should avoid declaring the matter immaterial, resolved, or won "
            "unless the filing supports that interpretation."
        ),
        suggested_management_follow_up=(
            "Create a matter tracker with stage, next event, potential remedies, accounting "
            "position, and disclosure owner."
        ),
        what_not_to_overstate=(
            "Do not say the company violated law or will incur a loss. Frame it as a matter "
            "requiring legal and accounting review."
        ),
    ),
    "regulatory_trade_policy": CardTemplate(
        title="Regulatory / Trade Policy",
        owners=["Legal", "Finance", "IR", "Management"],
        plain_language_meaning=(
            "The language points to regulatory or trade-policy exposure such as tariffs, UFLPA, "
            "AD/CVD, ITC 337, sanctions, export controls, or tax-credit eligibility."
        ),
        why_finance_readers_should_care=(
            "These matters can affect market access, import timing, gross margin, inventory, "
            "supplier choices, customer delivery, and cash recovery."
        ),
        legal_or_audit_relevance=(
            "The review question is which rule or authority applies, what evidence supports "
            "compliance, and whether the outcome remains uncertain."
        ),
        financial_statement_linkage=[
            "tariff expense or refund",
            "inventory valuation",
            "gross margin",
            "supply-chain cost",
            "revenue timing",
            "customer and supplier concentration",
        ],
        disclosure_ir_relevance=(
            "IR should avoid presenting refunds, eligibility, or customs outcomes as resolved "
            "if the filing frames them as uncertain."
        ),
        suggested_management_follow_up=(
            "Map each regulatory item to affected product lines, customs/import status, margin "
            "exposure, and responsible compliance owner."
        ),
        what_not_to_overstate=(
            "Do not conclude non-compliance or guaranteed recovery. Use review language such as "
            "may indicate, should confirm, and depends on regulatory outcome."
        ),
    ),
    "related_party_governance": CardTemplate(
        title="Related Party Transactions / Governance",
        owners=["Legal", "Auditor", "Finance", "Board"],
        plain_language_meaning=(
            "Related-party language is not only revenue concentration. It raises questions about "
            "transaction independence, fairness, approvals, conflicts, collectability, and disclosure completeness."
        ),
        why_finance_readers_should_care=(
            "Related parties can affect revenue quality, margins, cash conversion, liquidity "
            "support, guarantees, and sustainability of commercial terms."
        ),
        legal_or_audit_relevance=(
            "Readers should check whether the transactions were identified, approved, priced, "
            "and disclosed under the company's related-party and audit procedures."
        ),
        financial_statement_linkage=[
            "revenue quality",
            "accounts receivable collectability",
            "gross margin",
            "cash-flow quality",
            "guarantees or financing support",
            "balances due to/from related parties",
        ],
        disclosure_ir_relevance=(
            "Disclosure should not make related-party economics look equivalent to arm's-length "
            "third-party business without support."
        ),
        suggested_management_follow_up=(
            "Prepare a related-party schedule covering approval path, pricing method, balances, "
            "settlement terms, and independence considerations."
        ),
        what_not_to_overstate=(
            "Do not label the transaction improper. The right conclusion is that governance, "
            "pricing, collectability, and disclosure should be checked."
        ),
    ),
    "debt_liquidity_covenant": CardTemplate(
        title="Debt / Liquidity / Covenant",
        owners=["Finance", "Legal", "Auditor"],
        plain_language_meaning=(
            "Debt and liquidity language may signal contractual constraints, refinancing risk, "
            "default risk, waiver dependency, or classification questions."
        ),
        why_finance_readers_should_care=(
            "Covenants, defaults, guarantees, and maturities can change liquidity runway, debt "
            "classification, financing options, and going-concern analysis."
        ),
        legal_or_audit_relevance=(
            "The legal-to-finance bridge is the contract: covenant definitions, cure rights, "
            "acceleration, cross-default, collateral, and waiver terms."
        ),
        financial_statement_linkage=[
            "debt maturity schedule",
            "current versus noncurrent classification",
            "interest expense",
            "covenant compliance",
            "going-concern analysis",
            "restricted cash or collateral",
        ],
        disclosure_ir_relevance=(
            "Liquidity messaging should distinguish committed availability from financing that "
            "depends on future waivers, refinancing, or market access."
        ),
        suggested_management_follow_up=(
            "Build a covenant and maturity tracker with headroom, waiver dates, default triggers, "
            "and refinancing assumptions."
        ),
        what_not_to_overstate=(
            "Do not imply default or covenant breach unless disclosed. Ask whether contract terms "
            "create a review trigger."
        ),
    ),
    "guarantees_commitments": CardTemplate(
        title="Guarantees / Commitments / Binding Backlog",
        owners=["Finance", "Legal", "Management"],
        plain_language_meaning=(
            "Commitments and guarantees are not just operational notes. They can create fixed "
            "obligations, contingent exposure, performance duties, or liquidity constraints."
        ),
        why_finance_readers_should_care=(
            "These items can affect cash planning, margins, capex, inventory, revenue durability, "
            "and downside exposure if counterparties or projects change."
        ),
        legal_or_audit_relevance=(
            "The key review is whether obligations are firm or cancellable, guaranteed or conditional, "
            "and properly reflected in disclosure and accounting."
        ),
        financial_statement_linkage=[
            "purchase commitments",
            "off-balance-sheet obligations",
            "contract liabilities",
            "backlog conversion",
            "guarantees and indemnities",
            "capex and working capital",
        ],
        disclosure_ir_relevance=(
            "Backlog or commitments should not be described as guaranteed revenue unless the "
            "contract terms and disclosure support that framing."
        ),
        suggested_management_follow_up=(
            "Separate firm obligations, cancellable backlog, customer-dependent projects, and "
            "guarantee exposure in one schedule."
        ),
        what_not_to_overstate=(
            "Do not equate backlog with certain revenue or all commitments with immediate liabilities."
        ),
    ),
    "equity_dilution_control": CardTemplate(
        title="Earnout / Warrants / Convertible Notes / Dilution",
        owners=["Finance", "Legal", "IR"],
        plain_language_meaning=(
            "Equity-linked instruments may create dilution, control, fair-value, registration, "
            "or investor-communication issues beyond ordinary capital structure facts."
        ),
        why_finance_readers_should_care=(
            "Dilution and fair-value movements can affect EPS, ownership, control, non-cash P&L "
            "volatility, and investor interpretation of performance."
        ),
        legal_or_audit_relevance=(
            "Review instrument terms, conversion/exercise triggers, voting rights, registration "
            "obligations, accounting classification, and change-of-control provisions."
        ),
        financial_statement_linkage=[
            "EPS and diluted share count",
            "fair-value gains or losses",
            "liability versus equity classification",
            "additional paid-in capital",
            "change-of-control terms",
        ],
        disclosure_ir_relevance=(
            "Investor messaging should distinguish operating performance from non-cash mark-to-market "
            "effects or potential dilution."
        ),
        suggested_management_follow_up=(
            "Prepare a fully diluted capitalization bridge with trigger conditions and accounting treatment."
        ),
        what_not_to_overstate=(
            "Do not treat all potential shares as currently issued or all fair-value movement as cash impact."
        ),
    ),
    "tax_cross_border": CardTemplate(
        title="Tax / Cross-Border Structure",
        owners=["Finance", "Legal", "Auditor"],
        plain_language_meaning=(
            "Tax and cross-border language may indicate exposure to transfer pricing, withholding, "
            "tax authority review, repatriation limits, credits, or uncertain tax positions."
        ),
        why_finance_readers_should_care=(
            "These matters can affect effective tax rate, cash taxes, reserves, valuation allowance, "
            "repatriation, and earnings quality."
        ),
        legal_or_audit_relevance=(
            "The review question is whether tax positions, reserves, jurisdictional assumptions, "
            "and authority challenges are appropriately disclosed and supported."
        ),
        financial_statement_linkage=[
            "effective tax rate",
            "uncertain tax positions",
            "deferred tax assets and valuation allowance",
            "withholding taxes",
            "cash tax payments",
            "transfer-pricing reserves",
        ],
        disclosure_ir_relevance=(
            "Do not present tax benefits or credits as durable if eligibility or authority review remains uncertain."
        ),
        suggested_management_follow_up=(
            "Create a jurisdiction-by-jurisdiction tax exposure schedule with reserve, cash, and disclosure implications."
        ),
        what_not_to_overstate=(
            "Do not say the tax position is wrong or accepted unless the filing provides that conclusion."
        ),
    ),
    "management_board_governance": CardTemplate(
        title="Management / Board Governance",
        owners=["Board", "Legal", "IR"],
        plain_language_meaning=(
            "Leadership, board, committee, independence, or governance changes can affect oversight, "
            "continuity, approvals, and disclosure controls."
        ),
        why_finance_readers_should_care=(
            "Governance changes may affect execution credibility, succession, audit committee oversight, "
            "investor confidence, and risk supervision."
        ),
        legal_or_audit_relevance=(
            "Review whether governance facts are consistent with exchange rules, committee charters, "
            "independence standards, and filing disclosures."
        ),
        financial_statement_linkage=[
            "management continuity",
            "audit committee oversight",
            "related-party approvals",
            "control environment",
            "executive compensation",
        ],
        disclosure_ir_relevance=(
            "IR should explain transition and oversight without overstating certainty or continuity."
        ),
        suggested_management_follow_up=(
            "Document transition plan, committee ownership, independence assessment, and investor messaging posture."
        ),
        what_not_to_overstate=(
            "Do not assume governance change is negative. Treat it as a review prompt for oversight and continuity."
        ),
    ),
    "disclosure_ir_consistency": CardTemplate(
        title="Disclosure / IR Consistency",
        owners=["Legal", "IR", "Finance"],
        plain_language_meaning=(
            "The filing language may require more careful wording in finance analysis, management notes, "
            "or investor-facing commentary."
        ),
        why_finance_readers_should_care=(
            "A financial conclusion can become misleading if it sounds more certain than the filing language supports."
        ),
        legal_or_audit_relevance=(
            "This is a disclosure calibration issue: check whether assumptions, caveats, and unresolved risks are preserved."
        ),
        financial_statement_linkage=[
            "guidance assumptions",
            "non-GAAP reconciliation",
            "risk-factor alignment",
            "MD&A liquidity and trend language",
        ],
        disclosure_ir_relevance=(
            "Use safer wording when the filing frames outcomes as conditional, uncertain, or subject to review."
        ),
        suggested_management_follow_up=(
            "Compare finance-analysis conclusions against filing caveats and revise overly certain claims."
        ),
        what_not_to_overstate=(
            "Do not remove uncertainty language merely because a financial model has a base case."
        ),
    ),
    "cybersecurity_governance": CardTemplate(
        title="Cybersecurity Governance",
        owners=["Legal", "Management", "Board"],
        plain_language_meaning=(
            "Cybersecurity language may involve governance, incident response, materiality, vendor, "
            "and board oversight questions."
        ),
        why_finance_readers_should_care=(
            "Cyber events can affect operations, legal exposure, customer trust, remediation spend, "
            "insurance, and disclosure timing."
        ),
        legal_or_audit_relevance=(
            "The review question is whether board oversight, incident materiality, controls, and "
            "disclosure timing match current facts."
        ),
        financial_statement_linkage=[
            "remediation costs",
            "insurance recovery",
            "contingent liabilities",
            "business interruption",
            "vendor risk",
        ],
        disclosure_ir_relevance=(
            "Disclosure should not imply there was no material incident unless that conclusion has been reviewed."
        ),
        suggested_management_follow_up=(
            "Confirm incident-response ownership, board reporting cadence, and financial exposure tracking."
        ),
        what_not_to_overstate=(
            "Do not infer a breach or material cyber incident from governance disclosure alone."
        ),
    ),
    "material_contracts": CardTemplate(
        title="Material Contracts / Commercial Dependencies",
        owners=["Legal", "Finance", "Management"],
        plain_language_meaning=(
            "Material contracts can embed rights and obligations that change how revenue quality, "
            "margin, exclusivity, termination, and concentration risks should be read."
        ),
        why_finance_readers_should_care=(
            "Contract terms may affect revenue durability, pricing power, supply access, capex, "
            "termination risk, and customer or supplier concentration."
        ),
        legal_or_audit_relevance=(
            "Review key terms: exclusivity, termination, change of control, minimums, indemnities, "
            "performance obligations, and related accounting treatment."
        ),
        financial_statement_linkage=[
            "revenue recognition",
            "backlog",
            "gross margin",
            "contract assets and liabilities",
            "customer or supplier concentration",
            "capex commitments",
        ],
        disclosure_ir_relevance=(
            "Do not describe a contract as stable recurring revenue if termination, concentration, "
            "or performance conditions remain material."
        ),
        suggested_management_follow_up=(
            "Summarize contract economics, termination rights, performance obligations, and downside scenarios."
        ),
        what_not_to_overstate=(
            "Do not infer that a material agreement guarantees future revenue without checking terms."
        ),
    ),
}


def template_for(domain: str) -> CardTemplate:
    """Return a domain template, with a generic fallback for future domains."""

    return TEMPLATES.get(
        domain,
        CardTemplate(
            title=domain.replace("_", " ").title(),
            owners=["Legal", "Finance"],
            plain_language_meaning=(
                "The filing language appears risk-relevant and should be translated into "
                "finance, disclosure, and follow-up questions."
            ),
            why_finance_readers_should_care=(
                "Finance readers should identify the affected accounts, assumptions, cash flows, "
                "and disclosure posture."
            ),
            legal_or_audit_relevance=(
                "Qualified reviewers should confirm the legal, audit, and disclosure implications."
            ),
            financial_statement_linkage=["affected accounts", "cash-flow timing", "disclosure notes"],
            disclosure_ir_relevance=(
                "Investor-facing language should remain consistent with the filing's uncertainty level."
            ),
            suggested_management_follow_up=(
                "Assign an owner to reconcile the filing language with finance and disclosure materials."
            ),
            what_not_to_overstate=(
                "Do not convert a risk prompt into a legal, audit, accounting, or investment conclusion."
            ),
        ),
    )
