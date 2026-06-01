from pathlib import Path

from sec_filing_legal_decoder.cli import main


def test_zh_cn_reports_hide_raw_ui_terms_but_preserve_source_excerpts(tmp_path: Path):
    input_path = tmp_path / "sample.htm"
    input_path.write_text(
        "<html><body><p>Form 20-F Annual Report</p>"
        "<p>The auditor expressed substantial doubt about the company's ability to continue as a going concern.</p>"
        "<p>The company is a foreign private issuer and follows home-country governance practices.</p>"
        "</body></html>",
        encoding="utf-8",
    )
    output_dir = tmp_path / "zh"

    result = main(
        [
            "risk-cards",
            str(input_path),
            "--lang",
            "zh-CN",
            "--issuer-profile",
            "foreign-private-issuer",
            "--output-dir",
            str(output_dir),
        ]
    )

    assert result == 0
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            output_dir / "legal-risk-review.md",
            output_dir / "legal-risk-cards.md",
            output_dir / "evidence-audit.md",
            output_dir / "escalation-questions.md",
            output_dir / "management-follow-up.md",
        ]
    )

    assert "法律风险复核" in combined
    assert "主要确认方" in combined
    assert "substantial doubt" in combined
    for raw_term in ["route out", "Priority:", "Owners:", "read-first", "appendix-level", "lower-priority"]:
        assert raw_term not in combined
