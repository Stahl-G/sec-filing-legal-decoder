"""Base parser backend protocol and backend selection."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from sec_filing_legal_decoder.schemas import ParsedDocument


class ParserError(RuntimeError):
    """Raised when a parser backend cannot produce text."""


class ParserBackend(ABC):
    """Interface for document-to-text parser adapters."""

    name: str

    @abstractmethod
    def supports(self, path: Path) -> bool:
        """Return whether this backend can parse the given path."""

    @abstractmethod
    def parse(self, path: Path) -> ParsedDocument:
        """Parse an input path into a ParsedDocument."""


def choose_backend(parser_name: str, path: Path) -> ParserBackend:
    """Choose a parser backend by explicit name or input suffix."""

    from .markdown_backend import MarkdownParserBackend
    from .html_backend import HtmlParserBackend
    from .mineru_cli_backend import MinerUCliBackend
    from .mock_backend import MockParserBackend
    from .plaintext_backend import PlainTextParserBackend

    normalized = parser_name.lower().strip()
    by_name: dict[str, ParserBackend] = {
        "markdown": MarkdownParserBackend(),
        "md": MarkdownParserBackend(),
        "html": HtmlParserBackend(),
        "htm": HtmlParserBackend(),
        "inline-xbrl": HtmlParserBackend(),
        "ixbrl": HtmlParserBackend(),
        "text": PlainTextParserBackend(),
        "txt": PlainTextParserBackend(),
        "plain-text": PlainTextParserBackend(),
        "mineru-cli": MinerUCliBackend(),
        "mineru": MinerUCliBackend(),
        "mock": MockParserBackend(),
    }

    if normalized != "auto":
        try:
            return by_name[normalized]
        except KeyError as exc:
            valid = ", ".join(["auto", *sorted(by_name)])
            raise ParserError(f"Unknown parser '{parser_name}'. Valid options: {valid}") from exc

    auto_backends: list[ParserBackend] = [
        HtmlParserBackend(),
        MarkdownParserBackend(),
        PlainTextParserBackend(),
    ]
    for backend in auto_backends:
        if backend.supports(path):
            return backend

    return MinerUCliBackend()
