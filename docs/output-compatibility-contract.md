# Output Compatibility Contract

This contract preserves v0.4.x outputs while preparing for v0.5 issue-first
reports.

## Existing v0.4 Files

The `risk-cards` command must continue to write:

- `legal-risk-review.md`
- `legal-risk-cards.md`
- `legal-risk-cards.json`
- `evidence-audit.md`
- `escalation-questions.md`
- `management-follow-up.md`

The Markdown files remain Obsidian-friendly by default.

## JSON Top-Level Fields

From v0.4.2 onward, `legal-risk-cards.json` includes both current v0.4 fields
and placeholders for future v0.5 issue-first outputs:

```json
{
  "risk_cards": [],
  "issues": [],
  "functional_action_plan": {},
  "evidence_appendix": []
}
```

Current v0.4 behavior:

- `risk_cards` contains the generated domain-grouped risk cards.
- `issues` is an empty list.
- `functional_action_plan` is an empty object.
- `evidence_appendix` is an empty list.

Future v0.5 behavior:

- `risk_cards` remains available for compatibility.
- `issues` contains reader-facing issue objects synthesized from one or more
  risk cards.
- `functional_action_plan` contains role-based actions and output artifacts.
- `evidence_appendix` contains structured evidence references suitable for
  downstream review.

## Source-Only Boundary

All fields remain source-only unless a future workflow explicitly adds external
enrichment and marks that mode in metadata. The default `risk-cards` workflow
must not mix web, news, analyst, market-data, database, or user-private context
into these fields.

## Compatibility Rule

Downstream tools should tolerate the v0.4.2 placeholders and should not assume
`issues`, `functional_action_plan`, or `evidence_appendix` are populated until
v0.5 introduces issue-first generation.
