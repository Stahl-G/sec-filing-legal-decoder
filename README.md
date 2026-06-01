# Filling-Crosswalker

Filling-Crosswalker is an initial open-source Python CLI project for
`filing-crosswalk`: a workflow layer for reading SEC filings, annual reports,
and legal-heavy corporate documents, especially SEC-style issuer reports such
as `20-F`, `10-K`, `10-Q`, and `40-F`.

It focuses on the non-financial filing language that can change financial
judgment: legal proceedings, regulatory risk, internal control weaknesses,
related-party transactions, debt covenants, guarantees, commitments, dilution,
and material contracts.

## What This Project Is

- A deterministic v0.1 toolkit for legal-to-finance filing triage.
- Especially useful for legal-heavy sections in `20-F`, `10-K`, `10-Q`, and
  `40-F` reports.
- A CLI that reads Markdown/TXT today and can optionally call MinerU for PDF or
  Office parsing.
- A source of structured crosswalk notes, escalation questions, Markdown
  reports, JSON output, and management memo drafts.
- A model-agnostic workflow layer that can later work with ChatGPT, Claude,
  Codex, OpenCode, local LLMs, or manual review.

## What This Project Is Not

- Not legal advice, investment advice, accounting advice, audit advice, or a
  substitute for professional review.
- Not a generic financial statement reader.
- Not a legal chatbot.
- Not a PDF parser and not a fork of MinerU.

## Why Not Another Financial Statement Reader

Many readers can handle revenue, margins, cash flow, and debt tables. The
slowdown often comes from legal-heavy filing sections where a finance reader
needs to know whether language is routine boilerplate, finance-relevant, or a
matter for Legal, Finance, Auditors, IR, Management, or the Board.

This project helps answer: should this paragraph be skipped, skimmed, read
closely, deeply reviewed, or escalated?

## How MinerU Fits

MinerU can handle document parsing: PDF, DOCX, PPTX, XLSX, images, and similar
inputs into Markdown or JSON suitable for agent and RAG workflows.

Filling-Crosswalker handles filing workflow intelligence after text exists:
section classification, legal-to-finance decoding, boilerplate vs material
triage, escalation question generation, and memo output.

This project can use MinerU as an optional document parsing backend. MinerU is
developed by OpenDataLab/MinerU Team and licensed under the MinerU Open Source
License, based on Apache 2.0 with additional conditions. This project is not
affiliated with OpenDataLab or MinerU. Users are responsible for complying with
MinerU's own license and service terms. If online services are ever built using
MinerU, documentation must state that the service uses MinerU.

## Quick Start For Agent Users

This project is designed to be agent-readable.

If you are using Codex, Claude Code, OpenCode, Cursor, Devin, or another coding
agent, give the agent this repository link and your filing input, then ask it
to install the project, read this README, run the smoke test, and generate a
report.

Suggested prompt:

```text
Please use this project:
https://github.com/YihongGuo/Filling-Crosswalker

Clone or open the repository, read README.md and AGENTS.md, install it in a
local virtual environment, run the built-in smoke test, then analyze my filing
Markdown/TXT file with filing-crosswalk. This is especially intended for
20-F, 10-K, 10-Q, and 40-F legal-heavy sections. Generate a Markdown report, a
JSON structured report, and, if useful, a management memo. Do not treat the
output as legal, investment, accounting, or audit advice.
```

For a first test, ask your agent to run the built-in synthetic example:

```text
Use the sample file examples/synthetic_legal_proceedings.md and generate:
- outputs/report.md
- outputs/report.json
Then summarize the top flagged paragraphs and escalation questions for me.
```

Expected result:

- A Markdown review report at `outputs/report.md`
- A structured JSON report at `outputs/report.json`
- Reading decisions such as `SKIM`, `DEEP_READ`, or `ESCALATE`
- Legal-to-finance notes and role-specific escalation questions
- A disclaimer reminding you that the output is only a triage aid

## 中文快速开始

这个项目更适合当作一个 **agent skill / agent-readable repository** 使用。

最简单的用法：把本仓库链接和你的 filing 文档交给 Codex、Claude Code、
OpenCode、Cursor 或其他 coding agent，让 agent 自己读取 `README.md` 和
`AGENTS.md`，安装依赖，运行 smoke test，然后生成报告。

可以直接复制下面这段给你的 agent：

```text
请使用这个项目：
https://github.com/YihongGuo/Filling-Crosswalker

请 clone 或打开这个仓库，阅读 README.md 和 AGENTS.md，在本地虚拟环境中安装
项目，先运行内置 smoke test，然后用 filing-crosswalk 分析我的 filing
Markdown/TXT 文件。这个项目特别适合 20-F、10-K、10-Q、40-F 中法律语言较重的
章节。请输出 Markdown review report、JSON structured report，并在有必要时生成
management memo。不要把输出当作法律、投资、会计或审计意见。
```

第一次试用可以让 agent 先跑内置样例：

```text
请使用 examples/synthetic_legal_proceedings.md 生成：
- outputs/report.md
- outputs/report.json
然后用中文总结 top flagged paragraphs 和 escalation questions。
```

## Manual Developer Setup

If you are running the project yourself from a terminal:

```bash
python -m pip install -e ".[dev]"
filing-crosswalk analyze examples/synthetic_legal_proceedings.md \
  --out outputs/report.md \
  --json outputs/report.json
```

Run tests and evals if you are modifying the code:

```bash
pytest
python evals/run_evals.py
```

## CLI Examples

Analyze Markdown or TXT from a filing, especially `20-F`, `10-K`, `10-Q`, or
`40-F` content:

```bash
filing-crosswalk analyze examples/synthetic_legal_proceedings.md \
  --out outputs/report.md \
  --json outputs/report.json
```

Analyze a PDF through MinerU if the MinerU CLI is installed and compatible:

```bash
filing-crosswalk analyze input.pdf --parser mineru-cli --out outputs/report.md
```

Generate a management memo:

```bash
filing-crosswalk memo examples/synthetic_internal_control.md --out outputs/memo.md
```

## Output Example

Each analyzed paragraph produces:

- `section_type`
- `plain_english_meaning`
- `boilerplate_or_material`
- `reading_decision`
- `business_relevance`
- `financial_relevance`
- `what_to_compare`
- `escalation_questions`
- `suggested_management_briefing_sentence`
- `confidence`
- `source_excerpt`

## Architecture

```text
src/filing_crosswalk/
  parser_backends/       # Markdown, TXT, MinerU CLI, mock parser adapters
  classifiers/           # Rule-based section classification and triage
  crosswalk/             # Finance relevance, reading decisions, questions
  reports/               # Markdown, JSON, and memo generation
  schemas/               # Dataclass output models
  utils/                 # Text splitting and source references
```

The default path runs without MinerU or an LLM API key.

## Safety And Confidentiality

- Do not include confidential company documents.
- Do not include material non-public information, raw logs, credentials, or
  personal data.
- Use synthetic examples or public filing excerpts.
- Treat all outputs as reading aids requiring professional review.

## Roadmap

v0.1:

- Rule-based legal-heavy paragraph classification
- Legal-to-finance note generation
- Escalation questions
- Markdown/JSON reports
- Optional MinerU CLI backend

v0.2:

- Prior-year wording diff reviewer
- SEC 20-F / 10-K section mapper
- EDGAR input adapter
- Better source citation and page references
- Optional LLM adapter

v0.3:

- Finance-to-legal decoder
- Governance-to-investor decoder
- Board / management briefing packs
- DOCX report export
- CI-based redaction checks

## Disclaimer

This project is not legal advice, investment advice, accounting advice, audit
advice, or a substitute for qualified professional review. It is designed to
help readers classify, simplify, and triage legal-heavy filing language and
generate better escalation questions. Users should consult qualified legal,
accounting, audit, or investment professionals before relying on any output.
