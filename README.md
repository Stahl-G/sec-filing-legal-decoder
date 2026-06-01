# SEC Filing Legal Decoder

Legal-to-finance workflows for decoding legal-heavy `10-K`, `20-F`, and annual
report sections.

SEC Filing Legal Decoder is an AI agent skill and CLI for decoding legal-heavy
SEC filing sections into finance-readable risk notes, triage decisions, and
escalation questions. It is especially useful for `10-K`, `10-Q`, `20-F`,
`40-F`, and annual report review workflows.

法律语言到金融理解的工作流，用于解码 `10-K`、`20-F` 等年报文件或是季报文件中法律语言较重的
章节。

SEC Filing Legal Decoder 是一个 AI agent skill 和 CLI，用来把 SEC filing 中
法律语言较重的章节解码为金融读者能理解的风险笔记、阅读分级和升级问题。它尤其
适合 `10-K`、`10-Q`、`20-F`、`40-F` 和年报 review。

It focuses on the non-financial filing language that can change financial
judgment: legal proceedings, regulatory risk, internal control weaknesses,
related-party transactions, debt covenants, guarantees, commitments, dilution,
and material contracts.

它重点处理那些会影响财务判断的非财务法律披露：法律诉讼、监管风险、内控缺陷、
关联交易、债务 covenant、担保、承诺事项、股权稀释和重大合同。

## What This Project Is

- A deterministic v0.1 toolkit for legal-to-finance filing triage.
- A CLI that reads SEC `.htm/.html` Inline XBRL main documents, Markdown, and
  TXT today.
- An optional MinerU adapter for PDF/Office fallback when the source is not an
  EDGAR HTML main filing.
- A generator for legal-to-finance review notes, reading decisions, escalation questions,
  Markdown reports, JSON output, and management memo drafts.
- A model-agnostic workflow layer that can later work with ChatGPT, Claude,
  Codex, OpenCode, local LLMs, or manual review.

## 这个项目是什么

- 一个 deterministic v0.1 工具，用于把 filing 里的法律语言转成 finance reader
  能用的 triage 输出。
- 一个 CLI，目前可以直接读取 SEC `.htm/.html` Inline XBRL 主文件、Markdown 和
  TXT。
- 一个可选 MinerU adapter，只在 PDF/Office 等非 EDGAR HTML 主文件场景下作为
  fallback。
- 一个可以生成 legal-to-finance review notes、reading decisions、escalation questions、
  Markdown report、JSON output 和 management memo draft 的工具。
- 一个 model-agnostic workflow layer，未来可以接 ChatGPT、Claude、Codex、
  OpenCode、本地 LLM 或人工 review。

## What This Project Is Not

- Not legal advice, investment advice, accounting advice, audit advice, or a
  substitute for professional review.
- Not a generic financial statement reader.
- Not a legal chatbot.
- Not a PDF parser and not a MinerU wrapper.
- Not a definitive SEC compliance, disclosure, or accounting conclusion engine.

## 这个项目不是什么

- 不是法律意见、投资意见、会计意见、审计意见，也不能替代专业 review。
- 不是通用财务报表阅读器。
- 不是法律聊天机器人。
- 不是 PDF parser，也不是 MinerU 套壳。
- 不是 SEC 合规、披露或会计结论引擎。

## SEC Filing Source Priority

For standard SEC annual and quarterly reports, the first-choice source should
usually be the EDGAR main `.htm/.html` filing document, not PDF.

For many modern SEC filings, the main document is an HTML/HTM file that embeds
Inline XBRL tags. A file such as `tsla-20251231.htm` is readable in a browser,
but it also contains machine-readable Inline XBRL elements, often using `ix:`
tags. SEC guidance describes Inline XBRL as a way to combine human-readable and
machine-readable reporting in one document. SEC Inline XBRL requirements also
cover information in forms such as `10-K`, `10-Q`, `20-F`, and `40-F`.

Recommended source order:

| Source format | Practical meaning | Best use |
| --- | --- | --- |
| `.htm` / `.html` | Official main filing document, usually Inline XBRL HTML | Human reading, LLM parsing, section splitting, legal language review |
| SEC `.txt` submission package | Raw submission archive containing the main document and exhibits | Archiving and completeness checks; split before analysis |
| `.xml` / XBRL files | Structured financial data files | Databases, quantitative extraction, financial metric extraction |
| `.pdf` | Often an IR website version or an EDGAR exhibit | Human reading or printing; not recommended as the primary agent source |

## SEC filing 源文件优先级

对于标准 SEC 年报和季报，第一选择通常应该是 EDGAR 的主 `.htm/.html` 文件，
不是 PDF。

很多现代 SEC filing 的主文件是 HTML/HTM，但里面嵌了 Inline XBRL 标签。例如
`tsla-20251231.htm` 可以直接用浏览器打开给人读，同时也包含机器可读的 Inline
XBRL 元素，常见标记包括 `ix:`。SEC 对 Inline XBRL 的说明是：它把 human-readable
和 machine-readable reporting 合在同一份文件里。SEC 的 Inline XBRL 要求也覆盖
`10-K`、`10-Q`、`20-F`、`40-F` 等表格中的相关信息。

建议优先级：

| 源文件格式 | 实质 | 最适合用途 |
| --- | --- | --- |
| `.htm` / `.html` | 官方主 filing 文档，通常是 Inline XBRL HTML | 人读、LLM 解析、章节切分、法律语言 review |
| SEC `.txt` submission package | 原始 submission 归档，包含主文档和附件 | 归档和完整性检查；分析前应先拆主文档 |
| `.xml` / XBRL files | 结构化财务数据文件 | 数据库、量化抽取、财务指标抽取 |
| `.pdf` | 通常是 IR 网站展示版或 EDGAR 附件 | 适合人工阅读/打印；不建议作为 agent 主源 |

## Why Not Another Financial Statement Reader

Many readers can handle revenue, margins, cash flow, and debt tables. The
slowdown often comes from legal-heavy filing sections where a finance reader
needs to know whether language is routine boilerplate, finance-relevant, or a
matter for Legal, Finance, Auditors, IR, Management, or the Board.

This project helps answer: should this paragraph be skipped, skimmed, read,
deep-read, or escalated?

## 为什么不是又一个财务报表阅读器

很多读者能看懂收入、毛利率、现金流和债务表格。真正拖慢阅读速度的，往往是
法律语言较重的 filing 章节：finance reader 需要判断一段话到底是普通 boilerplate、
财务相关风险，还是应该升级给 Legal、Finance、Auditor、IR、Management 或 Board。

这个项目帮助回答：这段话应该跳过、略读、正常读、深读，还是升级处理？

## How MinerU Fits

MinerU remains useful for PDF, DOCX, PPTX, XLSX, image, or non-EDGAR document
parsing. It should not be the default path for standard SEC `10-K`, `10-Q`,
`20-F`, or `40-F` main filings when `.htm/.html` is available.

SEC Filing Legal Decoder handles filing workflow intelligence after readable text
exists: section classification, legal-to-finance decoding, boilerplate vs
material triage, escalation question generation, and memo output.

This project can use MinerU as an optional document parsing backend. MinerU is
developed by OpenDataLab/MinerU Team and licensed under the MinerU Open Source
License, based on Apache 2.0 with additional conditions. This project is not
affiliated with OpenDataLab or MinerU. Users are responsible for complying with
MinerU's own license and service terms.

## MinerU 在这里怎么用

MinerU 仍然适合 PDF、DOCX、PPTX、XLSX、图片或非 EDGAR 文档解析。但如果是标准
SEC `10-K`、`10-Q`、`20-F`、`40-F` 主文件，并且已经有 `.htm/.html`，就不应该
默认走 MinerU。

SEC Filing Legal Decoder 处理的是“文本已经可读之后”的 filing workflow intelligence：
章节分类、legal-to-finance 解码、boilerplate vs material triage、升级问题生成和
memo 输出。

本项目可以把 MinerU 作为可选解析后端。MinerU 由 OpenDataLab/MinerU Team 开发，
其许可证是基于 Apache 2.0 并带有额外条件的 MinerU Open Source License。本项目
不隶属于 OpenDataLab 或 MinerU。用户应自行遵守 MinerU 的许可证和服务条款。

## Quick Start For Agent Users

This project is designed to be agent-readable. If you are using Codex, Claude
Code, OpenCode, Cursor, Devin, or another coding agent, give the agent this
repository link and your filing input, then ask it to install the project, read
`README.md` and `AGENTS.md`, run the smoke test, and generate a report.

Suggested prompt:

```text
Please use this project:
https://github.com/Stahl-G/sec-filing-legal-decoder

Clone or open the repository, read README.md and AGENTS.md, install it in a
local virtual environment, run the built-in smoke test, then analyze my SEC
filing main .htm/.html file with sec-filing-legal-decoder. This is especially intended
for 20-F, 10-K, 10-Q, and 40-F legal-heavy sections. Generate a Markdown report,
a JSON structured report, and, if useful, a management memo. Do not treat the
output as legal, investment, accounting, or audit advice.
```

## Agent 用户快速开始

这个项目更适合当作一个 agent skill / agent-readable repository 使用。如果你在用
Codex、Claude Code、OpenCode、Cursor、Devin 或其他 coding agent，可以把仓库链接
和 filing 输入文件交给 agent，让它自己安装、阅读 `README.md` 和 `AGENTS.md`、
运行 smoke test，然后生成报告。

可以直接复制下面这段给你的 agent：

```text
请使用这个项目：
https://github.com/Stahl-G/sec-filing-legal-decoder

请 clone 或打开这个仓库，阅读 README.md 和 AGENTS.md，在本地虚拟环境中安装
项目，先运行内置 smoke test，然后用 sec-filing-legal-decoder 分析我的 SEC filing 主
.htm/.html 文件。这个项目特别适合 20-F、10-K、10-Q、40-F 中法律语言较重的
章节。请输出 Markdown review report、JSON structured report，并在有必要时生成
management memo。不要把输出当作法律、投资、会计或审计意见。
```

## First Smoke Test

Run the built-in synthetic example:

```bash
sec-filing-legal-decoder analyze examples/synthetic_legal_proceedings.md \
  --out outputs/report.md \
  --json outputs/report.json
```

Run the built-in synthetic SEC HTML / Inline XBRL-style example:

```bash
sec-filing-legal-decoder analyze examples/synthetic_sec_inline_xbrl.htm \
  --out outputs/html-report.md \
  --json outputs/html-report.json
```

Expected result:

- A Markdown review report at `outputs/report.md`
- A structured JSON report at `outputs/report.json`
- Reading decisions such as `SKIM`, `DEEP_READ`, or `ESCALATE`
- Legal-to-finance notes and role-specific escalation questions
- A disclaimer reminding you that the output is only a triage aid

## 第一次 smoke test

先跑内置 synthetic example：

```bash
sec-filing-legal-decoder analyze examples/synthetic_legal_proceedings.md \
  --out outputs/report.md \
  --json outputs/report.json
```

再跑内置 synthetic SEC HTML / Inline XBRL-style example：

```bash
sec-filing-legal-decoder analyze examples/synthetic_sec_inline_xbrl.htm \
  --out outputs/html-report.md \
  --json outputs/html-report.json
```

预期结果：

- `outputs/report.md` 里有 Markdown review report
- `outputs/report.json` 里有结构化 JSON report
- 结果包含 `SKIM`、`DEEP_READ`、`ESCALATE` 等 reading decisions
- 结果包含 legal-to-finance notes 和 role-specific escalation questions
- 结果包含 disclaimer，提醒输出只是 triage aid

## Manual Developer Setup

If you are running the project yourself from a terminal:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install .
sec-filing-legal-decoder analyze examples/synthetic_legal_proceedings.md \
  --out outputs/report.md \
  --json outputs/report.json
```

Run tests and evals if you are modifying the code:

```bash
python -m pip install ".[dev]"
pytest
python evals/run_evals.py
```

## 手动开发者安装

如果你自己在 terminal 里运行：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install .
sec-filing-legal-decoder analyze examples/synthetic_legal_proceedings.md \
  --out outputs/report.md \
  --json outputs/report.json
```

如果你修改代码，请跑测试和 eval：

```bash
python -m pip install ".[dev]"
pytest
python evals/run_evals.py
```

## CLI Examples

Analyze an EDGAR main HTML filing:

```bash
sec-filing-legal-decoder analyze tsla-20251231.htm \
  --out outputs/tesla-10k-report.md \
  --json outputs/tesla-10k-report.json
```

Export the same analysis into an Obsidian vault:

```bash
sec-filing-legal-decoder analyze tsla-20251231.htm \
  --out outputs/tesla-10k-report.md \
  --json outputs/tesla-10k-report.json \
  --obsidian-vault ~/Documents/ObsidianVault \
  --obsidian-folder "SEC Filings/TSLA/2025 10-K" \
  --company "Tesla, Inc." \
  --ticker TSLA \
  --form 10-K \
  --year 2025
```

Analyze Markdown or TXT:

```bash
sec-filing-legal-decoder analyze examples/synthetic_legal_proceedings.md \
  --out outputs/report.md \
  --json outputs/report.json
```

Analyze a PDF through MinerU only if you do not have the SEC HTML main file and
the MinerU CLI is installed:

```bash
sec-filing-legal-decoder analyze annual-report.pdf --parser mineru-cli --out outputs/report.md
```

Generate a management memo:

```bash
sec-filing-legal-decoder memo examples/synthetic_internal_control.md --out outputs/memo.md
```

## CLI 示例

分析 EDGAR HTML 主 filing：

```bash
sec-filing-legal-decoder analyze tsla-20251231.htm \
  --out outputs/tesla-10k-report.md \
  --json outputs/tesla-10k-report.json
```

同时导出到 Obsidian vault：

```bash
sec-filing-legal-decoder analyze tsla-20251231.htm \
  --out outputs/tesla-10k-report.md \
  --json outputs/tesla-10k-report.json \
  --obsidian-vault ~/Documents/ObsidianVault \
  --obsidian-folder "SEC Filings/TSLA/2025 10-K" \
  --company "Tesla, Inc." \
  --ticker TSLA \
  --form 10-K \
  --year 2025
```

Obsidian export will create a linked note set:

```text
SEC Filings/TSLA/2025 10-K/
  00 Dashboard.md
  01 Executive Summary.md
  02 Reading Decision Index.md
  03 Escalation Matrix.md
  04 Management Memo.md
  05 Legal-to-Finance Notes.md
  06 Suggested Questions.md
  paragraphs/
    P0001 - legal-proceedings - ESCALATE.md
  data/
    report.json
```

Obsidian export 会生成一组互相链接的 notes：

```text
SEC Filings/TSLA/2025 10-K/
  00 Dashboard.md
  01 Executive Summary.md
  02 Reading Decision Index.md
  03 Escalation Matrix.md
  04 Management Memo.md
  05 Legal-to-Finance Notes.md
  06 Suggested Questions.md
  paragraphs/
    P0001 - legal-proceedings - ESCALATE.md
  data/
    report.json
```

分析 Markdown 或 TXT：

```bash
sec-filing-legal-decoder analyze examples/synthetic_legal_proceedings.md \
  --out outputs/report.md \
  --json outputs/report.json
```

只有在没有 SEC HTML 主文件、且本机已经安装 MinerU CLI 时，才建议用 MinerU 分析 PDF：

```bash
sec-filing-legal-decoder analyze annual-report.pdf --parser mineru-cli --out outputs/report.md
```

生成 management memo：

```bash
sec-filing-legal-decoder memo examples/synthetic_internal_control.md --out outputs/memo.md
```

## Tesla 10-K / 10-K/A Test Plan

Use the official EDGAR `.htm/.html` main documents as the primary inputs. Do
not start from PDF unless HTML is unavailable.

Suggested flow:

1. Put the downloaded Tesla `10-K` and `10-K/A` main `.htm` files into a local
   test folder such as `samples/tesla/`.
2. Run the built-in synthetic smoke test first.
3. Analyze the Tesla `10-K` HTML file and save Markdown plus JSON output.
4. Analyze the Tesla `10-K/A` HTML file with the same output pattern.
5. Compare the top flagged paragraphs, reading decisions, and escalation
   questions between the original filing and the amendment.
6. Manually inspect whether the amendment changes legal-heavy sections, risk
   language, controls, legal proceedings, dilution, commitments, or related
   party language.

Example commands:

```bash
sec-filing-legal-decoder analyze samples/tesla/tsla-10k.htm \
  --out outputs/tesla-10k-report.md \
  --json outputs/tesla-10k-report.json

sec-filing-legal-decoder analyze samples/tesla/tsla-10ka.htm \
  --out outputs/tesla-10ka-report.md \
  --json outputs/tesla-10ka-report.json

sec-filing-legal-decoder analyze samples/tesla/tsla-10k.htm \
  --obsidian-vault ~/Documents/ObsidianVault \
  --obsidian-folder "SEC Filings/TSLA/2025 10-K" \
  --company "Tesla, Inc." \
  --ticker TSLA \
  --form 10-K \
  --year 2025

sec-filing-legal-decoder memo samples/tesla/tsla-10ka.htm \
  --out outputs/tesla-10ka-memo.md
```

## Tesla 10-K / 10-K/A 测试流程

优先使用 EDGAR 官方 `.htm/.html` 主文件作为输入。除非拿不到 HTML，否则不要从
PDF 开始。

建议流程：

1. 把刚下载的 Tesla `10-K` 和 `10-K/A` 主 `.htm` 文件放到本地测试目录，例如
   `samples/tesla/`。
2. 先运行内置 synthetic smoke test，确认工具链可用。
3. 分析 Tesla `10-K` HTML 文件，保存 Markdown 和 JSON 输出。
4. 用同样方式分析 Tesla `10-K/A` HTML 文件。
5. 对比原始 filing 和 amendment 的 top flagged paragraphs、reading decisions
   和 escalation questions。
6. 人工检查 amendment 是否改变了法律语言较重的章节、risk language、controls、
   legal proceedings、dilution、commitments 或 related party language。

示例命令：

```bash
sec-filing-legal-decoder analyze samples/tesla/tsla-10k.htm \
  --out outputs/tesla-10k-report.md \
  --json outputs/tesla-10k-report.json

sec-filing-legal-decoder analyze samples/tesla/tsla-10ka.htm \
  --out outputs/tesla-10ka-report.md \
  --json outputs/tesla-10ka-report.json

sec-filing-legal-decoder analyze samples/tesla/tsla-10k.htm \
  --obsidian-vault ~/Documents/ObsidianVault \
  --obsidian-folder "SEC Filings/TSLA/2025 10-K" \
  --company "Tesla, Inc." \
  --ticker TSLA \
  --form 10-K \
  --year 2025

sec-filing-legal-decoder memo samples/tesla/tsla-10ka.htm \
  --out outputs/tesla-10ka-memo.md
```

## Output Schema

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

## 输出字段

每个被分析的段落都会输出：

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
src/sec_filing_legal_decoder/
  parser_backends/       # HTML, Markdown, TXT, MinerU CLI, mock parser adapters
  classifiers/           # Rule-based section classification and triage
  crosswalk/             # Finance relevance, reading decisions, questions
  reports/               # Markdown, JSON, memo, and Obsidian vault generation
  schemas/               # Dataclass output models
  utils/                 # Text splitting and source references
skills/
  sec-filing-legal-decoder/
    SKILL.md
    skill.json
```

The default path runs without MinerU or an LLM API key.

## 架构

```text
src/sec_filing_legal_decoder/
  parser_backends/       # HTML、Markdown、TXT、MinerU CLI、mock parser adapters
  classifiers/           # 规则分类和 triage
  crosswalk/             # Finance relevance、reading decisions、questions
  reports/               # Markdown、JSON、memo、Obsidian vault 生成
  schemas/               # Dataclass output models
  utils/                 # 文本切分和 source references
skills/
  sec-filing-legal-decoder/
    SKILL.md
    skill.json
```

默认路径不需要 MinerU，也不需要 LLM API key。

## Safety And Confidentiality

- Do not include confidential company documents.
- Do not include material non-public information, raw logs, credentials, or
  personal data.
- Use synthetic examples or public filing excerpts.
- Treat all outputs as reading aids requiring professional review.

## 安全和保密

- 不要放入公司机密文件。
- 不要放入重大非公开信息、原始日志、凭证或个人数据。
- 使用 synthetic examples 或公开 filing excerpts。
- 所有输出都只是 reading aid，需要专业 review。

## Roadmap

v0.1:

- Rule-based legal-heavy paragraph classification
- Legal-to-finance note generation
- Escalation questions
- Markdown/JSON reports
- EDGAR HTML / Inline XBRL main document input
- Optional MinerU CLI fallback for PDF/Office

v0.2:

- Prior-year wording diff reviewer
- SEC `20-F` / `10-K` / `10-Q` / `40-F` section mapper
- EDGAR `.txt` submission package splitter
- Better source citation and page/section references
- Optional LLM adapter

v0.3:

- Finance-to-legal decoder
- Governance-to-investor decoder
- Board / management briefing packs
- DOCX report export
- CI-based redaction checks

## 路线图

v0.1:

- 规则化法律段落分类
- Legal-to-finance note generation
- Escalation questions
- Markdown/JSON reports
- EDGAR HTML / Inline XBRL 主文件输入
- PDF/Office 场景下的可选 MinerU CLI fallback

v0.2:

- 去年 wording diff reviewer
- SEC `20-F` / `10-K` / `10-Q` / `40-F` section mapper
- EDGAR `.txt` submission package splitter
- 更好的 source citation 和 page/section references
- 可选 LLM adapter

v0.3:

- Finance-to-legal decoder
- Governance-to-investor decoder
- Board / management briefing packs
- DOCX report export
- CI-based redaction checks

## References

- SEC Inline XBRL overview: <https://www.sec.gov/data-research/structured-data/inline-xbrl>
- SEC EDGAR Filer Manual, Volume II, Chapter 5: <https://www.sec.gov/files/edgar/filermanual/efmvol2-c5.pdf>

## 参考资料

- SEC Inline XBRL overview: <https://www.sec.gov/data-research/structured-data/inline-xbrl>
- SEC EDGAR Filer Manual, Volume II, Chapter 5: <https://www.sec.gov/files/edgar/filermanual/efmvol2-c5.pdf>

## Disclaimer

This project is not legal advice, investment advice, accounting advice, audit
advice, or a substitute for qualified professional review. It is designed to
help readers classify, simplify, and triage legal-heavy filing language and
generate better escalation questions. Users should consult qualified legal,
accounting, audit, or investment professionals before relying on any output.

## 免责声明

本项目不是法律意见、投资意见、会计意见、审计意见，也不能替代合格专业人士的
review。本项目只用于帮助读者分类、简化和 triage 法律语言较重的 filing 内容，
并生成更好的升级问题。用户在依赖任何输出之前，应咨询合格的法律、会计、审计或
投资专业人士。
