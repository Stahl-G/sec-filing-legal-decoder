"""Finance relevance mapping by legal-heavy filing section type."""

from __future__ import annotations


SECTION_GUIDANCE: dict[str, dict[str, object]] = {
    "forward_looking_statement": {
        "plain": "Safe-harbor language frames projections and assumptions; usually it is context rather than a standalone finance issue.",
        "business": "Helps identify management's assumption set and cautionary framing.",
        "financial": "Compare with guidance, liquidity assumptions, capex plans, and sensitivity disclosures.",
        "compare": ["guidance language", "risk factors", "MD&A assumptions", "prior-year safe harbor wording"],
    },
    "risk_factor": {
        "plain": "Risk language describes a possible adverse event; determine whether it is generic or tied to a current fact.",
        "business": "May affect strategy, operations, market access, supply, customers, or execution risk.",
        "financial": "Map to revenue, margin, impairment, liquidity, covenant, or contingency exposure.",
        "compare": ["prior-year wording", "MD&A trend discussion", "footnotes", "known events after period end"],
    },
    "legal_proceedings": {
        "plain": "Legal-proceedings language may describe claims, investigations, settlements, or routine litigation exposure.",
        "business": "Can indicate operational disruption, regulatory scrutiny, management distraction, or reputational risk.",
        "financial": "Review contingency accruals, reasonably possible loss ranges, insurance recoveries, and disclosure controls.",
        "compare": ["contingency footnote", "prior-year legal proceedings", "subsequent events", "press releases"],
    },
    "regulatory_compliance": {
        "plain": "Regulatory language signals compliance obligations or scrutiny that may affect operations or approvals.",
        "business": "May affect licenses, product approvals, market access, export controls, or operating practices.",
        "financial": "Assess remediation cost, fines, revenue restrictions, inventory exposure, or capex needs.",
        "compare": ["risk factors", "MD&A", "compliance cost disclosures", "known regulator correspondence"],
    },
    "tax_risk": {
        "plain": "Tax language may describe uncertain tax positions, audits, transfer pricing, or jurisdictional exposure.",
        "business": "May affect legal structure, cash repatriation, pricing, or geographic strategy.",
        "financial": "Review tax reserves, effective tax rate, cash taxes, deferred tax assets, and valuation allowance.",
        "compare": ["tax footnote", "effective tax rate bridge", "prior-year tax reserves", "audit status"],
    },
    "internal_control": {
        "plain": "Internal-control language addresses reliability of reporting processes and disclosure controls.",
        "business": "May indicate process, system, staffing, or governance weakness.",
        "financial": "Assess restatement risk, audit scope, remediation cost, and confidence in reported numbers.",
        "compare": ["auditor opinion", "ICFR disclosure", "restatement history", "remediation timeline"],
    },
    "related_party_transaction": {
        "plain": "Related-party language describes transactions with affiliates, directors, officers, or commonly controlled parties.",
        "business": "May affect governance quality, transfer pricing, procurement, or strategic independence.",
        "financial": "Review pricing, balances, cash flows, guarantees, receivables collectability, and approval controls.",
        "compare": ["related-party footnote", "board approvals", "receivables/payables", "governance disclosures"],
    },
    "debt_covenant_default": {
        "plain": "Debt-covenant language can affect access to capital, acceleration risk, waivers, and going-concern analysis.",
        "business": "May constrain operations, capex, dividends, acquisitions, or refinancing options.",
        "financial": "Review liquidity runway, covenant calculations, waiver terms, default remedies, and classification of debt.",
        "compare": ["debt footnote", "liquidity MD&A", "credit agreement", "subsequent waivers"],
    },
    "guarantee_commitment": {
        "plain": "Guarantee and commitment language can create off-balance-sheet or future cash obligations.",
        "business": "May lock in suppliers, customers, affiliates, projects, or purchase volumes.",
        "financial": "Review maximum exposure, fair value, cash timing, collateral, and contingent liabilities.",
        "compare": ["commitments footnote", "lease/purchase obligations", "cash flow forecast", "counterparty exposure"],
    },
    "share_capital_dilution": {
        "plain": "Dilution language describes securities or rights that may increase share count or alter ownership economics.",
        "business": "May affect control, financing flexibility, investor perception, or transaction strategy.",
        "financial": "Review diluted EPS, warrant terms, convertible triggers, proceeds, and share-count sensitivity.",
        "compare": ["equity footnote", "EPS table", "capitalization table", "financing agreements"],
    },
    "material_contract": {
        "plain": "Material-contract language may describe agreements whose terms could affect operating or financial outcomes.",
        "business": "May affect supply, customers, exclusivity, termination rights, pricing, or strategic dependence.",
        "financial": "Review minimum commitments, penalties, revenue dependence, margin terms, and termination exposure.",
        "compare": ["filed exhibits", "revenue concentration", "purchase commitments", "risk factors"],
    },
    "generic_boilerplate": {
        "plain": "Generic cautionary language appears broadly applicable and may not describe a current company-specific event.",
        "business": "Usually context unless wording changed or became tied to a specific event.",
        "financial": "Compare for wording changes before spending detailed review time.",
        "compare": ["prior-year wording", "new named parties", "new amounts", "new specific events"],
    },
    "unknown": {
        "plain": "The paragraph does not match the current legal-heavy filing categories with high confidence.",
        "business": "Review manually if it appears important to the filing narrative.",
        "financial": "Map manually to financial statements, MD&A, or footnotes if relevant.",
        "compare": ["surrounding section heading", "prior-year wording", "related footnotes"],
    },
}


def guidance_for(section_type: str) -> dict[str, object]:
    """Return guidance metadata for a section type."""

    return SECTION_GUIDANCE.get(section_type, SECTION_GUIDANCE["unknown"])
