# SEC Filing Legal Decoder

Source-only legal risk review for `10-K`, `10-Q`, `20-F`, `40-F`, and annual
report filings.

SEC Filing Legal Decoder is an AI agent skill and Python CLI that turns
legal-heavy SEC filing language into finance-readable legal risk reviews,
issue-level risk cards, escalation questions, management follow-up items, and
Obsidian-friendly Markdown.

SEC Filing Legal Decoder 是一个 AI agent skill 和 Python CLI，用于把 SEC filing
中法律语言较重的内容，转换成金融读者可读的法律风险复核、事项级风险卡、升级问题、
管理层跟进事项和 Obsidian-friendly Markdown。

## What This Project Is

- A deterministic `v0.4.1` source-only review workflow with an agent-readable
  skill wrapper.
- A legal-to-finance decoder for legal proceedings, internal controls,
  regulatory risk, related-party transactions, debt covenants, guarantees,
  commitments, dilution, tax, cybersecurity governance, disclosure consistency,
  and material contracts.
- A risk-card generator that consolidates paragraphs into issue-level review
  themes.
- A CLI that reads SEC `.htm/.html` Inline XBRL main documents, Markdown, and
  TXT files without MinerU.
- An optional MinerU path for PDF, Office, image, or non-EDGAR fallback files.

## 这个项目是什么

- 一个 deterministic `v0.4.1` source-only review workflow，并带有 agent-readable
  skill wrapper。
- 一个 legal-to-finance decoder，覆盖法律诉讼、内控、监管、关联交易、债务
  covenant、担保、承诺事项、股权稀释、税务、网络安全治理、披露一致性和重大合同。
- 一个 risk-card generator，把原文段落合并成事项级风险主题。
- 一个 CLI，可以直接读取 SEC `.htm/.html` Inline XBRL 主文件、Markdown 和 TXT，
  不依赖 MinerU。
- 一个可选 MinerU 路径，用于 PDF、Office、图片或非 EDGAR fallback 文件。

## What This Project Is Not

- Not legal advice, investment advice, accounting advice, audit advice, or a
  substitute for qualified professional review.
- Not a generic financial statement reader.
- Not a PDF parser and not a MinerU wrapper.
- Not a disclosure conclusion engine.
- Not an external enrichment tool. `v0.4.1` does not add web, news, analyst, or
  database context to the filing.

## 这个项目不是什么

- 不是法律意见、投资意见、会计意见、审计意见，也不能替代专业人员复核。
- 不是通用财务报表阅读器。
- 不是 PDF parser，也不是 MinerU 套壳。
- 不是披露结论引擎。
- 不是外部信息增强工具。`v0.4.1` 不会把网页、新闻、卖方报告或数据库信息混入 filing。

## SEC Filing Source Priority

For standard SEC filings, prefer the official EDGAR main `.htm/.html` document.
Modern SEC annual and quarterly reports are usually HTML files with Inline XBRL
tags, so the same main document is both human-readable and machine-readable.

Recommended source order:

| Source | Practical meaning | Best use |
| --- | --- | --- |
| `.htm` / `.html` | Official EDGAR main filing, often Inline XBRL HTML | First choice for legal-risk review |
| `.txt` | SEC submission package | Archive/completeness checks; split before analysis |
| `.xml` / XBRL | Structured financial data | Numeric extraction and databases |
| `.pdf` | Often IR version or exhibit | Human reading only when HTML is unavailable |

## SEC filing 源文件优先级

标准 SEC filing 优先使用 EDGAR 官方主 `.htm/.html` 文件。现代 SEC 年报和季报的主
文件通常是带 Inline XBRL 标签的 HTML，所以同一份文件既能给人读，也能给机器解析。

建议优先级：

| 源文件 | 实质 | 最适合用途 |
| --- | --- | --- |
| `.htm` / `.html` | EDGAR 官方主 filing，通常是 Inline XBRL HTML | 法律风险复核第一选择 |
| `.txt` | SEC submission package | 归档和完整性检查；分析前应拆主文档 |
| `.xml` / XBRL | 结构化财务数据 | 财务数字抽取和数据库 |
| `.pdf` | 常见于 IR 展示版或附件 | 仅在 HTML 不可用时用于人工阅读 |

## Do I Need MinerU?

Usually no.

For `10-K`, `10-Q`, `20-F`, and `40-F`, use the official EDGAR `.htm/.html`
main filing whenever available. MinerU is only an optional fallback for PDF,
Office, image, or non-EDGAR documents.

## 我需要 MinerU 吗？

通常不需要。

分析 `10-K`、`10-Q`、`20-F`、`40-F` 时，优先使用 EDGAR 官方 `.htm/.html` 主
filing。MinerU 只是 PDF、Office、图片或非 EDGAR 文件的可选 fallback。

## Quick Start For Agent Users

Give this project link and your filing file to your coding agent:

```text
Please use this project:
https://github.com/Stahl-G/sec-filing-legal-decoder

Clone or open the repository, read README.md and AGENTS.md, install it in a
local virtual environment, run the smoke test, then analyze my SEC filing main
.htm/.html file with sec-filing-legal-decoder risk-cards. Use source-only mode.
Read legal-risk-review.md first, then use legal-risk-cards.md and
evidence-audit.md as supporting appendices.
```

## Agent 用户快速开始

把本项目链接和 filing 文件交给你的 coding agent：

```text
Please use this project:
https://github.com/Stahl-G/sec-filing-legal-decoder

Clone or open the repository, read README.md and AGENTS.md, install it in a
local virtual environment, run the smoke test, then analyze my SEC filing main
.htm/.html file with sec-filing-legal-decoder risk-cards. Use source-only mode.
Read legal-risk-review.md first, then use legal-risk-cards.md and
evidence-audit.md as supporting appendices.
```

## Use as an Agent Skill

The Python CLI is the execution layer. The agent-readable entrypoint is
`skills/sec-filing-legal-decoder/SKILL.md`, which tells coding agents when to
use this project, how to run the CLI, which outputs to read first, and which
safety boundaries to preserve.

This is not a legal advice plugin. It is source-only first, keeps the filing as
the evidence boundary, and supports Chinese bilingual legal-to-finance review.

Basic command:

```bash
sec-filing-legal-decoder risk-cards input.htm \
  --output-dir outputs/sample-risk-review
```

Chinese bilingual command:

```bash
sec-filing-legal-decoder risk-cards input.htm \
  --lang zh-CN \
  --output-dir outputs/sample-risk-review-zh
```

Validate the skill package:

```bash
python skills/sec-filing-legal-decoder/scripts/validate_skill_structure.py
```

## 作为 Agent Skill 使用

Python CLI 是执行层。Agent-readable 入口是
`skills/sec-filing-legal-decoder/SKILL.md`，它会告诉 coding agent 什么时候使用本项目、
如何运行 CLI、先读哪些输出文件，以及必须遵守哪些安全边界。

这不是法律意见插件。它优先采用 source-only review，把 filing 本身作为证据边界，
并支持中文双语 legal-to-finance review。

基础命令：

```bash
sec-filing-legal-decoder risk-cards input.htm \
  --output-dir outputs/sample-risk-review
```

中文双语命令：

```bash
sec-filing-legal-decoder risk-cards input.htm \
  --lang zh-CN \
  --output-dir outputs/sample-risk-review-zh
```

校验 skill package：

```bash
python skills/sec-filing-legal-decoder/scripts/validate_skill_structure.py
```

## Installation Guide For Beginners

Required tools:

- Python 3.10 or later
- Git
- A terminal

Install and test:

```bash
git clone https://github.com/Stahl-G/sec-filing-legal-decoder.git
cd sec-filing-legal-decoder
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ".[dev]"
sec-filing-legal-decoder --version
```

Windows PowerShell activation:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install ".[dev]"
sec-filing-legal-decoder --version
```

## 小白安装指南

必装工具：

- Python 3.10 或更高版本
- Git
- 一个终端

安装和测试：

```bash
git clone https://github.com/Stahl-G/sec-filing-legal-decoder.git
cd sec-filing-legal-decoder
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ".[dev]"
sec-filing-legal-decoder --version
```

Windows PowerShell 激活方式：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install ".[dev]"
sec-filing-legal-decoder --version
```

## First Smoke Test

```bash
sec-filing-legal-decoder risk-cards examples/synthetic_small_fpi_20f.htm \
  --review-mode source-only \
  --issuer-profile small-issuer \
  --output-dir outputs/smoke-small-fpi
```

Expected files:

- `legal-risk-review.md`
- `legal-risk-cards.md`
- `legal-risk-cards.json`
- `evidence-audit.md`
- `escalation-questions.md`
- `management-follow-up.md`

## 第一次 smoke test

```bash
sec-filing-legal-decoder risk-cards examples/synthetic_small_fpi_20f.htm \
  --review-mode source-only \
  --issuer-profile small-issuer \
  --output-dir outputs/smoke-small-fpi
```

预期文件：

- `legal-risk-review.md`
- `legal-risk-cards.md`
- `legal-risk-cards.json`
- `evidence-audit.md`
- `escalation-questions.md`
- `management-follow-up.md`

## Primary Command

```bash
sec-filing-legal-decoder risk-cards filing.htm \
  --review-mode source-only \
  --issuer-profile general \
  --output-dir outputs/sample-review
```

Chinese report:

```bash
sec-filing-legal-decoder risk-cards filing.htm \
  --review-mode source-only \
  --issuer-profile foreign-private-issuer \
  --lang zh-CN \
  --output-dir outputs/sample-review-zh
```

## 主要命令

```bash
sec-filing-legal-decoder risk-cards filing.htm \
  --review-mode source-only \
  --issuer-profile general \
  --output-dir outputs/sample-review
```

中文报告：

```bash
sec-filing-legal-decoder risk-cards filing.htm \
  --review-mode source-only \
  --issuer-profile foreign-private-issuer \
  --lang zh-CN \
  --output-dir outputs/sample-review-zh
```

## Issuer Profiles

`v0.4.1` includes issuer profiles for under-covered issuer review. Profiles adjust
priority only when the filing text supports that risk.

Supported profiles:

- `general`
- `small-issuer`
- `foreign-private-issuer`
- `spac-de-spac`
- `manufacturing`
- `solar-manufacturing`

## Issuer profile

`v0.4.1` 包含 issuer profile，适合 under-covered issuer review。Profile 只在
filing 原文支持相应风险时调整优先级。

支持：

- `general`
- `small-issuer`
- `foreign-private-issuer`
- `spac-de-spac`
- `manufacturing`
- `solar-manufacturing`

## Reading The Output

Start with `legal-risk-review.md`. It is the integrated first-read document that
connects the risk cards into a source-only review. Use `legal-risk-cards.md` as
the card appendix and `evidence-audit.md` to check what was routed in or out.

The JSON output includes:

- `review_mode`
- `external_enrichment`
- `issuer_profile`
- `coverage_summary`
- `risk_cards`
- `route_audit`

## 如何阅读输出

先读 `legal-risk-review.md`。这是从头看到尾的 integrated first-read document，会把
风险卡串成一份 source-only review。`legal-risk-cards.md` 是风险卡附录，
`evidence-audit.md` 用来核查哪些段落进入或排除。

JSON 输出包含：

- `review_mode`
- `external_enrichment`
- `issuer_profile`
- `coverage_summary`
- `risk_cards`
- `route_audit`

## Obsidian Export

The normal Markdown files are already Obsidian-friendly. Use `--obsidian-dir`
when you want linked notes inside a vault folder:

```bash
sec-filing-legal-decoder risk-cards filing.htm \
  --output-dir outputs/sample-review \
  --obsidian-dir ~/Documents/ObsidianVault/SEC\ Filings/SAMPLE/2025\ 20-F \
  --company "Sample Foreign Issuer" \
  --ticker SAMPLE \
  --form 20-F \
  --year 2025
```

## Obsidian 导出

默认 Markdown 已经适合 Obsidian 阅读。如果需要在 vault 里生成 linked notes，使用
`--obsidian-dir`：

```bash
sec-filing-legal-decoder risk-cards filing.htm \
  --output-dir outputs/sample-review \
  --obsidian-dir ~/Documents/ObsidianVault/SEC\ Filings/SAMPLE/2025\ 20-F \
  --company "Sample Foreign Issuer" \
  --ticker SAMPLE \
  --form 20-F \
  --year 2025
```

## Development

```bash
python -m pip install ".[dev]"
pytest
python evals/run_evals.py
scripts/run_smoke.sh
```

Local privacy check:

```bash
python scripts/check_sensitive_terms.py
```

## 开发

```bash
python -m pip install ".[dev]"
pytest
python evals/run_evals.py
scripts/run_smoke.sh
```

本地隐私检查：

```bash
python scripts/check_sensitive_terms.py
```

## Repository Safety

Do not commit confidential company documents, private filings, credentials, raw
logs, personal data, internal legal/finance advice, or material non-public
information. Use synthetic examples and public filing excerpts only.

## 仓库安全

不要提交公司机密文档、私人 filing、凭据、原始日志、个人数据、内部法律/财务意见或
重大非公开信息。示例和测试应使用 synthetic examples 或明确公开的 filing excerpts。

## More Docs

- [Source-only review](docs/source-only-review.md)
- [Development workflow](docs/development-workflow.md)
- [Update workflow](docs/update-workflow.md)
- [Privacy and sanitization](docs/privacy-and-sanitization.md)
- [Release process](docs/release-process.md)
- [Roadmap](ROADMAP.md)

## 更多文档

- [Source-only review](docs/source-only-review.md)
- [Development workflow](docs/development-workflow.md)
- [Update workflow](docs/update-workflow.md)
- [Privacy and sanitization](docs/privacy-and-sanitization.md)
- [Release process](docs/release-process.md)
- [Roadmap](ROADMAP.md)

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## 更新记录

见 [CHANGELOG.md](CHANGELOG.md)。
