# Release Process

This project uses semantic versioning while it is pre-1.0.

- `0.3.x`: Chinese bilingual risk-card output and consolidation.
- `0.4.1`: agent-readable skill package, source-only review, issuer profiles, update workflow, and privacy guardrails.
- `0.5.0`: prior-year wording diff.
- `0.6.0`: industry playbooks.

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
10. Tag release, for example `git tag -a v0.4.1 -m "v0.4.1"`.
11. Push main and tag.

## Release Check Command

```bash
scripts/release_check.sh
```

Do not commit generated outputs from private or user-specific filing tests.
