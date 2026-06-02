# AGENTS.md

## Project Rules

- Do not commit confidential company documents, private filings, credentials, or
  raw logs.
- Do not commit material non-public information, internal legal/finance advice,
  personal data, private transaction facts, or local filing outputs.
- Use synthetic examples or clearly public filing excerpts only. Prefer
  synthetic names in README, tests, evals, docs, and examples.
- Preserve the distinction between parser backends and filing workflow logic.
- MinerU must remain optional; EDGAR HTML, Markdown, and TXT analysis should work without it.
- v0.4.1 is deterministic, rule-based, and source-only. Future LLM or external
  enrichment adapters should be isolated behind adapter boundaries.
- Outputs must not claim to provide legal advice, investment advice, accounting
  advice, audit advice, or professional conclusions.
- When modifying scripts or behavior, run tests or at least a smoke test before
  completion.

## Git Workflow

- Through the `0.4.2` bridge release, maintainers may make direct `main` updates
  only for roadmap, project-board, release, or emergency maintenance work.
- After `0.4.2`, default to a pull-request workflow:
  create a `codex/...` feature branch, commit there, push the branch, and open a
  PR against `main`.
- Do not push directly to `main` after `0.4.2` unless the user explicitly asks
  for a hotfix/direct push.
- PR titles, descriptions, branch names, and commit messages must follow the
  same privacy rules as source files.

## Preferred Workflow

- Use `sec-filing-legal-decoder risk-cards` as the primary command.
- Use `--review-mode source-only`; v0.4.1 does not add web, news, analyst,
  market-data, or database enrichment.
- Choose an issuer profile when useful:
  `general`, `small-issuer`, `foreign-private-issuer`, `spac-de-spac`,
  `manufacturing`, or `solar-manufacturing`.
- Read `legal-risk-review.md` first. Treat `legal-risk-cards.md`,
  `evidence-audit.md`, `escalation-questions.md`, and
  `management-follow-up.md` as supporting files.
- Use `analyze` only for legacy paragraph-level output.
