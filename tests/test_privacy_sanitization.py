import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_sensitive_terms",
    ROOT / "scripts" / "check_sensitive_terms.py",
)
assert SPEC and SPEC.loader
check_sensitive_terms = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_sensitive_terms)


def test_sensitive_term_scanner_detects_configured_terms(tmp_path: Path):
    sample = tmp_path / "sample.md"
    sample.write_text("This line contains PRIVATE_TEST_TOKEN.", encoding="utf-8")

    findings = check_sensitive_terms._scan_file(sample, ["PRIVATE_TEST_TOKEN"])

    assert findings
    assert "PRIVATE_TEST_TOKEN" in findings[0]


def test_sensitive_term_scanner_skips_binary_suffix(tmp_path: Path):
    sample = tmp_path / "sample.pdf"
    sample.write_text("PRIVATE_TEST_TOKEN", encoding="utf-8")

    assert check_sensitive_terms._scan_file(sample, ["PRIVATE_TEST_TOKEN"]) == []
