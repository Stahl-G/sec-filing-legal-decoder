from pathlib import Path

import pytest

from filing_crosswalk.parser_backends import (
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


def test_choose_backend_auto_markdown():
    assert choose_backend("auto", Path("sample.md")).name == "markdown"


def test_mineru_backend_helpful_when_missing(monkeypatch, tmp_path: Path):
    path = tmp_path / "sample.pdf"
    path.write_bytes(b"%PDF-1.4")
    monkeypatch.setenv("PATH", "")
    monkeypatch.delenv("MINERU_CLI_COMMAND", raising=False)
    with pytest.raises(ParserError, match="MinerU CLI was requested"):
        MinerUCliBackend().parse(path)
