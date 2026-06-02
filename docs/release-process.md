# Release Process

This project uses semantic versioning while it is pre-1.0.

- `0.3.x`: Chinese bilingual risk-card output and consolidation.
- `0.4.1`: agent-readable skill package, source-only review, issuer profiles, update workflow, and privacy guardrails.
- `0.4.2`: pre-0.5 quality baseline, compatibility contract, terminology cleanup, and PR-based workflow transition.
- `0.5.0`: issue-first reports and functional action planning.
- `0.6.0`: local evidence store / RAG-ready primitives without external RAG.

## Branch And PR Policy

Through the `0.4.2` bridge release, direct `main` updates are allowed only for
roadmap, project-board, release, or emergency maintenance work.

After `0.4.2`, use pull requests by default:

```bash
git switch main
git pull --ff-only
git switch -c codex/short-change-name
# edit, test, commit
git push -u origin codex/short-change-name
gh pr create --base main --head codex/short-change-name
```

Do not push directly to `main` after `0.4.2` unless the user explicitly asks for
a hotfix/direct push.

PR titles, descriptions, branches, commits, and screenshots must not include
private filing names, internal company names, credentials, raw logs, or material
non-public information.

## Release Checklist

1. Update `pyproject.toml` version.
2. Update package `__version__`.
3. Update `skills/sec-filing-legal-decoder/skill.json`.
4. Update `CHANGELOG.md`.
5. Run `pytest`.
6. Run an English `risk-cards` smoke test.
7. Run a `zh-CN` smoke test.
8. Run the privacy/sensitive-term check.
9. Commit with a message that does not include private company names or private scenarios.
10. For post-`0.4.2` work, open a PR and merge to `main` after checks pass.
11. Tag release, for example `git tag -a v0.4.2 -m "v0.4.2"`.
12. Push the tag.

## Release Check Command

```bash
scripts/release_check.sh
```

Do not commit generated outputs from private or user-specific filing tests.
