"""Run deterministic v0.1 eval cases."""

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


def main() -> int:
    failures: list[str] = []
    failures.extend(_eval_classifier())
    failures.extend(_eval_triage())
    failures.extend(_eval_escalation())
    failures.extend(_eval_finance_mapping())

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


def _case_count() -> int:
    return sum(len(_load(name)) for name in [
        "classifier_cases.json",
        "triage_cases.json",
        "escalation_cases.json",
        "finance_mapping_cases.json",
    ])


if __name__ == "__main__":
    raise SystemExit(main())
