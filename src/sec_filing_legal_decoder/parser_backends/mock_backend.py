"""Mock parser backend for demos and tests."""

from __future__ import annotations

from pathlib import Path

from sec_filing_legal_decoder.schemas import ParsedDocument

from .base import ParserBackend


class MockParserBackend(ParserBackend):
    """Return deterministic synthetic content without external parsers."""

    name = "mock"

    def supports(self, path: Path) -> bool:
        return True

    def parse(self, path: Path) -> ParsedDocument:
        if path.exists() and path.is_file():
            content = path.read_text(encoding="utf-8", errors="replace")
        else:
            content = (
                "The company may from time to time become involved in claims, "
                "litigation, or regulatory proceedings that could adversely "
                "affect its business.\n\n"
                "During the year, the company received a subpoena from the SEC "
                "related to revenue recognition and has accrued a liability of "
                "$4.2 million."
            )

        return ParsedDocument(
            source_path=str(path),
            content=content,
            parser_backend=self.name,
            title="Mock Filing Content",
            metadata={"format": "mock"},
        )
