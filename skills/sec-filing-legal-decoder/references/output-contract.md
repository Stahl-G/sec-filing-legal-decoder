# Output Contract

The `risk-cards` workflow writes a small review package. Read files in this
order.

## `legal-risk-review.md`

First-read integrated review. Use it to brief the user on the main legal-risk
themes, management questions, and what not to overstate.

Primary readers: finance, management, IR, legal coordinator, agent.

## `legal-risk-cards.md`

Issue-level card appendix. Use it to inspect each risk domain, source excerpts,
owners, questions, and evidence details.

Primary readers: legal, finance, audit, IR, management.

## `escalation-questions.md`

Role-organized question list. Use it to prepare follow-up questions for Legal,
Finance, Auditor, IR, Board, or Management.

Primary readers: project owner, analyst, agent.

## `management-follow-up.md`

Management action list. Use it to identify who should confirm what before the
review becomes a conclusion.

Primary readers: management, finance lead, project coordinator.

## `evidence-audit.md`

Audit trail for accepted, weak, or suppressed evidence. Use it to debug why a
paragraph did or did not support a card.

Primary readers: agent, maintainer, reviewer.

## `legal-risk-cards.json`

Machine-readable card output. Use it for downstream workflows, tests, evals, or
structured review pipelines.

Primary readers: software agents and scripts.
