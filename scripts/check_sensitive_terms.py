"""Local sensitive-term scanner for repository files."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TERMS: tuple[str, ...] = ()
SKIP_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "build",
    "dist",
    "outputs",
    "private_outputs",
    "local_filings",
    "private_filings",
}
SKIP_SUFFIXES = {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check local files for configured sensitive terms.")
    parser.add_argument("--staged", action="store_true", help="Scan staged files only.")
    args = parser.parse_args(argv)

    terms = _terms()
    files = _staged_files() if args.staged else _working_tree_files()
    findings: list[str] = []
    for path in files:
        findings.extend(_scan_file(path, terms))

    if findings:
        print("Sensitive-term check failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print(f"Sensitive-term check passed ({len(files)} file(s), {len(terms)} term(s)).")
    return 0


def _terms() -> list[str]:
    terms = [term.strip() for term in DEFAULT_TERMS if term.strip()]
    local_terms = ROOT / "sensitive_terms.txt"
    if local_terms.exists():
        for line in local_terms.read_text(encoding="utf-8").splitlines():
            value = line.strip()
            if value and not value.startswith("#"):
                terms.append(value)
    return terms


def _staged_files() -> list[Path]:
    output = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    ).stdout
    return [_clean_path(line) for line in output.splitlines() if line.strip()]


def _working_tree_files() -> list[Path]:
    output = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    ).stdout
    return [_clean_path(line) for line in output.splitlines() if line.strip()]


def _clean_path(value: str) -> Path:
    return (ROOT / value).resolve()


def _scan_file(path: Path, terms: list[str]) -> list[str]:
    if not path.exists() or path.is_dir() or _skip(path):
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    findings: list[str] = []
    for index, line in enumerate(text.splitlines(), start=1):
        for term in terms:
            if term and term in line:
                findings.append(f"{_display_path(path)}:{index}: contains {term}")
    return findings


def _skip(path: Path) -> bool:
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        return path.suffix.lower() in SKIP_SUFFIXES
    if any(part in SKIP_PARTS for part in rel.parts):
        return True
    return path.suffix.lower() in SKIP_SUFFIXES


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
