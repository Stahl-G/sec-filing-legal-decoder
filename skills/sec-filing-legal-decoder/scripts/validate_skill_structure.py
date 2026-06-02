#!/usr/bin/env python3
"""Validate the sec-filing-legal-decoder skill package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
ROOT = SKILL_DIR.parents[1]

REQUIRED_REFERENCES = [
    "source-priority.md",
    "output-contract.md",
    "privacy-and-sanitization.md",
    "zh-cn-legal-style.md",
    "risk-taxonomy.md",
    "source-only-review.md",
    "update-workflow.md",
]
REQUIRED_EXAMPLES = [
    "prompt-basic-risk-cards.md",
    "prompt-zh-cn-risk-review.md",
    "prompt-review-overlay.md",
    "prompt-small-issuer-source-only.md",
]
REQUIRED_TRIGGERS = ["10-K", "20-F", "legal risk cards", "SEC filing", "Chinese", "source-only"]
BANNED_PLACEHOLDER_TERMS = [
    "INTERNAL_" + "COMPANY_NAME",
    "PRIVATE_" + "ISSUER_NAME",
    "MATERIAL_" + "NON_PUBLIC",
]
SKIP_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", "outputs"}
SKIP_SUFFIXES = {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip"}


def main() -> int:
    failures: list[str] = []
    skill_path = SKILL_DIR / "SKILL.md"
    manifest_path = SKILL_DIR / "skill.json"

    if not skill_path.exists():
        failures.append("SKILL.md is missing")
        frontmatter: dict[str, str] = {}
        body = ""
    else:
        frontmatter, body = _parse_frontmatter(skill_path.read_text(encoding="utf-8"))
        if not frontmatter:
            failures.append("SKILL.md YAML frontmatter is missing or invalid")

    for key in ["name", "description", "version"]:
        if key not in frontmatter:
            failures.append(f"SKILL.md frontmatter missing {key}")

    description = frontmatter.get("description", "")
    if "This skill should be used when" not in description:
        failures.append("description must contain 'This skill should be used when'")
    for trigger in REQUIRED_TRIGGERS:
        if trigger not in description:
            failures.append(f"description missing trigger phrase: {trigger}")

    if frontmatter.get("name") != "sec-filing-legal-decoder":
        failures.append("frontmatter name must be sec-filing-legal-decoder")

    if not manifest_path.exists():
        failures.append("skill.json is missing")
        manifest: dict[str, object] = {}
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if manifest.get("version") != str(frontmatter.get("version", "")):
        failures.append("skill.json version must match SKILL.md version")
    if manifest.get("default_review_mode") != "source-only":
        failures.append("skill.json default_review_mode must be source-only")

    failures.extend(_required_files("references", REQUIRED_REFERENCES))
    failures.extend(_required_files("examples", REQUIRED_EXAMPLES))
    failures.extend(_body_links(body))
    failures.extend(_privacy_findings())

    if failures:
        print("Skill validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Skill validation passed: {SKILL_DIR}")
    return 0


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, flags=re.DOTALL)
    if not match:
        return {}, text
    raw, body = match.groups()
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, body


def _required_files(folder: str, names: list[str]) -> list[str]:
    failures: list[str] = []
    for name in names:
        if not (SKILL_DIR / folder / name).exists():
            failures.append(f"missing {folder}/{name}")
    return failures


def _body_links(body: str) -> list[str]:
    failures: list[str] = []
    for name in REQUIRED_REFERENCES:
        if f"references/{name}" not in body:
            failures.append(f"SKILL.md does not reference references/{name}")
    for name in REQUIRED_EXAMPLES:
        if f"examples/{name}" not in body:
            failures.append(f"SKILL.md does not reference examples/{name}")
    return failures


def _privacy_findings() -> list[str]:
    terms = list(BANNED_PLACEHOLDER_TERMS)
    local_terms = ROOT / "sensitive_terms.txt"
    if local_terms.exists():
        for line in local_terms.read_text(encoding="utf-8").splitlines():
            value = line.strip()
            if value and not value.startswith("#"):
                terms.append(value)

    findings: list[str] = []
    for path in _scan_paths():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(text.splitlines(), start=1):
            for term in terms:
                if term and term in line:
                    findings.append(f"{path.relative_to(ROOT)}:{index}: contains {term}")
    return findings


def _scan_paths() -> list[Path]:
    paths = [
        SKILL_DIR / "SKILL.md",
        SKILL_DIR / "skill.json",
        *sorted((SKILL_DIR / "references").glob("*.md")),
        *sorted((SKILL_DIR / "examples").glob("*.md")),
        *sorted((SKILL_DIR / "scripts").glob("*")),
    ]
    return [path for path in paths if path.exists() and path.is_file() and not _skip(path)]


def _skip(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in SKIP_PARTS for part in rel.parts):
        return True
    return path.suffix.lower() in SKIP_SUFFIXES


if __name__ == "__main__":
    raise SystemExit(main())
