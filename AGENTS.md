# AGENTS.md

## Project Rules

- Do not commit confidential company documents, private filings, credentials, or
  raw logs.
- Use synthetic examples or public filing excerpts only.
- Preserve the distinction between parser backends and filing workflow logic.
- MinerU must remain optional; EDGAR HTML, Markdown, and TXT analysis should work without it.
- v0.1 is deterministic and rule-based. Future LLM adapters should be isolated
  behind adapter boundaries.
- Outputs must not claim to provide legal advice, investment advice, accounting
  advice, audit advice, or professional conclusions.
- When modifying scripts or behavior, run tests or at least a smoke test before
  completion.
