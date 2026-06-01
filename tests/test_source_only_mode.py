import json
from pathlib import Path

from sec_filing_legal_decoder.cli import main


def test_source_only_metadata_in_markdown_and_json(tmp_path: Path):
    input_path = tmp_path / "sample.htm"
    input_path.write_text(
        "<html><body><p>Form 20-F Annual Report</p>"
        "<p>The company disclosed a material weakness in internal control over financial reporting.</p>"
        "</body></html>",
        encoding="utf-8",
    )
    output_dir = tmp_path / "out"

    result = main(
        [
            "risk-cards",
            str(input_path),
            "--review-mode",
            "source-only",
            "--issuer-profile",
            "small-issuer",
            "--output-dir",
            str(output_dir),
        ]
    )

    assert result == 0
    review = output_dir.joinpath("legal-risk-review.md").read_text(encoding="utf-8")
    payload = json.loads(output_dir.joinpath("legal-risk-cards.json").read_text(encoding="utf-8"))

    assert "review_mode: source-only" in review
    assert "external_enrichment: false" in review
    assert "issuer_profile: small-issuer" in review
    assert payload["review_mode"] == "source-only"
    assert payload["external_enrichment"] is False
    assert payload["issuer_profile"] == "small-issuer"
