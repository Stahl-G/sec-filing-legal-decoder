import json
from pathlib import Path

from sec_filing_legal_decoder.quality import score_issue_report


ROOT = Path(__file__).resolve().parents[1]


def test_product_quality_baseline_passes_on_issue_contract():
    markdown = """
# Sample Issue-First Review

## Executive Thesis

The filing points to three decision issues: liquidity support, control remediation, and tax reserve support.

## Issue 1

Liquidity support depends on committed financing evidence, not only management intent.

## Evidence Appendix

> Source excerpts belong here, not in the main report.
"""
    issues = [
        _issue("Liquidity support credibility", "Liquidity support depends on committed financing evidence."),
        _issue("Control remediation timing", "Control remediation remains an audit-readiness question."),
        _issue("Tax reserve support", "Tax reserve support depends on jurisdiction-level evidence."),
    ]
    plan = {
        "Finance": [
            {
                "action": "Prepare support schedules before management review.",
                "output_artifact": "liquidity bridge memo and tax reserve support schedule",
            }
        ]
    }

    result = score_issue_report(markdown, issues, plan)

    assert result.passed, result.to_dict()


def test_product_quality_flags_raw_domain_issue_titles():
    markdown = "## Executive Thesis\n\nThe report has a thesis."
    issues = [
        _issue("audit_going_concern", "Liquidity support depends on committed financing evidence."),
        _issue("Control remediation timing", "Control remediation remains an audit-readiness question."),
        _issue("Tax reserve support", "Tax reserve support depends on jurisdiction-level evidence."),
    ]
    plan = {"Finance": [{"output_artifact": "support memo"}]}

    result = score_issue_report(markdown, issues, plan)
    failed = {check.name for check in result.failed_checks()}

    assert "no_issue_title_is_raw_domain_name" in failed


def test_product_quality_flags_excessive_main_report_source_excerpts():
    markdown = """
## Executive Thesis

The report has a thesis.

> Source excerpt one repeats filing text.
> Source excerpt two repeats filing text.
> Source excerpt three repeats filing text.
"""
    issues = [
        _issue("Liquidity support credibility", "Liquidity support depends on committed financing evidence."),
        _issue("Control remediation timing", "Control remediation remains an audit-readiness question."),
        _issue("Tax reserve support", "Tax reserve support depends on jurisdiction-level evidence."),
    ]
    plan = {"Finance": [{"output_artifact": "support memo"}]}

    result = score_issue_report(markdown, issues, plan)
    failed = {check.name for check in result.failed_checks()}

    assert "main_report_excerpt_ratio_under_25_percent" in failed


def test_v042_golden_fixture_contract_is_complete():
    cases = json.loads((ROOT / "evals" / "cases" / "v042_golden_fixture_cases.json").read_text(encoding="utf-8"))

    assert len(cases) == 6
    for case in cases:
        assert (ROOT / case["path"]).exists(), case["path"]
        assert case["expected_risk_domains"]
        assert case["expected_issue_titles"]
        assert case["expected_owners"]
        assert case["expected_do_not_overstate"]
        assert case["expected_action_artifacts"]


def _issue(title: str, conclusion: str) -> dict[str, object]:
    return {
        "issue_title": title,
        "one_sentence_conclusion": conclusion,
        "source_facts": ["Filing-backed fact with paragraph reference."],
        "owner_actions": [{"owner": "Finance", "action": "Prepare a support memo."}],
        "do_not_overstate": ["Do not present a conditional filing statement as resolved."],
    }
