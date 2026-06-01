"""Command-line interface for sec-filing-legal-decoder."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sec_filing_legal_decoder.crosswalk import analyze_document
from sec_filing_legal_decoder.parser_backends import ParserError, choose_backend
from sec_filing_legal_decoder.reports import (
    ObsidianExportOptions,
    export_obsidian_vault,
    render_json_report,
    render_management_memo,
    render_markdown_report,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sec-filing-legal-decoder",
        description="Decode legal-heavy SEC filing sections into finance-readable notes.",
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
        help="Relative folder inside the Obsidian vault, such as 'SEC Filings/TSLA/2025 10-K'.",
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


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
