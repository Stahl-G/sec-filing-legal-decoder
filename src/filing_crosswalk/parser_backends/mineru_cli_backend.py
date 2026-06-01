"""Optional MinerU CLI parser backend.

This adapter intentionally does not vendor, fork, or copy MinerU. It invokes a
locally installed CLI through subprocess and then looks for Markdown output.
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path

from filing_crosswalk.schemas import ParsedDocument

from .base import ParserBackend, ParserError


class MinerUCliBackend(ParserBackend):
    """Parse PDF or Office files through an installed MinerU CLI."""

    name = "mineru-cli"
    suffixes = {".pdf", ".docx", ".pptx", ".xlsx", ".png", ".jpg", ".jpeg", ".webp"}

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.suffixes

    def _command(self) -> list[str]:
        configured = os.environ.get("MINERU_CLI_COMMAND")
        if configured:
            return shlex.split(configured)

        executable = shutil.which("mineru")
        if executable:
            return [executable]

        executable = shutil.which("magic-pdf")
        if executable:
            return [executable]

        raise ParserError(
            "MinerU CLI was requested, but no 'mineru' or 'magic-pdf' command "
            "was found. Install MinerU, set MINERU_CLI_COMMAND, or provide "
            "pre-parsed Markdown/TXT input."
        )

    def parse(self, path: Path) -> ParsedDocument:
        if not path.exists():
            raise ParserError(f"Input file does not exist: {path}")
        if not self.supports(path):
            raise ParserError(
                f"MinerU CLI backend expects PDF/Office/image input, got: "
                f"{path.suffix or '(no suffix)'}"
            )

        command = self._command()
        with tempfile.TemporaryDirectory(prefix="filing-crosswalk-mineru-") as tmp:
            output_dir = Path(tmp)
            completed = self._run(command, path, output_dir)
            markdown = self._find_markdown(output_dir)
            if markdown is None:
                raise ParserError(
                    "MinerU CLI completed but no Markdown output was found. "
                    f"Command stdout: {completed.stdout[-500:]}"
                )

            return ParsedDocument(
                source_path=str(path),
                content=markdown.read_text(encoding="utf-8", errors="replace"),
                parser_backend=self.name,
                title=path.stem.replace("_", " ").replace("-", " ").title(),
                metadata={
                    "format": path.suffix.lower().lstrip("."),
                    "mineru_command": " ".join(command),
                },
            )

    def _run(
        self, command: list[str], path: Path, output_dir: Path
    ) -> subprocess.CompletedProcess[str]:
        candidates = [
            [*command, "-p", str(path), "-o", str(output_dir)],
            [*command, str(path), "--output", str(output_dir)],
        ]
        errors: list[str] = []
        for candidate in candidates:
            completed = subprocess.run(
                candidate,
                capture_output=True,
                check=False,
                text=True,
                timeout=300,
            )
            if completed.returncode == 0:
                return completed
            errors.append(
                f"{' '.join(candidate)}\nSTDERR: {completed.stderr[-500:]}\n"
                f"STDOUT: {completed.stdout[-500:]}"
            )

        raise ParserError(
            "MinerU CLI command failed. Install a compatible MinerU CLI or "
            "provide pre-parsed Markdown/TXT input.\n\n" + "\n\n".join(errors)
        )

    @staticmethod
    def _find_markdown(output_dir: Path) -> Path | None:
        markdown_files = sorted(output_dir.rglob("*.md"))
        if not markdown_files:
            return None
        return max(markdown_files, key=lambda item: item.stat().st_size)
