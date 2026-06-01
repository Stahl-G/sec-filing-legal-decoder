"""Command-line interface for sec-filing-legal-decoder."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sec_filing_legal_decoder import __version__
from sec_filing_legal_decoder.crosswalk import analyze_document
from sec_filing_legal_decoder.obsidian import RiskCardObsidianOptions, export_risk_cards_to_obsidian
from sec_filing_legal_decoder.overlay import build_overlay_report
from sec_filing_legal_decoder.parser_backends import ParserError, choose_backend
from sec_filing_legal_decoder.reports import (
    ObsidianExportOptions,
    export_obsidian_vault,
    render_evidence_audit_report,
    render_escalation_questions_report,
    render_integrated_legal_risk_review,
    render_json_report,
    render_legal_risk_cards_report,
    render_management_follow_up_report,
    render_management_memo,
    render_markdown_report,
    render_overlay_report,
    render_risk_cards_json_report,
)
from sec_filing_legal_decoder.risk_cards import generate_risk_card_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sec-filing-legal-decoder",
        description="Decode legal-heavy SEC filing sections into finance-readable notes.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"sec-filing-legal-decoder {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Analyze SEC HTML, Markdown, TXT, or MinerU-parsed input.")
    analyze.add_argument("input", type=Path, help="Input HTML/Markdown/TXT/PDF/Office path.")
    analyze.add_argument(
        "--parser",
        default="auto",
        help="Parser backend: auto, html, markdown, text, mineru-cli, or mock.",
    )
    analyze.add_argument("--out", type=Path, help="Markdown report output path.")
    analyze.add_argument("--json", type=Path, help="JSON report output path.")
    analyze.add_argument("--obsidian-vault", type=Path, help="Obsidian vault root path.")
    analyze.add_argument(
        "--obsidian-folder",
        help="Relative folder inside the Obsidian vault, such as 'SEC Filings/SAMPLE/2025 20-F'.",
    )
    analyze.add_argument("--company", help="Company name for Obsidian frontmatter.")
    analyze.add_argument("--ticker", help="Ticker for Obsidian frontmatter.")
    analyze.add_argument("--form", help="Form type for Obsidian frontmatter, such as 10-K or 20-F.")
    analyze.add_argument("--year", help="Filing year for Obsidian frontmatter.")

    memo = subparsers.add_parser("memo", help="Generate a management memo Markdown file.")
    memo.add_argument("input", type=Path, help="Input HTML/Markdown/TXT/PDF/Office path.")
    memo.add_argument(
        "--parser",
        default="auto",
        help="Parser backend: auto, html, markdown, text, mineru-cli, or mock.",
    )
    memo.add_argument("--out", type=Path, required=True, help="Memo output path.")

    risk_cards = subparsers.add_parser(
        "risk-cards",
        help="Generate source-only legal risk cards and integrated legal risk review for finance readers.",
    )
    risk_cards.add_argument("input", type=Path, help="Input SEC HTML/Markdown/TXT/PDF/Office path.")
    risk_cards.add_argument(
        "--parser",
        default="auto",
        help="Parser backend: auto, html, markdown, text, mineru-cli, or mock.",
    )
    risk_cards.add_argument("--out", type=Path, help="Legal risk cards Markdown output path.")
    risk_cards.add_argument("--json", type=Path, help="Legal risk cards JSON output path.")
    risk_cards.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for legal-risk-review.md, legal-risk-cards.md/json, evidence-audit.md, escalation-questions.md, and management-follow-up.md.",
    )
    risk_cards.add_argument("--review-out", type=Path, help="Integrated legal risk review Markdown output path.")
    risk_cards.add_argument("--questions-out", type=Path, help="Escalation questions Markdown output path.")
    risk_cards.add_argument("--management-follow-up-out", type=Path, help="Management follow-up Markdown output path.")
    risk_cards.add_argument("--evidence-audit-out", type=Path, help="Evidence audit Markdown output path.")
    risk_cards.add_argument("--obsidian-dir", type=Path, help="Obsidian folder for v0.4 risk-card notes.")
    risk_cards.add_argument(
        "--review-mode",
        choices=["source-only"],
        default="source-only",
        help="Review mode. v0.4 supports source-only filing review.",
    )
    risk_cards.add_argument(
        "--issuer-profile",
        choices=[
            "general",
            "small-issuer",
            "foreign-private-issuer",
            "spac-de-spac",
            "manufacturing",
            "solar-manufacturing",
        ],
        default="general",
        help="Issuer profile used to calibrate priority without creating unsupported cards.",
    )
    risk_cards.add_argument(
        "--lang",
        choices=["en", "zh-CN"],
        default="en",
        help="Markdown report language: en or zh-CN.",
    )
    risk_cards.add_argument(
        "--term-style",
        choices=["english", "bilingual"],
        default="bilingual",
        help="Advanced: domain title style for non-English reports. Default: bilingual.",
    )
    risk_cards.add_argument("--company", help="Company name for Obsidian frontmatter.")
    risk_cards.add_argument("--ticker", help="Ticker for Obsidian frontmatter.")
    risk_cards.add_argument("--form", help="Form type for Obsidian frontmatter, such as 10-K or 20-F.")
    risk_cards.add_argument("--year", help="Filing year for Obsidian frontmatter.")

    overlay = subparsers.add_parser(
        "review-overlay",
        help="Compare filing risk cards against an existing finance or earnings analysis.",
    )
    overlay.add_argument("input", type=Path, help="Input SEC HTML/Markdown/TXT/PDF/Office path.")
    overlay.add_argument("--analysis", type=Path, required=True, help="Existing finance or earnings analysis Markdown/TXT path.")
    overlay.add_argument(
        "--parser",
        default="auto",
        help="Parser backend: auto, html, markdown, text, mineru-cli, or mock.",
    )
    overlay.add_argument("--out", type=Path, help="Review overlay Markdown output path.")
    overlay.add_argument("--json", type=Path, help="Review overlay JSON output path.")
    overlay.add_argument("--output-dir", type=Path, help="Directory for review-overlay.md/json.")
    overlay.add_argument("--obsidian-dir", type=Path, help="Obsidian folder for underlying risk-card notes.")
    overlay.add_argument("--company", help="Company name for Obsidian frontmatter.")
    overlay.add_argument("--ticker", help="Ticker for Obsidian frontmatter.")
    overlay.add_argument("--form", help="Form type for Obsidian frontmatter, such as 10-K or 20-F.")
    overlay.add_argument("--year", help="Filing year for Obsidian frontmatter.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "analyze":
            return _analyze(
                args.input,
                args.parser,
                args.out,
                args.json,
                args.obsidian_vault,
                args.obsidian_folder,
                args.company,
                args.ticker,
                args.form,
                args.year,
            )
        if args.command == "memo":
            return _memo(args.input, args.parser, args.out)
        if args.command == "risk-cards":
            return _risk_cards(
                args.input,
                args.parser,
                args.out,
                args.json,
                args.output_dir,
                args.review_out,
                args.questions_out,
                args.management_follow_up_out,
                args.evidence_audit_out,
                args.obsidian_dir,
                args.review_mode,
                args.issuer_profile,
                args.lang,
                args.term_style,
                args.company,
                args.ticker,
                args.form,
                args.year,
            )
        if args.command == "review-overlay":
            return _review_overlay(
                args.input,
                args.analysis,
                args.parser,
                args.out,
                args.json,
                args.output_dir,
                args.obsidian_dir,
                args.company,
                args.ticker,
                args.form,
                args.year,
            )
    except ParserError as exc:
        print(f"Parser error: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"I/O error: {exc}", file=sys.stderr)
        return 3

    parser.error("Unknown command")
    return 2


def _analyze(
    input_path: Path,
    parser_name: str,
    markdown_out: Path | None,
    json_out: Path | None,
    obsidian_vault: Path | None,
    obsidian_folder: str | None,
    company: str | None,
    ticker: str | None,
    form: str | None,
    year: str | None,
) -> int:
    if (obsidian_vault is None) != (obsidian_folder is None):
        raise ParserError("--obsidian-vault and --obsidian-folder must be provided together.")

    backend = choose_backend(parser_name, input_path)
    document = backend.parse(input_path)
    report = analyze_document(document)
    markdown = render_markdown_report(report)

    if markdown_out is None and json_out is None and obsidian_vault is None:
        print(markdown)
        return 0

    if markdown_out is not None:
        _write_text(markdown_out, markdown)
    if json_out is not None:
        _write_text(json_out, render_json_report(report))
    if obsidian_vault is not None and obsidian_folder is not None:
        export_obsidian_vault(
            report,
            ObsidianExportOptions(
                vault=obsidian_vault,
                folder=obsidian_folder,
                company=company,
                ticker=ticker,
                form=form,
                year=year,
            ),
        )
    return 0


def _memo(input_path: Path, parser_name: str, out: Path) -> int:
    backend = choose_backend(parser_name, input_path)
    document = backend.parse(input_path)
    report = analyze_document(document)
    _write_text(out, render_management_memo(report))
    return 0


def _risk_cards(
    input_path: Path,
    parser_name: str,
    markdown_out: Path | None,
    json_out: Path | None,
    output_dir: Path | None,
    review_out: Path | None,
    questions_out: Path | None,
    management_follow_up_out: Path | None,
    evidence_audit_out: Path | None,
    obsidian_dir: Path | None,
    review_mode: str,
    issuer_profile: str,
    lang: str,
    term_style: str,
    company: str | None,
    ticker: str | None,
    form: str | None,
    year: str | None,
) -> int:
    backend = choose_backend(parser_name, input_path)
    document = backend.parse(input_path)
    report = generate_risk_card_report(
        document,
        review_mode=review_mode,
        issuer_profile=issuer_profile,
    )

    review_markdown = render_integrated_legal_risk_review(report, lang=lang, term_style=term_style)
    markdown = render_legal_risk_cards_report(report, lang=lang, term_style=term_style)
    if output_dir is not None:
        _write_text(output_dir / "legal-risk-review.md", review_markdown)
        _write_text(output_dir / "legal-risk-cards.md", markdown)
        _write_text(output_dir / "legal-risk-cards.json", render_risk_cards_json_report(report))
        _write_text(output_dir / "evidence-audit.md", render_evidence_audit_report(report, lang=lang))
        _write_text(output_dir / "escalation-questions.md", render_escalation_questions_report(report, lang=lang, term_style=term_style))
        _write_text(
            output_dir / "management-follow-up.md",
            render_management_follow_up_report(report, lang=lang, term_style=term_style),
        )

    if review_out is not None:
        _write_text(review_out, review_markdown)
    if markdown_out is not None:
        _write_text(markdown_out, markdown)
    if json_out is not None:
        _write_text(json_out, render_risk_cards_json_report(report))
    if questions_out is not None:
        _write_text(questions_out, render_escalation_questions_report(report, lang=lang, term_style=term_style))
    if management_follow_up_out is not None:
        _write_text(management_follow_up_out, render_management_follow_up_report(report, lang=lang, term_style=term_style))
    if evidence_audit_out is not None:
        _write_text(evidence_audit_out, render_evidence_audit_report(report, lang=lang))
    if obsidian_dir is not None:
        export_risk_cards_to_obsidian(
            report,
            RiskCardObsidianOptions(
                output_dir=obsidian_dir,
                lang=lang,
                term_style=term_style,
                company=company,
                ticker=ticker,
                form=form,
                year=year,
            ),
        )

    if (
        output_dir is None
        and review_out is None
        and markdown_out is None
        and json_out is None
        and questions_out is None
        and management_follow_up_out is None
        and evidence_audit_out is None
        and obsidian_dir is None
    ):
        print(review_markdown)
    return 0


def _review_overlay(
    input_path: Path,
    analysis_path: Path,
    parser_name: str,
    markdown_out: Path | None,
    json_out: Path | None,
    output_dir: Path | None,
    obsidian_dir: Path | None,
    company: str | None,
    ticker: str | None,
    form: str | None,
    year: str | None,
) -> int:
    backend = choose_backend(parser_name, input_path)
    document = backend.parse(input_path)
    report = build_overlay_report(document, analysis_path)
    markdown = render_overlay_report(report)

    if output_dir is not None:
        _write_text(output_dir / "review-overlay.md", markdown)
        _write_text(output_dir / "review-overlay.json", render_risk_cards_json_report(report))
    if markdown_out is not None:
        _write_text(markdown_out, markdown)
    if json_out is not None:
        _write_text(json_out, render_risk_cards_json_report(report))
    if obsidian_dir is not None:
        export_risk_cards_to_obsidian(
            report.risk_card_report,
            RiskCardObsidianOptions(
                output_dir=obsidian_dir,
                company=company,
                ticker=ticker,
                form=form,
                year=year,
            ),
        )
    if output_dir is None and markdown_out is None and json_out is None and obsidian_dir is None:
        print(markdown)
    return 0


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
