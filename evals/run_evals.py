"""Run deterministic eval cases."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sec_filing_legal_decoder.classifiers import classify_section, triage_paragraph
from sec_filing_legal_decoder.crosswalk.escalation_questions import generate_escalation_questions
from sec_filing_legal_decoder.crosswalk.finance_relevance_map import guidance_for
from sec_filing_legal_decoder.parser_backends import choose_backend
from sec_filing_legal_decoder.reports import render_integrated_legal_risk_review
from sec_filing_legal_decoder.reports.zh_cn_reports import render_integrated_legal_risk_review_zh_cn
from sec_filing_legal_decoder.risk_cards import generate_risk_card_report
from sec_filing_legal_decoder.schemas import ParsedDocument


def main() -> int:
    failures: list[str] = []
    failures.extend(_eval_classifier())
    failures.extend(_eval_triage())
    failures.extend(_eval_escalation())
    failures.extend(_eval_finance_mapping())
    failures.extend(_eval_v04_risk_cards())
    failures.extend(_eval_v04_issuer_profiles())
    failures.extend(_eval_v04_zh_cn_quality())
    failures.extend(_eval_v042_golden_fixtures())

    passed = "PASS" if not failures else "FAIL"
    total = _case_count()
    print(f"{passed}: {total - len(failures)}/{total} eval checks passed")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


def _load(name: str) -> list[dict[str, object]]:
    path = ROOT / "evals" / "cases" / name
    return json.loads(path.read_text(encoding="utf-8"))


def _eval_classifier() -> list[str]:
    failures: list[str] = []
    for case in _load("classifier_cases.json"):
        actual = classify_section(str(case["text"]))
        expected = str(case["expected_section_type"])
        if actual != expected:
            failures.append(f"classifier/{case['name']}: expected {expected}, got {actual}")
    return failures


def _eval_triage() -> list[str]:
    failures: list[str] = []
    for case in _load("triage_cases.json"):
        result = triage_paragraph(str(case["text"]), str(case["section_type"]))
        expected = str(case["expected_reading_decision"])
        if result.reading_decision != expected:
            failures.append(
                f"triage/{case['name']}: expected {expected}, got {result.reading_decision}"
            )
    return failures


def _eval_escalation() -> list[str]:
    failures: list[str] = []
    for case in _load("escalation_cases.json"):
        questions = generate_escalation_questions(
            str(case["section_type"]),
            str(case["reading_decision"]),
            list(case["signals"]),
        )
        for role in case["expected_roles"]:
            if role not in questions:
                failures.append(f"escalation/{case['name']}: missing role {role}")
    return failures


def _eval_finance_mapping() -> list[str]:
    failures: list[str] = []
    for case in _load("finance_mapping_cases.json"):
        guidance = guidance_for(str(case["section_type"]))
        blob = " ".join(str(value) for value in guidance.values()).lower()
        for term in case["expected_terms"]:
            if str(term).lower() not in blob:
                failures.append(f"finance_mapping/{case['name']}: missing term {term}")
    return failures


def _eval_v04_risk_cards() -> list[str]:
    failures: list[str] = []
    for case in _load("v04_risk_card_cases.json"):
        report = generate_risk_card_report(_document(str(case["text"])))
        expected_count = case.get("expected_card_count")
        if expected_count is not None and len(report.risk_cards) != int(expected_count):
            failures.append(
                f"v04_risk_cards/{case['name']}: expected {expected_count} cards, got {len(report.risk_cards)}"
            )
        markdown = render_integrated_legal_risk_review(report).lower()
        for term in case.get("forbidden_terms", []):
            if str(term).lower() in markdown:
                failures.append(f"v04_risk_cards/{case['name']}: forbidden term {term}")
    return failures


def _eval_v04_issuer_profiles() -> list[str]:
    failures: list[str] = []
    for case in _load("v04_issuer_profile_cases.json"):
        report = generate_risk_card_report(_document(str(case["text"])), issuer_profile=str(case["profile"]))
        card = next((card for card in report.risk_cards if card.risk_domain == case["expected_domain"]), None)
        if card is None:
            failures.append(f"v04_issuer_profiles/{case['name']}: missing domain {case['expected_domain']}")
            continue
        if card.priority != case["expected_priority"]:
            failures.append(
                f"v04_issuer_profiles/{case['name']}: expected priority {case['expected_priority']}, got {card.priority}"
            )
        if card.recommended_review_posture != case["expected_posture"]:
            failures.append(
                f"v04_issuer_profiles/{case['name']}: expected posture {case['expected_posture']}, got {card.recommended_review_posture}"
            )
    return failures


def _eval_v04_zh_cn_quality() -> list[str]:
    failures: list[str] = []
    for case in _load("v04_zh_cn_quality_cases.json"):
        report = generate_risk_card_report(_document(str(case["text"])), issuer_profile="small-issuer")
        markdown = render_integrated_legal_risk_review_zh_cn(report)
        for term in case["expected_terms"]:
            if str(term) not in markdown:
                failures.append(f"v04_zh_cn_quality/{case['name']}: missing term {term}")
        for term in case["forbidden_terms"]:
            if str(term) in markdown:
                failures.append(f"v04_zh_cn_quality/{case['name']}: forbidden term {term}")
    return failures


def _eval_v042_golden_fixtures() -> list[str]:
    failures: list[str] = []
    for case in _load("v042_golden_fixture_cases.json"):
        path = ROOT / str(case["path"])
        document = choose_backend("auto", path).parse(path)
        report = generate_risk_card_report(document, issuer_profile=str(case["issuer_profile"]))
        actual_domains = {card.risk_domain for card in report.risk_cards}
        for domain in case["expected_risk_domains"]:
            if str(domain) not in actual_domains:
                failures.append(f"v042_golden_fixtures/{case['name']}: missing domain {domain}")
        for field in [
            "expected_issue_titles",
            "expected_owners",
            "expected_do_not_overstate",
            "expected_action_artifacts",
        ]:
            if not case.get(field):
                failures.append(f"v042_golden_fixtures/{case['name']}: missing contract field {field}")
    return failures


def _case_count() -> int:
    return sum(len(_load(name)) for name in [
        "classifier_cases.json",
        "triage_cases.json",
        "escalation_cases.json",
        "finance_mapping_cases.json",
        "v04_risk_card_cases.json",
        "v04_issuer_profile_cases.json",
        "v04_zh_cn_quality_cases.json",
        "v042_golden_fixture_cases.json",
    ])


def _document(text: str) -> ParsedDocument:
    return ParsedDocument(
        source_path="eval-sample.htm",
        content=f"Form 20-F Annual Report\n\n{text}",
        parser_backend="html",
        title="Sample Eval Filing",
    )


if __name__ == "__main__":
    raise SystemExit(main())
