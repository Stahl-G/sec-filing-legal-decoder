"""HTML and Inline XBRL parser backend for EDGAR main filing documents."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

from filing_crosswalk.schemas import ParsedDocument

from .base import ParserBackend, ParserError


class _VisibleTextHTMLParser(HTMLParser):
    """Extract visible text from filing HTML while ignoring hidden metadata."""

    _BLOCK_TAGS = {
        "address",
        "article",
        "aside",
        "blockquote",
        "br",
        "caption",
        "dd",
        "div",
        "dl",
        "dt",
        "figcaption",
        "figure",
        "footer",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hr",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "pre",
        "section",
        "table",
        "td",
        "th",
        "tr",
        "ul",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._chunks: list[str] = []
        self._skip_depth = 0
        self._title_parts: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized = tag.lower()
        attrs_dict = {name.lower(): (value or "") for name, value in attrs}
        if normalized in {"script", "style", "noscript"} or self._is_hidden(normalized, attrs_dict):
            self._skip_depth += 1
            return
        if normalized == "title":
            self._in_title = True
        if normalized in self._BLOCK_TAGS:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        normalized = tag.lower()
        if self._skip_depth:
            self._skip_depth -= 1
            return
        if normalized == "title":
            self._in_title = False
        if normalized in self._BLOCK_TAGS:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = data.strip()
        if not text:
            return
        if self._in_title:
            self._title_parts.append(text)
        self._chunks.append(text)
        self._chunks.append(" ")

    @staticmethod
    def _is_hidden(tag: str, attrs: dict[str, str]) -> bool:
        if tag in {"ix:hidden", "ix:header", "ix:references", "ix:resources"}:
            return True
        style = attrs.get("style", "").lower().replace(" ", "")
        if "display:none" in style or "visibility:hidden" in style:
            return True
        if attrs.get("hidden") is not None:
            return True
        aria_hidden = attrs.get("aria-hidden", "").lower()
        return aria_hidden == "true"

    def text(self) -> str:
        raw = "".join(self._chunks)
        raw = re.sub(r"[ \t\f\v]+", " ", raw)
        raw = re.sub(r" *\n *", "\n", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()

    def title(self) -> str | None:
        title = " ".join(part.strip() for part in self._title_parts if part.strip())
        return re.sub(r"\s+", " ", title).strip() or None


class HtmlParserBackend(ParserBackend):
    """Load SEC main filing HTML or Inline XBRL HTML into visible text."""

    name = "html"
    suffixes = {".htm", ".html", ".xhtml"}

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.suffixes

    def parse(self, path: Path) -> ParsedDocument:
        if not path.exists():
            raise ParserError(f"HTML file does not exist: {path}")
        if not self.supports(path):
            raise ParserError(f"Expected an HTML file, got: {path.suffix or '(no suffix)'}")

        content = path.read_text(encoding="utf-8", errors="replace")
        parser = _VisibleTextHTMLParser()
        parser.feed(content)
        text = parser.text()
        if not text:
            raise ParserError(f"No visible text could be extracted from HTML file: {path}")

        return ParsedDocument(
            source_path=str(path),
            content=text,
            parser_backend=self.name,
            title=parser.title() or path.stem.replace("_", " ").replace("-", " ").title(),
            metadata={"format": "html", "inline_xbrl_supported": True},
        )
