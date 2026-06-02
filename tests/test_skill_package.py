import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "sec-filing-legal-decoder"


def test_skill_frontmatter_and_manifest_versions_match():
    text = SKILL_DIR.joinpath("SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    assert match
    frontmatter = _frontmatter(match.group(1))
    manifest = json.loads(SKILL_DIR.joinpath("skill.json").read_text(encoding="utf-8"))

    assert frontmatter["name"] == "sec-filing-legal-decoder"
    assert frontmatter["version"] == "0.4.1"
    assert manifest["version"] == frontmatter["version"]
    assert "This skill should be used when" in frontmatter["description"]
    for trigger in ["10-K", "20-F", "legal risk cards", "SEC filing", "Chinese", "source-only"]:
        assert trigger in frontmatter["description"]


def test_skill_required_resources_exist():
    required = [
        "references/source-priority.md",
        "references/output-contract.md",
        "references/privacy-and-sanitization.md",
        "references/zh-cn-legal-style.md",
        "examples/prompt-basic-risk-cards.md",
        "examples/prompt-zh-cn-risk-review.md",
        "scripts/validate_skill_structure.py",
        "scripts/run_smoke_test.sh",
    ]
    for rel in required:
        assert SKILL_DIR.joinpath(rel).exists(), rel


def test_validate_skill_structure_script_passes():
    result = subprocess.run(
        [sys.executable, str(SKILL_DIR / "scripts" / "validate_skill_structure.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_skill_package_avoids_private_placeholder_terms():
    banned = ["INTERNAL_" + "COMPANY_NAME", "PRIVATE_" + "ISSUER_NAME", "MATERIAL_" + "NON_PUBLIC"]
    paths = [
        SKILL_DIR / "SKILL.md",
        SKILL_DIR / "skill.json",
        *SKILL_DIR.joinpath("references").glob("*.md"),
        *SKILL_DIR.joinpath("examples").glob("*.md"),
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    for term in banned:
        assert term not in combined


def _frontmatter(raw: str) -> dict[str, str]:
    data = {}
    for line in raw.splitlines():
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data
