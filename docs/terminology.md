# Terminology

Use these terms consistently in code, docs, issues, and release notes.

## Risk Domain

A risk domain is a backend classification label.

Examples:

- `legal_proceedings_litigation`
- `internal_control_reporting`
- `tax_cross_border`
- `regulatory_trade_policy`

Risk domains are useful for routing, grouping, deterministic templates, and
regression tests. They are not reader-facing conclusions.

## Risk Card

A risk card is an evidence-backed legal-to-finance note grouped by risk domain.

In v0.4.x, risk cards are the main structured output. A risk card should include
source excerpts, owners, finance relevance, legal or audit relevance, questions,
and a do-not-overstate guardrail.

Risk cards help readers decide where to look. They are not final legal,
accounting, audit, investment, or disclosure conclusions.

## Risk Issue

A risk issue is a future issue-first decision object synthesized from one or
more risk cards.

Risk issues should be controversy-based and reader-facing. They should explain:

- the one-sentence conclusion;
- the filing-backed facts;
- why the issue matters to finance readers;
- owner actions and expected output artifacts;
- what not to overstate.

## Practical Rule

Use risk domains inside the engine. Use risk cards as v0.4 evidence-backed
appendices. Use risk issues for v0.5 first-read reports and action planning.
