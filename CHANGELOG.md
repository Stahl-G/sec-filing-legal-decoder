# Changelog

All notable changes to `sec-filing-legal-decoder` are documented here.

## 0.4.2

### Added
- Golden synthetic fixture contracts for the pre-0.5 issue-first refactor.
- Synthetic policy reliance, tax/DTA, and litigation contingency filing examples.
- Product-quality scoring for future issue-first reports.
- Output compatibility placeholders: `issues`, `functional_action_plan`, and `evidence_appendix`.
- Terminology and output compatibility documentation.

### Changed
- Clarified risk domain vs risk card vs risk issue language.
- Updated README, skill package, source-only docs, and report tags to v0.4.2.

### Workflow
- Completed the bridge release before switching default future work to pull requests.

## 0.4.1

### Added
- Anthropic-style / agent-readable `SKILL.md` frontmatter.
- Skill references for source priority, output contract, source-only review, privacy guardrails, and zh-CN legal style.
- Synthetic agent prompt examples.
- Skill validation and smoke-test scripts.

### Changed
- Clarified skill trigger description and primary risk-card workflow.
- Kept Python CLI as the core execution layer and skill wrapper as the agent entrypoint.

### Security / Privacy
- Reinforced no-private-company, no-internal-filing, no-MNPI rule for skill files, examples, tests, and generated outputs.

## 0.4.0

### Added
- Source-only review metadata in risk-card Markdown frontmatter and JSON output.
- `--review-mode source-only` for explicit filing-only review workflows.
- `--issuer-profile` priority calibration for general, small issuer, foreign private issuer, SPAC/de-SPAC, manufacturing, and solar manufacturing review contexts.
- `sec-filing-legal-decoder --version`.
- Development, update, release, and privacy documentation.
- Local sensitive-term scanner using gitignored `sensitive_terms.txt`.
- Synthetic examples for small FPI, de-SPAC, manufacturing, and solar manufacturing scenarios.

### Changed
- `risk-cards` remains the primary workflow; `analyze` is documented as legacy/debug output.
- Chinese output uses Chinese-first labels and role questions while preserving key SEC/legal/accounting terms.

### Security / Privacy
- Added stronger privacy guardrails for private filings, internal company names, credentials, raw logs, and material non-public information.
- Added gitignore coverage for private filings, private outputs, local filings, and local sensitive-term lists.

## 0.3.1

### Changed
- Simplified Chinese output usage to `--lang zh-CN`.
- Removed the misleading `translated` term style from the public CLI.

## 0.3.0

### Added
- Integrated `legal-risk-review.md` as the first-read report.
- Sharper read-first card consolidation and issue-level legal risk review.
- Chinese bilingual Markdown output.
- `financial_analysis_difference` on each risk card.

## 0.2.1

### Added
- Evidence filtering, evidence quality scoring, issuer-specific facts, and evidence audit output.

## 0.2.0

### Added
- `risk-cards` workflow for issue-level legal risk cards.
- `review-overlay` workflow for comparing existing finance analysis against filing risk cards.

## 0.1.1

### Added
- Obsidian-friendly Markdown output and vault export.

## 0.1.0

### Added
- Rule-based legal-heavy paragraph classification, legal-to-finance notes, escalation questions, and Markdown/JSON reports.
