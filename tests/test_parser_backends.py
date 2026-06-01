from pathlib import Path

import pytest

from sec_filing_legal_decoder.parser_backends import (
    HtmlParserBackend,
    MarkdownParserBackend,
    MinerUCliBackend,
    ParserError,
    PlainTextParserBackend,
    choose_backend,
)


def test_markdown_backend_reads_file(tmp_path: Path):
    path = tmp_path / "sample.md"
    path.write_text("# Title\n\nThe company may face legal proceedings from time to time.", encoding="utf-8")
    doc = MarkdownParserBackend().parse(path)
    assert doc.parser_backend == "markdown"
    assert "legal proceedings" in doc.content


def test_plaintext_backend_reads_file(tmp_path: Path):
    path = tmp_path / "sample.txt"
    path.write_text("The company received a subpoena from the SEC.", encoding="utf-8")
    doc = PlainTextParserBackend().parse(path)
    assert doc.parser_backend == "text"
    assert "subpoena" in doc.content


def test_html_backend_extracts_visible_inline_xbrl_text(tmp_path: Path):
    path = tmp_path / "tsla-20251231.htm"
    path.write_text(
        """
        <html>
          <head><title>Tesla 10-K</title><style>.x{display:none}</style></head>
          <body>
            <ix:hidden><ix:nonNumeric name="dei:EntityRegistrantName">Hidden Corp</ix:nonNumeric></ix:hidden>
            <h1>Item 1A. Risk Factors</h1>
            <p>The company received a subpoena from the SEC related to revenue recognition.</p>
            <script>var ignored = true;</script>
          </body>
        </html>
        """,
        encoding="utf-8",
    )
    doc = HtmlParserBackend().parse(path)
    assert doc.parser_backend == "html"
    assert doc.title == "Tesla 10-K"
    assert "Risk Factors" in doc.content
    assert "subpoena from the SEC" in doc.content
    assert "Hidden Corp" not in doc.content
    assert "ignored" not in doc.content


def test_choose_backend_auto_markdown():
    assert choose_backend("auto", Path("sample.md")).name == "markdown"


def test_choose_backend_auto_html():
    assert choose_backend("auto", Path("tsla-20251231.htm")).name == "html"


def test_mineru_backend_helpful_when_missing(monkeypatch, tmp_path: Path):
    path = tmp_path / "sample.pdf"
    path.write_bytes(b"%PDF-1.4")
    monkeypatch.setenv("PATH", "")
    monkeypatch.delenv("MINERU_CLI_COMMAND", raising=False)
    with pytest.raises(ParserError, match="MinerU CLI was requested"):
        MinerUCliBackend().parse(path)
