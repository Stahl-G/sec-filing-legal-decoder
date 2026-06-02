# Roadmap

This roadmap tracks `sec-filing-legal-decoder` as a source-only
legal-to-finance review tool for SEC filings.

The product should not become a generic filing summarizer, earnings analysis
tool, legal advice tool, investment advice tool, accounting opinion tool, audit
opinion tool, or disclosure conclusion engine.

## Product Direction

Target workflow:

```text
SEC filing source text
-> evidence extraction
-> risk cards
-> issue thesis generation
-> controversy map
-> cross-functional action plan
-> evidence appendix
```

Core value:

```text
Identify company-specific legal / disclosure / governance / audit / tax /
commitment risks from filing evidence, explain why they matter to finance
readers, and show what Legal, Finance, Auditor, IR, Operations, Board, and
Management should do next.
```

## Privacy Boundary

Do not commit real employer names, internal company names, private filings,
internal memos, private transaction names, user-specific scenarios, material
non-public information, credentials, raw logs, screenshots, or generated reports
from private files.

Use synthetic issuer names in docs, examples, tests, evals, sample outputs,
issues, and PR descriptions.

Acceptable synthetic examples:

- `Sample Foreign Issuer`
- `Sample Small FPI`
- `Sample De-SPAC Issuer`
- `Sample Manufacturing Issuer`
- `Sample Renewable Manufacturer`
- `Example Annual Report Issuer`

## Repository Workflow Boundary

Through the `0.4.2` bridge release, direct `main` updates are allowed only for
roadmap, project-board, release, or emergency maintenance work.

After `0.4.2`, default to pull requests:

```text
feature branch -> tests / evals -> PR -> review / checks -> merge to main
```

Do not push directly to `main` after `0.4.2` unless the user explicitly requests
a hotfix/direct push.

## Product Positioning

Primary positioning:

```text
A source-only legal-to-finance review skill and CLI for turning legal-heavy SEC
filing language into risk issues, evidence chains, action plans, and management
follow-up notes.
```

Secondary positioning:

```text
A deterministic agent workflow for finance readers who need to understand
legal, regulatory, audit, tax, governance, related-party, debt, dilution,
guarantee, commitment, and disclosure risks in SEC filings.
```

## GitHub Project Fields

Recommended GitHub Project fields:

| Field | Values |
| --- | --- |
| Status | Todo, In Progress, Done |
| Milestone | 0.4.0, 0.4.1, 0.4.2, 0.5.0, 0.6.0, Future |
| Type | Feature, Refactor, Docs, Test, Eval, Security / Privacy, Release, Agent Skill |
| Priority | P0, P1, P2, P3 |
| Area | CLI, Risk Engine, Issues, Reports, Chinese Output, Docs, Skill, Privacy, Tests, Evals, Examples, Release |

Project convention: use `Todo` for planned `Ready` / `Backlog` work, `In
Progress` for active implementation, and `Done` for released or closed items.

## Milestones

### 0.4.0 — Source-Only Review, Version Workflow, Privacy Guardrails

Status: Done

Goal: stabilize the project as a source-only legal risk review tool for
under-covered issuers.

Delivered:

- Version and update workflow docs.
- `sec-filing-legal-decoder --version`.
- Privacy and sanitization docs.
- Gitignored private/local filing paths and outputs.
- Optional local sensitive-term scanner.
- Explicit `--review-mode source-only`.
- Source-only metadata in Markdown and JSON.
- `--issuer-profile` support for `general`, `small-issuer`,
  `foreign-private-issuer`, `spac-de-spac`, `manufacturing`, and
  `solar-manufacturing`.
- zh-CN output polish with Chinese-first labels and preserved English SEC/legal
  terms.
- README and AGENTS.md updated around the primary `risk-cards` workflow.

### 0.4.1 — Agent Skill Packaging

Status: Done

Goal: package the existing Python CLI as an agent-readable skill without
turning the repository into a platform-specific plugin.

Delivered:

- Anthropic-style `SKILL.md` YAML frontmatter.
- Agent trigger description for SEC filing legal-to-finance review.
- Skill references for source priority, output contract, privacy, source-only
  review, risk taxonomy, zh-CN style, and update workflow.
- Synthetic prompt examples.
- Skill validation script.
- Skill smoke-test script.
- Output validation script.
- README section for using the project as an agent skill.

### 0.4.2 — Pre-0.5 Quality Baseline

Status: Ready

Goal: add quality baselines before the issue-first refactor. This is a bridge
release and should not change core product behavior.

Purpose:

- Create golden synthetic fixtures for 0.5 regression testing.
- Define product-quality scoring before report structure changes.
- Lock compatibility expectations for existing risk-card outputs and new issue
  outputs.
- Clarify terminology before introducing `RiskIssue`.
- Switch the repository workflow to pull requests by default after `0.4.2`.

Planned fixtures:

```text
synthetic_small_fpi_20f.htm
synthetic_spac_despace_20f.htm
synthetic_manufacturing_10k.htm
synthetic_policy_reliance_20f.htm
synthetic_tax_dta_10k.htm
synthetic_litigation_contingency_10k.htm
```

Each fixture should define:

- Expected risk domains.
- Expected issue titles.
- Expected owners.
- Expected do-not-overstate cautions.
- Expected action artifacts.

Product-quality checks:

- `main_report_has_executive_thesis`
- `issue_count_between_3_and_6`
- `no_issue_title_is_raw_domain_name`
- `each_issue_has_one_sentence_conclusion`
- `each_issue_has_source_facts`
- `each_issue_has_owner_actions`
- `each_issue_has_do_not_overstate`
- `main_report_excerpt_ratio_under_25_percent`
- `functional_action_plan_has_output_artifacts`

Compatibility contract:

```json
{
  "risk_cards": [],
  "issues": [],
  "functional_action_plan": {},
  "evidence_appendix": []
}
```

Terminology:

- Risk domain: backend classification label.
- Risk card: evidence-backed legal-to-finance note grouped by domain.
- Risk issue: controversy-based decision object synthesized from one or more
  risk cards.

### 0.5.0 — Issue-First Report And Functional Action Planner

Status: Ready after 0.4.2 baseline

Goal: upgrade from risk-card reading summary to issue-first decision support.

Current flow:

```text
Source excerpt -> risk category -> generic explanation -> questions to ask
```

Target flow:

```text
Core controversy -> evidence chain -> legal / finance / IR implications ->
cross-functional action plan
```

Principle: risk cards are backend evidence and taxonomy objects. Issues are
frontend decision-making objects.

Quality principle: a good issue is not a raw risk domain. A good issue states a
controversy, connects source facts to legal / finance / IR implications,
recommends concrete action artifacts, preserves evidence traceability, and
includes do-not-overstate cautions.

Planned report structure:

```text
# Executive Risk Thesis
# Controversy Map
# Issue Analysis
# Cross-Risk Connections
# Functional Action Plan
# Evidence Appendix
```

Planned schema:

```python
@dataclass(frozen=True)
class RiskIssue:
    issue_id: str
    issue_title: str
    one_sentence_conclusion: str
    why_it_matters_now: str
    risk_domains: list[str]
    related_card_ids: list[str]
    evidence_strength: str
    action_priority: str
    source_facts: list[str]
    evidence_chain: list[SourceExcerpt]
    legal_angle: str
    finance_angle: str
    tax_angle: str
    operations_angle: str
    ir_disclosure_angle: str
    auditor_angle: str
    board_management_angle: str
    preventive_actions: list[ActionItem]
    evidence_preservation: list[ActionItem]
    remediation_or_contingency_plan: list[ActionItem]
    disclosure_ir_alignment: list[ActionItem]
    do_not_overstate: list[str]


@dataclass(frozen=True)
class ActionItem:
    owner: str
    action: str
    rationale: str
    output_artifact: str | None = None


@dataclass(frozen=True)
class IssueReport:
    document: DocumentInfo
    review_mode: str
    issuer_profile: str
    executive_risk_thesis: str
    controversy_map: list[RiskIssue]
    functional_action_plan: dict[str, list[ActionItem]]
    evidence_appendix: list[SourceExcerpt]
    disclaimer: str
```

Planned modules:

```text
src/sec_filing_legal_decoder/issues/
  __init__.py
  issue_generator.py
  issue_templates.py
  issue_scorer.py
  action_planner.py
  evidence_chain.py
  controversy_rules.py
```

Issue templates should be added before renderers so English, zh-CN, Obsidian,
and overlay outputs can reuse the same deterministic issue logic.

Planned template families:

- `CommitmentDownsideExposureTemplate`
- `TaxSustainabilityTemplate`
- `LitigationContingencyTemplate`
- `PolicyRelianceTemplate`
- `GoingConcernMitigationTemplate`
- `RelatedPartyDependenceTemplate`

Planned issue types:

- Supply and capacity commitments: growth infrastructure or downside exposure?
- Tax benefit sustainability and jurisdictional assumption risk.
- Litigation contingency: no accrual does not mean no exposure.
- Policy reliance risk and administrative challenge readiness.
- Liquidity plan credibility and going-concern mitigation support.
- Related-party dependence: transaction quality, support durability, and
  minority-holder protection.

Functional action plan categories:

- Preventive Actions
- Evidence Preservation
- Remediation / Contingency Planning
- Disclosure / IR Alignment

Default action language should use "prepare / verify / model / preserve /
review / confirm" framing. Avoid unsupported directives such as terminate the
contract, sue an agency, recognize a liability, disclose immediately, or
conclude violation unless the filing explicitly supports that statement.

Recommended output artifacts:

- Commitment exposure schedule.
- Tax benefit bridge.
- DTA realizability support memo.
- Litigation matter tracker.
- Disclosure consistency memo.
- Policy reliance dossier.
- Board approval evidence pack.
- Scenario sensitivity model.

Issue JSON should include structured required outputs, not only prose action
items:

```json
{
  "required_outputs": [
    {
      "artifact": "DTA realizability support memo",
      "owner": "Finance / Auditor",
      "purpose": "Support more-likely-than-not realization assumptions"
    }
  ]
}
```

Compatibility requirement: keep existing outputs:

```text
legal-risk-review.md
legal-risk-cards.md
legal-risk-cards.json
evidence-audit.md
escalation-questions.md
management-follow-up.md
```

Add:

```text
legal-risk-issues.md
functional-action-plan.md
```

Acceptance criteria:

- `legal-risk-review.md` becomes issue-first.
- Report has Executive Risk Thesis.
- Report has Controversy Map.
- Report has Issue Analysis.
- Report has Functional Action Plan.
- Report has Evidence Appendix.
- No main section is only titled "Questions to Ask".
- Every issue has one-sentence conclusion.
- Every issue has owner-specific action items.
- Every issue has do-not-overstate cautions.
- Long excerpts move to the appendix.
- Existing risk-card outputs still exist.
- Every issue traces to at least one related risk card or source fact.
- Every issue includes source paragraph IDs or source facts.
- Issue titles do not equal raw domain titles.
- Main report source excerpt ratio stays under 25%.
- Functional action plan recommends output artifacts.
- Tests pass.

### 0.6.0 — Evidence Retrieval / RAG-Ready Store

Status: Backlog

Goal: make the project RAG-ready without introducing external retrieval
dependencies too early.

Add structured local evidence primitives first:

```text
EvidenceStore
EvidencePack
paragraph_id
source_ref
document_section
risk_domains
evidence_quality
issuer_specific_facts
```

Supported future use cases:

- Prior-year diff.
- Multi-document review.
- Local retrieval.
- Issue evidence chaining.

Out of scope before issue-first reports are stable:

- Vector DB.
- Embedding API.
- External news RAG.
- Law-firm memo ingestion.
- Public enrichment.
- Multi-source web search.

## Suggested GitHub Issues

### Done / Historical

| Title | Milestone | Type | Area | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| Rewrite AGENTS.md for v0.4 source-only workflow | 0.4.0 | Docs | Docs | P0 | Done |
| Add update workflow docs | 0.4.0 | Docs | Docs | P0 | Done |
| Add source-only metadata | 0.4.0 | Feature | Reports | P0 | Done |
| Add issuer profile support | 0.4.0 | Feature | Risk Engine | P1 | Done |
| Polish zh-CN output | 0.4.0 | Refactor | Chinese Output | P1 | Done |
| Add Anthropic-style SKILL.md | 0.4.1 | Agent Skill | Skill | P1 | Done |

### Ready / Next

| Title | Milestone | Type | Area | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| Add golden synthetic fixtures before issue-first refactor | 0.4.2 | Eval | Evals | P0 | Ready |
| Add product-quality scoring before v0.5 | 0.4.2 | Eval | Evals | P0 | Ready |
| Add backward compatibility contract for issue outputs | 0.4.2 | Docs | Reports | P0 | Ready |
| Clarify terminology: domain vs card vs issue | 0.4.2 | Docs | Docs | P2 | Ready |
| Adopt PR-based workflow after v0.4.2 | 0.4.2 | Docs | Release | P0 | Ready |
| Add issue synthesis schema | 0.5.0 | Feature | Issues | P1 | Ready after 0.4.2 |
| Add issue-first `legal-risk-review.md` | 0.5.0 | Refactor | Reports | P1 | Ready after 0.4.2 |
| Add functional action planner | 0.5.0 | Feature | Issues | P2 | Ready after 0.4.2 |
| Add issue-first zh-CN renderer | 0.5.0 | Feature | Chinese Output | P2 | Ready after 0.4.2 |
| Define issue quality rubric for v0.5 issue-first reports | 0.5.0 | Eval | Issues | P0 | Ready after 0.4.2 |
| Add risk-card-to-issue traceability | 0.5.0 | Feature | Issues | P0 | Ready after 0.4.2 |
| Add anti-overclaim rules for action planner | 0.5.0 | Security / Privacy | Issues | P0 | Ready after 0.4.2 |
| Add issue templates before report renderer | 0.5.0 | Feature | Issues | P1 | Ready after 0.4.2 |
| Add required artifact generator | 0.5.0 | Feature | Issues | P1 | Ready after 0.4.2 |
| Update review-overlay to compare against issues | 0.5.0 | Refactor | Reports | P1 | Ready after 0.4.2 |
| Update Obsidian export from card notes to issue notes | 0.5.0 | Feature | Reports | P1 | Ready after 0.4.2 |
| Add zh-CN issue-first action verb style guide | 0.5.0 | Refactor | Chinese Output | P2 | Ready after 0.4.2 |
| Add issue count and excerpt-ratio readability tests | 0.5.0 | Test | Reports | P2 | Ready after 0.4.2 |
| Add RAG-ready EvidenceStore | 0.6.0 | Feature | Risk Engine | P3 | Backlog |

## 0.4.2 Issue Breakdown

### P0 — Add Golden Synthetic Fixtures Before Issue-First Refactor

Type: Eval
Milestone: 0.4.2
Area: Evals
Priority: P0

Tasks:

- Add synthetic policy-reliance 20-F fixture.
- Add synthetic tax / DTA 10-K fixture.
- Add synthetic litigation contingency 10-K fixture.
- Keep existing small FPI / de-SPAC / manufacturing fixtures in the baseline.
- Define expected risk domains, issue titles, owners, cautions, and action
  artifacts.

### P0 — Add Product-Quality Scoring Before v0.5

Type: Eval
Milestone: 0.4.2
Area: Evals
Priority: P0

Tasks:

- Add executive-thesis check.
- Add issue-count range check.
- Add raw-domain-title rejection.
- Add source-facts / owner-actions / do-not-overstate checks.
- Add excerpt-ratio threshold.
- Add functional-action-plan output-artifact check.

### P0 — Add Backward Compatibility Contract For Issue Outputs

Type: Docs
Milestone: 0.4.2
Area: Reports
Priority: P0

Tasks:

- Document whether issues live in `legal-risk-cards.json` or
  `legal-risk-review.json`.
- Define top-level JSON fields for `issues`, `functional_action_plan`, and
  `evidence_appendix`.
- Preserve existing risk-card output files.
- Document new `legal-risk-issues.md` and `functional-action-plan.md` outputs.

### P2 — Clarify Terminology: Domain vs Card vs Issue

Type: Docs
Milestone: 0.4.2
Area: Docs
Priority: P2

Tasks:

- Define risk domain.
- Define risk card.
- Define risk issue.
- Update roadmap and docs before issue-first implementation.

### P0 — Adopt PR-Based Workflow After v0.4.2

Type: Docs
Milestone: 0.4.2
Area: Release
Priority: P0

Tasks:

- Document feature-branch workflow.
- Document `gh pr create` as the default post-0.4.2 delivery path.
- Update `AGENTS.md`, `CONTRIBUTING.md`, and release process docs.
- Allow direct `main` pushes only for explicit hotfix/direct-push requests after
  `0.4.2`.
- Keep PR metadata under the same privacy and sanitization rules as source
  files.

## 0.5.0 Issue Breakdown

### P0 — Define Issue Quality Rubric For v0.5 Issue-First Reports

Type: Eval
Milestone: 0.5.0
Area: Issues
Priority: P0

Tasks:

- Document that a good issue is not a raw risk domain.
- Require each issue to state a controversy.
- Require source facts connected to legal / finance / IR implications.
- Require action artifacts.
- Require do-not-overstate cautions.
- Add good and bad synthetic examples.

### P0 — Add Risk-Card-To-Issue Traceability

Type: Feature
Milestone: 0.5.0
Area: Issues
Priority: P0

Tasks:

- Require `related_card_ids` on every issue.
- Require `risk_domains` on every issue.
- Require source paragraph IDs or source facts.
- Carry evidence quality into issue synthesis.
- Expose weak or suppressed evidence notes when relevant.

### P0 — Add Anti-Overclaim Rules For Action Planner

Type: Security / Privacy
Milestone: 0.5.0
Area: Issues
Priority: P0

Tasks:

- Allow actions such as prepare support memo, build exposure schedule, preserve
  board materials, quantify scenarios, review disclosure consistency, and
  confirm with owners.
- Block unsupported actions such as terminate contract, sue agency, recognize
  liability, disclose immediately, or conclude violation.
- Add tests for forbidden action verbs and conclusions.
- Keep do-not-overstate cautions on every issue.

### P1 — Add Issue Synthesis Schema

Type: Feature
Milestone: 0.5.0
Area: Issues
Priority: P1

Tasks:

- Add `RiskIssue`.
- Add `ActionItem`.
- Add `IssueReport`.
- Add basic deterministic issue generator.
- Add tests for issue creation from existing risk cards.

### P1 — Add Issue Templates Before Report Renderer

Type: Feature
Milestone: 0.5.0
Area: Issues
Priority: P1

Tasks:

- Add `CommitmentDownsideExposureTemplate`.
- Add `TaxSustainabilityTemplate`.
- Add `LitigationContingencyTemplate`.
- Add `PolicyRelianceTemplate`.
- Add `GoingConcernMitigationTemplate`.
- Add `RelatedPartyDependenceTemplate`.
- Define default actions, do-not-overstate cautions, and required artifacts per
  template.

### P1 — Add Required Artifact Generator

Type: Feature
Milestone: 0.5.0
Area: Issues
Priority: P1

Tasks:

- Add `required_outputs` field to issue or action-plan output.
- Support artifact, owner, and purpose fields.
- Generate commitment exposure schedules, tax benefit bridges, DTA support
  memos, litigation trackers, disclosure consistency memos, policy reliance
  dossiers, board approval evidence packs, and scenario sensitivity models when
  supported.

### P1 — Add Issue-First `legal-risk-review.md`

Type: Refactor
Milestone: 0.5.0
Area: Reports
Priority: P1

Tasks:

- Add Executive Risk Thesis.
- Add Controversy Map.
- Add Issue Analysis.
- Add Functional Action Plan.
- Add Evidence Appendix.
- Keep old risk-card files.

### P1 — Update Review-Overlay To Compare Against Issues

Type: Refactor
Milestone: 0.5.0
Area: Reports
Priority: P1

Tasks:

- Compare existing financial analysis against issue thesis and controversy map.
- Add `covered_issues`.
- Add `under_explained_issues`.
- Add `misframed_issues`.
- Add `overstated_financial_claims`.
- Add `missing_action_items`.

### P1 — Update Obsidian Export From Card Notes To Issue Notes

Type: Feature
Milestone: 0.5.0
Area: Reports
Priority: P1

Tasks:

- Add `00 Executive Risk Thesis.md`.
- Add `01 Controversy Map.md`.
- Add `issues/ISSUE-*.md` notes.
- Keep `cards/RC-*.md` notes.
- Add `evidence/Evidence Appendix.md`.
- Link issues to cards and evidence paragraphs.

### P2 — Add Functional Action Planner

Type: Feature
Milestone: 0.5.0
Area: Issues
Priority: P2

Tasks:

- Add preventive actions.
- Add evidence preservation.
- Add remediation / contingency plan.
- Add disclosure / IR alignment.
- Add owner-based aggregation.
- Add output artifact recommendations.

### P2 — Add zh-CN Issue-First Action Verb Style Guide

Type: Refactor
Milestone: 0.5.0
Area: Chinese Output
Priority: P2

Tasks:

- Prefer cautious verbs: 核查, 量化, 建立台账, 形成支持 memo, 保留证据,
  拆分一次性 / 经常性影响, 准备情景分析, 校准披露口径, 提交管理层复核.
- Avoid overclaim verbs: 认定, 判定违法, 确认责任, 立即披露, 确认负债,
  unless explicitly supported.
- Update zh-CN legal style docs or add zh-CN action style docs.
- Add tests for forbidden overclaim verbs.

### P2 — Add Issue-First zh-CN Renderer

Type: Feature
Milestone: 0.5.0
Area: Chinese Output
Priority: P2

Tasks:

- Chinese issue-first structure.
- Chinese functional action plan.
- Chinese evidence appendix.
- Preserve key English SEC/legal/accounting terms.
- Add readability tests.

### P2 — Add Issue Count And Excerpt-Ratio Readability Tests

Type: Test
Milestone: 0.5.0
Area: Reports
Priority: P2

Tasks:

- Assert `3 <= issue_count <= 6` for fixture reports.
- Assert `main_report_source_excerpt_ratio < 25%`.
- Assert Evidence Appendix contains long excerpts.
- Assert no issue title equals a domain title.
- Assert no main section is titled only `Questions to Ask`.

### P3 — Add RAG-Ready EvidenceStore

Type: Feature
Milestone: 0.6.0
Area: Risk Engine
Priority: P3

Tasks:

- Add `EvidenceStore`.
- Add `EvidencePack`.
- Add paragraph metadata.
- Do not add vector DB yet.
- Do not add external RAG yet.
