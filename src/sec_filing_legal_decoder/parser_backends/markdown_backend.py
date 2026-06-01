"""Markdown parser backend."""

from __future__ import annotations

from pathlib import Path

from sec_filing_legal_decoder.schemas import ParsedDocument

from .base import ParserBackend, ParserError


class MarkdownParserBackend(ParserBackend):
    """Load pre-parsed Markdown filing content."""

    name = "markdown"
    suffixes = {".md", ".markdown"}

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.suffixes

    def parse(self, path: Path) -> ParsedDocument:
        if not path.exists():
            raise ParserError(f"Markdown file does not exist: {path}")
        if not self.supports(path):
            raise ParserError(f"Expected a Markdown file, got: {path.suffix or '(no suffix)'}")

        content = path.read_text(encoding="utf-8")
        return ParsedDocument(
            source_path=str(path),
            content=content,
            parser_backend=self.name,
            title=path.stem.replace("_", " ").replace("-", " ").title(),
            metadata={"format": "markdown"},
        )
