"""Deterministic product-quality checks for issue-first report contracts."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from sec_filing_legal_decoder.risk_cards.risk_domain_classifier import RISK_DOMAIN_PATTERNS


@dataclass(frozen=True)
class QualityCheck:
    """One deterministic product-quality check."""

    name: str
    passed: bool
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class QualityReport:
    """Product-quality result for an issue-first report contract."""

    checks: list[QualityCheck]

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.checks)

    def to_dict(self) -> dict[str, Any]:
        return {"passed": self.passed, "checks": [check.to_dict() for check in self.checks]}

    def failed_checks(self) -> list[QualityCheck]:
        return [check for check in self.checks if not check.passed]


def score_issue_report(
    markdown: str,
    issues: list[dict[str, Any]],
    functional_action_plan: dict[str, Any] | None = None,
) -> QualityReport:
    """Score a future issue-first report against the v0.4.2 quality contract."""

    plan = functional_action_plan or {}
    checks = [
        _check(
            "main_report_has_executive_thesis",
            _has_executive_thesis(markdown),
            "Expected an Executive Thesis section or callout in the main report.",
        ),
        _check(
            "issue_count_between_3_and_6",
            3 <= len(issues) <= 6,
            f"Expected 3-6 issues, found {len(issues)}.",
        ),
        _check(
            "no_issue_title_is_raw_domain_name",
            _no_raw_domain_titles(issues),
            "Issue titles should be decision-oriented, not raw risk-domain labels.",
        ),
        _check(
            "each_issue_has_one_sentence_conclusion",
            all(_has_one_sentence_conclusion(issue) for issue in issues),
            "Each issue needs a one-sentence conclusion.",
        ),
        _check(
            "each_issue_has_source_facts",
            all(_has_source_facts(issue) for issue in issues),
            "Each issue needs filing-backed source facts.",
        ),
        _check(
            "each_issue_has_owner_actions",
            all(_has_owner_actions(issue) for issue in issues),
            "Each issue needs owner/action follow-up items.",
        ),
        _check(
            "each_issue_has_do_not_overstate",
            all(_has_do_not_overstate(issue) for issue in issues),
            "Each issue needs a do-not-overstate guardrail.",
        ),
        _check(
            "main_report_excerpt_ratio_under_25_percent",
            _source_excerpt_ratio(markdown) < 0.25,
            f"Source excerpt ratio was {_source_excerpt_ratio(markdown):.1%}; expected under 25%.",
        ),
        _check(
            "functional_action_plan_has_output_artifacts",
            _plan_has_output_artifacts(plan),
            "Functional action plan needs output artifacts such as memo, schedule, tracker, or support file.",
        ),
    ]
    return QualityReport(checks)


def _check(name: str, passed: bool, failure_detail: str) -> QualityCheck:
    return QualityCheck(name=name, passed=passed, detail="" if passed else failure_detail)


def _has_executive_thesis(markdown: str) -> bool:
    lowered = markdown.lower()
    return bool(
        re.search(r"(^|\n)#{1,3}\s+executive thesis\b", lowered)
        or re.search(r">\s*\[!summary\]\s*executive thesis\b", lowered)
        or "executive_thesis:" in lowered
    )


def _no_raw_domain_titles(issues: list[dict[str, Any]]) -> bool:
    for issue in issues:
        title = _normalize_name(str(issue.get("issue_title") or issue.get("title") or ""))
        if not title or title in RAW_DOMAIN_NAMES:
            return False
    return True


def _has_one_sentence_conclusion(issue: dict[str, Any]) -> bool:
    conclusion = str(
        issue.get("one_sentence_conclusion")
        or issue.get("conclusion")
        or issue.get("executive_conclusion")
        or ""
    ).strip()
    if len(conclusion) < 20:
        return False
    sentences = [part for part in re.split(r"(?<=[.!?])\s+", conclusion) if part.strip()]
    return len(sentences) == 1


def _has_source_facts(issue: dict[str, Any]) -> bool:
    facts = issue.get("source_facts") or issue.get("filing_facts") or issue.get("evidence_facts")
    return isinstance(facts, list) and any(_nonempty_item(fact) for fact in facts)


def _has_owner_actions(issue: dict[str, Any]) -> bool:
    actions = (
        issue.get("owner_actions")
        or issue.get("actions")
        or issue.get("next_steps")
        or issue.get("required_actions")
    )
    if not isinstance(actions, list):
        return False
    for action in actions:
        if isinstance(action, dict):
            owner = str(action.get("owner") or action.get("role") or "").strip()
            text = str(action.get("action") or action.get("task") or action.get("follow_up") or "").strip()
            if owner and text:
                return True
        elif isinstance(action, str) and action.strip():
            return True
    return False


def _has_do_not_overstate(issue: dict[str, Any]) -> bool:
    guardrail = (
        issue.get("do_not_overstate")
        or issue.get("what_not_to_overstate")
        or issue.get("overstatement_guardrails")
    )
    if isinstance(guardrail, str):
        return bool(guardrail.strip())
    if isinstance(guardrail, list):
        return any(_nonempty_item(item) for item in guardrail)
    return False


def _source_excerpt_ratio(markdown: str) -> float:
    main = _main_report_body(markdown)
    if not main.strip():
        return 0.0
    excerpt_chars = 0
    for line in main.splitlines():
        stripped = line.strip()
        lowered = stripped.lower()
        if stripped.startswith(">") or "source excerpt" in lowered or lowered.startswith("excerpt:"):
            excerpt_chars += len(stripped)
    return excerpt_chars / max(len(main), 1)


def _main_report_body(markdown: str) -> str:
    match = re.search(r"(^|\n)#{1,3}\s+evidence appendix\b", markdown, flags=re.IGNORECASE)
    if not match:
        return markdown
    return markdown[: match.start()]


def _plan_has_output_artifacts(functional_action_plan: dict[str, Any]) -> bool:
    artifact_terms = ("artifact", "memo", "schedule", "tracker", "support", "worksheet", "matrix")
    if not functional_action_plan:
        return False
    return any(term in str(functional_action_plan).lower() for term in artifact_terms)


def _nonempty_item(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict):
        return any(str(item).strip() for item in value.values())
    return value is not None


def _normalize_name_set(values: dict[str, Any]) -> set[str]:
    return {_normalize_name(value) for value in values}


def _normalize_name(value: str) -> str:
    value = value.replace("_", " ").replace("-", " ").replace("/", " ")
    value = re.sub(r"[^a-zA-Z0-9 ]+", "", value)
    return re.sub(r"\s+", " ", value).strip().lower()


RAW_DOMAIN_NAMES = {
    *_normalize_name_set(RISK_DOMAIN_PATTERNS),
    "audit going concern",
    "internal control reporting",
    "legal proceedings litigation",
    "regulatory trade policy",
    "related party governance",
    "debt liquidity covenant",
    "guarantees commitments",
    "equity dilution control",
    "tax cross border",
    "management board governance",
    "disclosure ir consistency",
    "cybersecurity governance",
    "material contracts",
}
