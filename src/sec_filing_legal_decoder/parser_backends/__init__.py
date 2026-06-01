"""Parser backend adapters."""

from .base import ParserBackend, ParserError, choose_backend
from .html_backend import HtmlParserBackend
from .markdown_backend import MarkdownParserBackend
from .mineru_cli_backend import MinerUCliBackend
from .mock_backend import MockParserBackend
from .plaintext_backend import PlainTextParserBackend

__all__ = [
    "MarkdownParserBackend",
    "HtmlParserBackend",
    "MinerUCliBackend",
    "MockParserBackend",
    "ParserBackend",
    "ParserError",
    "PlainTextParserBackend",
    "choose_backend",
]
