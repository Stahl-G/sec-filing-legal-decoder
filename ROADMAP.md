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
| Status | Backlog, Ready, In Progress, In Review, Blocked, Done |
| Milestone | 0.4.0, 0.4.1, 0.5.0, 0.6.0, Future |
| Type | Feature, Refactor, Docs, Test, Eval, Security / Privacy, Release, Agent Skill |
| Priority | P0, P1, P2, P3 |
| Area | CLI, Risk Engine, Issues, Reports, Chinese Output, Docs, Skill, Privacy, Tests, Evals, Examples, Release |

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

### 0.5.0 — Issue-First Report And Functional Action Planner

Status: Ready

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

Recommended output artifacts:

- Commitment exposure schedule.
- Tax benefit bridge.
- DTA realizability support memo.
- Litigation matter tracker.
- Disclosure consistency memo.
- Policy reliance dossier.
- Board approval evidence pack.
- Scenario sensitivity model.

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
| Add issue synthesis schema | 0.5.0 | Feature | Issues | P1 | Ready |
| Add issue-first `legal-risk-review.md` | 0.5.0 | Refactor | Reports | P1 | Ready |
| Add functional action planner | 0.5.0 | Feature | Issues | P2 | Ready |
| Add issue-first zh-CN renderer | 0.5.0 | Feature | Chinese Output | P2 | Ready |
| Add RAG-ready EvidenceStore | 0.6.0 | Feature | Risk Engine | P3 | Backlog |

## 0.5.0 Issue Breakdown

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
