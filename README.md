# SEC Filing Legal Decoder

Legal Risk Cards for Finance Readers: legal-to-finance workflows for decoding
legal-heavy `10-K`, `10-Q`, `20-F`, `40-F`, and annual report sections.

SEC Filing Legal Decoder is an AI agent skill and CLI for decoding legal-heavy
SEC filing sections into finance-readable risk cards, triage decisions,
escalation questions, and management follow-up notes. It is especially useful
for `10-K`, `10-Q`, `20-F`, `40-F`, and annual report review workflows.

面向金融读者的法律风险卡工具：把 `10-K`、`10-Q`、`20-F`、`40-F` 和年报/季报中
法律语言较重的章节，转成 legal-to-finance 工作流输出。

SEC Filing Legal Decoder 是一个 AI agent skill 和 CLI，用来把 SEC filing 中
法律语言较重的章节解码为金融读者能理解的风险卡、阅读分级、升级问题和管理层
跟进事项。它尤其适合 `10-K`、`10-Q`、`20-F`、`40-F` 和年报 review。

It focuses on the non-financial filing language that can change financial
judgment: legal proceedings, regulatory risk, internal control weaknesses,
related-party transactions, debt covenants, guarantees, commitments, dilution,
and material contracts.

它重点处理那些会影响财务判断的非财务法律披露：法律诉讼、监管风险、内控缺陷、
关联交易、债务 covenant、担保、承诺事项、股权稀释和重大合同。

## What This Project Is

- A deterministic v0.3.0 toolkit for legal-to-finance filing triage.
- A risk-card generator that groups source paragraphs into issue-level legal,
  regulatory, governance, audit, disclosure, debt, related-party, dilution, tax,
  cybersecurity, and material-contract cards, then consolidates overlapping
  cards into a sharper read-first review.
- A CLI that reads SEC `.htm/.html` Inline XBRL main documents, Markdown, and
  TXT today.
- An optional MinerU adapter for PDF/Office fallback when the source is not an
  EDGAR HTML main filing.
- A generator for legal-to-finance review notes, reading decisions, escalation questions,
  Obsidian-friendly Markdown reports, JSON output, risk-card notes, and management
  memo drafts.
- A model-agnostic workflow layer that can later work with ChatGPT, Claude,
  Codex, OpenCode, local LLMs, or manual review.

## 这个项目是什么

- 一个 deterministic v0.3.0 工具，用于把 filing 里的法律语言转成 finance reader
  能用的 triage 输出。
- 一个 risk-card generator，可以把 source paragraphs 聚合成事项级 legal、
  regulatory、governance、audit、disclosure、debt、related-party、dilution、
  tax、cybersecurity 和 material-contract cards，并把重叠卡片合并成更清晰的
  read-first review。
- 一个 CLI，目前可以直接读取 SEC `.htm/.html` Inline XBRL 主文件、Markdown 和
  TXT。
- 一个可选 MinerU adapter，只在 PDF/Office 等非 EDGAR HTML 主文件场景下作为
  fallback。
- 一个可以生成 legal-to-finance review notes、reading decisions、escalation questions、
  Obsidian-friendly Markdown report、JSON output、risk-card notes 和 management memo
  draft 的工具。
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

In v0.3.0, the preferred output is no longer a long paragraph-by-paragraph
report. The preferred output is a small set of issue-level legal risk cards.
Each card explains what the filing language may mean, why a finance reader
should care, which owners should review it, what questions to ask, what not to
overstate, how the legal-risk read differs from ordinary financial analysis,
and which source excerpts support the card.

The first-read file is now `legal-risk-review.md`, an integrated narrative
review synthesized from the evidence-filtered cards. `legal-risk-cards.md`
remains available as the card appendix.

## 为什么不是又一个财务报表阅读器

很多读者能看懂收入、毛利率、现金流和债务表格。真正拖慢阅读速度的，往往是
法律语言较重的 filing 章节：finance reader 需要判断一段话到底是普通 boilerplate、
财务相关风险，还是应该升级给 Legal、Finance、Auditor、IR、Management 或 Board。

这个项目帮助回答：这段话应该跳过、略读、正常读、深读，还是升级处理？

在 v0.3.0 中，首选输出不再是很长的逐段报告，而是一组事项级 legal risk cards。
每张卡会解释 filing 语言可能意味着什么、为什么金融读者需要关心、应该找哪些 owner
review、该问什么问题、哪些结论不能过度表述、这和普通财务分析有什么不同，以及
支撑这张卡的 source excerpts。

现在第一阅读入口是 `legal-risk-review.md`，它会基于 evidence-filtered cards 生成一份
连续叙事的 integrated review。`legal-risk-cards.md` 仍作为 card appendix 保留。

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

## Do I Need MinerU?

Usually no.

For SEC `10-K`, `10-Q`, `20-F`, and `40-F` filings, use the official EDGAR
`.htm` / `.html` main filing whenever available.

MinerU is only an optional fallback for PDF, Office, image, or non-EDGAR
documents.

## 我需要 MinerU 吗？

通常不需要。

如果分析的是 SEC `10-K`、`10-Q`、`20-F`、`40-F`，优先使用 EDGAR 官方
`.htm` / `.html` 主 filing 文件。

MinerU 只是可选 fallback，适合 PDF、Office、图片或非 EDGAR 文档。

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

## Installation Guide For Beginners

If you are new to Python CLI tools, install only the required tools first.
MinerU and Obsidian are optional.

### 1. Required Tools

You need:

- Python 3.10 or later
- Git
- A terminal:
  - macOS: Terminal or iTerm2
  - Windows: PowerShell, Windows Terminal, or Git Bash
  - Linux: your default terminal

Check your Python version:

```bash
python --version
```

If that does not work, try:

```bash
python3 --version
```

This project requires Python 3.10 or later.

Check Git:

```bash
git --version
```

### 2. Clone The Repository

```bash
git clone https://github.com/Stahl-G/sec-filing-legal-decoder.git
cd sec-filing-legal-decoder
```

### 3. Create A Virtual Environment

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 4. Install The Project

```bash
python -m pip install .
```

For development or testing:

```bash
python -m pip install ".[dev]"
```

### 5. Run The Smoke Test

```bash
sec-filing-legal-decoder analyze examples/synthetic_legal_proceedings.md \
  --out outputs/report.md \
  --json outputs/report.json
```

Expected outputs:

- `outputs/report.md`
- `outputs/report.json`

If this works, your local installation is ready.

### 6. Optional: Install Obsidian

Obsidian is optional. The normal `--out report.md` file is already
Obsidian-friendly Markdown with YAML properties, tags, tables, and callouts.
You only need the Obsidian app if you want to open the generated notes as a
local knowledge base.

After installing Obsidian, create or choose a vault folder. Then run:

```bash
sec-filing-legal-decoder analyze examples/synthetic_sec_inline_xbrl.htm \
  --out outputs/html-report.md \
  --json outputs/html-report.json \
  --obsidian-vault ~/Documents/ObsidianVault \
  --obsidian-folder "SEC Filings/Sample/2025 10-K" \
  --company "Sample Company" \
  --ticker SAMPLE \
  --form 10-K \
  --year 2025
```

Replace `~/Documents/ObsidianVault` with your own Obsidian vault path.

### 7. Optional: Install MinerU

MinerU is optional. You do not need MinerU for standard SEC `.htm` / `.html`
main filing files.

Use MinerU only when you need to parse PDF, DOCX, PPTX, XLSX, images, or other
non-EDGAR HTML documents.

If MinerU is not installed, you can still use this project with:

- SEC `.htm` / `.html` main filing files
- Markdown files
- TXT files

### 8. Recommended Source Format

For SEC filings, prefer the official EDGAR main filing document:

1. `.htm` / `.html` main filing file: recommended
2. `.txt` SEC submission package: useful for archiving and completeness checks
3. `.pdf`: only use when HTML is unavailable or the document is not a standard
   EDGAR filing

### 9. Troubleshooting

If the command is not found:

```bash
sec-filing-legal-decoder --help
```

does not work, try reinstalling inside your activated virtual environment:

```bash
python -m pip install .
```

If your virtual environment is not active, activate it again.

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If you see a Python version error, install Python 3.10 or later.

### 10. Safety Reminder

Do not upload or commit confidential company documents, material non-public
information, credentials, raw logs, personal data, or internal legal/finance
advice.

This project is a filing-reading and triage aid. It is not legal advice,
investment advice, accounting advice, audit advice, or a substitute for
qualified professional review.

## 新手安装指南

如果你第一次使用 Python CLI 工具，先安装必需工具即可。MinerU 和 Obsidian 都是
可选项。

### 1. 必需工具

你需要：

- Python 3.10 或更高版本
- Git
- 一个 terminal：
  - macOS: Terminal 或 iTerm2
  - Windows: PowerShell、Windows Terminal 或 Git Bash
  - Linux: 默认 terminal

检查 Python 版本：

```bash
python --version
```

如果不工作，试试：

```bash
python3 --version
```

本项目要求 Python 3.10 或更高版本。

检查 Git：

```bash
git --version
```

### 2. Clone 仓库

```bash
git clone https://github.com/Stahl-G/sec-filing-legal-decoder.git
cd sec-filing-legal-decoder
```

### 3. 创建虚拟环境

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 4. 安装项目

```bash
python -m pip install .
```

如果你要开发或跑测试：

```bash
python -m pip install ".[dev]"
```

### 5. 运行 smoke test

```bash
sec-filing-legal-decoder analyze examples/synthetic_legal_proceedings.md \
  --out outputs/report.md \
  --json outputs/report.json
```

预期输出：

- `outputs/report.md`
- `outputs/report.json`

如果这一步成功，本地安装就已经可用。

### 6. 可选：安装 Obsidian

Obsidian 是可选的。普通 `--out report.md` 已经是 Obsidian-friendly Markdown，
包含 YAML properties、tags、tables 和 callouts。只有当你想把生成结果作为本地
知识库阅读时，才需要安装 Obsidian。

安装 Obsidian 后，创建或选择一个 vault 文件夹，然后运行：

```bash
sec-filing-legal-decoder analyze examples/synthetic_sec_inline_xbrl.htm \
  --out outputs/html-report.md \
  --json outputs/html-report.json \
  --obsidian-vault ~/Documents/ObsidianVault \
  --obsidian-folder "SEC Filings/Sample/2025 10-K" \
  --company "Sample Company" \
  --ticker SAMPLE \
  --form 10-K \
  --year 2025
```

把 `~/Documents/ObsidianVault` 替换成你自己的 Obsidian vault 路径。

### 7. 可选：安装 MinerU

MinerU 是可选的。标准 SEC `.htm` / `.html` 主 filing 文件不需要 MinerU。

只有在需要解析 PDF、DOCX、PPTX、XLSX、图片或其他非 EDGAR HTML 文档时，才使用
MinerU。

即使没有安装 MinerU，本项目仍然可以分析：

- SEC `.htm` / `.html` 主 filing 文件
- Markdown 文件
- TXT 文件

### 8. 推荐源文件格式

分析 SEC filing 时，优先使用 EDGAR 官方主 filing 文件：

1. `.htm` / `.html` 主 filing 文件：推荐
2. SEC `.txt` submission package：适合归档和完整性检查
3. `.pdf`：只有在没有 HTML，或文档不是标准 EDGAR filing 时再用

### 9. 常见问题

如果命令不存在：

```bash
sec-filing-legal-decoder --help
```

无法运行，请在已激活的虚拟环境中重新安装：

```bash
python -m pip install .
```

如果虚拟环境没有激活，请重新激活。

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

如果遇到 Python 版本错误，请安装 Python 3.10 或更高版本。

### 10. 安全提醒

不要上传或提交公司机密文件、重大非公开信息、凭证、原始日志、个人数据或内部
法律/财务意见。

本项目只是 filing 阅读和 triage aid。它不是法律意见、投资意见、会计意见、审计
意见，也不能替代合格专业人士 review。

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

- An Obsidian-friendly Markdown review report at `outputs/report.md`
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

- `outputs/report.md` 里有 Obsidian-friendly Markdown review report
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

Generate v0.3.0 legal risk review and risk cards. This is the preferred command for agent
workflows:

```bash
sec-filing-legal-decoder risk-cards tsla-20251231.htm \
  --output-dir outputs/tesla-10k-risk-cards \
  --obsidian-dir ~/Documents/ObsidianVault/SEC\ Filings/TSLA/2025\ 10-K \
  --company "Tesla, Inc." \
  --ticker TSLA \
  --form 10-K \
  --year 2025
```

The output directory contains:

```text
legal-risk-cards.md
legal-risk-cards.json
legal-risk-review.md
evidence-audit.md
escalation-questions.md
management-follow-up.md
```

Chinese bilingual output keeps source excerpts in the original English filing
language while writing explanations, cautions, and review guidance in Chinese
with key filing/legal terms preserved:

```bash
sec-filing-legal-decoder risk-cards tsla-20251231.htm \
  --output-dir outputs/tesla-10k-risk-cards-zh \
  --lang zh-CN \
  --term-style bilingual
```

Language options:

- `--lang en` keeps the default English reports.
- `--lang zh-CN --term-style bilingual` writes Chinese explanations with key
  English terms such as `Legal Proceedings`, `valuation allowance`, and
  `reasonably possible` preserved.
- `--term-style english`, `--term-style bilingual`, and `--term-style translated`
  control how domain titles are displayed in non-English reports.

Compare an existing finance or earnings analysis against the filing risk cards:

```bash
sec-filing-legal-decoder review-overlay tsla-20251231.htm \
  --analysis outputs/tesla-earnings-analysis.md \
  --output-dir outputs/tesla-review-overlay
```

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

生成 v0.3.0 legal risk review 和 risk cards。Agent workflow 推荐优先使用这个命令：

```bash
sec-filing-legal-decoder risk-cards tsla-20251231.htm \
  --output-dir outputs/tesla-10k-risk-cards \
  --obsidian-dir ~/Documents/ObsidianVault/SEC\ Filings/TSLA/2025\ 10-K \
  --company "Tesla, Inc." \
  --ticker TSLA \
  --form 10-K \
  --year 2025
```

输出目录会包含：

```text
legal-risk-cards.md
legal-risk-cards.json
legal-risk-review.md
evidence-audit.md
escalation-questions.md
management-follow-up.md
```

中文双语输出会保留 filing 原文摘录的英文，同时把解释、谨慎表述和 review guidance
写成中文，并保留关键英文法律/披露术语：

```bash
sec-filing-legal-decoder risk-cards tsla-20251231.htm \
  --output-dir outputs/tesla-10k-risk-cards-zh \
  --lang zh-CN \
  --term-style bilingual
```

语言选项：

- `--lang en` 保持默认英文报告。
- `--lang zh-CN --term-style bilingual` 输出中文解释，并保留 `Legal Proceedings`、
  `valuation allowance`、`reasonably possible` 等关键英文术语。
- `--term-style english`、`--term-style bilingual`、`--term-style translated`
  控制非英文报告里的 domain title 展示方式。

把已有 finance / earnings analysis 和 filing risk cards 做 overlay review：

```bash
sec-filing-legal-decoder review-overlay tsla-20251231.htm \
  --analysis outputs/tesla-earnings-analysis.md \
  --output-dir outputs/tesla-review-overlay
```

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

Obsidian export will create a linked note set. Only priority paragraphs
(`DEEP_READ` and `ESCALATE`) are split into atomic paragraph notes by default,
so a large 10-K does not flood your vault with low-value notes.

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

Obsidian export 会生成一组互相链接的 notes。默认只把 priority paragraphs
（`DEEP_READ` 和 `ESCALATE`）拆成 atomic paragraph notes，避免大型 10-K 把 vault
刷满低价值段落。

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

The v0.3.0 `risk-cards` JSON output contains:

- `document`
- `coverage_summary`
- `risk_cards`
- `escalation_matrix`
- `management_follow_up`
- `disclosure_consistency_questions`
- `disclaimer`

Each risk card contains:

- `card_id`
- `title`
- `risk_domain`
- `subdomains`
- `priority`
- `reading_decision`
- `owners`
- `source_paragraphs`
- `plain_language_meaning`
- `why_finance_readers_should_care`
- `legal_or_audit_relevance`
- `financial_statement_linkage`
- `disclosure_ir_relevance`
- `boilerplate_or_material`
- `questions`
- `suggested_management_follow_up`
- `what_not_to_overstate`
- `source_excerpts`
- `issuer_specific_facts`
- `issuer_specific_interpretation`
- `finance_reader_implication`
- `financial_analysis_difference`
- `evidence_quality`
- `evidence_summary`
- `weak_or_suppressed_sources`
- `recommended_review_posture`
- `confidence`

The legacy `analyze` command still produces paragraph-level output.

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

v0.3.0 `risk-cards` JSON 输出包含：

- `document`
- `coverage_summary`
- `risk_cards`
- `escalation_matrix`
- `management_follow_up`
- `disclosure_consistency_questions`
- `disclaimer`

每张 risk card 包含：

- `card_id`
- `title`
- `risk_domain`
- `subdomains`
- `priority`
- `reading_decision`
- `owners`
- `source_paragraphs`
- `plain_language_meaning`
- `why_finance_readers_should_care`
- `legal_or_audit_relevance`
- `financial_statement_linkage`
- `disclosure_ir_relevance`
- `boilerplate_or_material`
- `questions`
- `suggested_management_follow_up`
- `what_not_to_overstate`
- `source_excerpts`
- `issuer_specific_facts`
- `issuer_specific_interpretation`
- `finance_reader_implication`
- `financial_analysis_difference`
- `evidence_quality`
- `evidence_summary`
- `weak_or_suppressed_sources`
- `recommended_review_posture`
- `confidence`

旧版 `analyze` command 仍然生成 paragraph-level output。

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
  document_modes/        # 10-K, 10-Q, 20-F, 40-F, 6-K, earnings-release detection
  content_routing/       # skip / route-out / analyze paragraph routing
  evidence/              # evidence filtering, scoring, and fact extraction
  risk_cards/            # v0.3 risk-domain classification, consolidation, and card generation
  overlay/               # compare existing analysis against filing risk cards
  obsidian/              # v0.3 risk-card Obsidian export
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
  document_modes/        # 10-K、10-Q、20-F、40-F、6-K、earnings-release 检测
  content_routing/       # skip / route-out / analyze 段落路由
  evidence/              # evidence filtering、scoring 和 fact extraction
  risk_cards/            # v0.3 risk-domain 分类、合并和 card generation
  overlay/               # 把已有 analysis 和 filing risk cards 做对照
  obsidian/              # v0.3 risk-card Obsidian export
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

## Known Issues In v0.3.0

- Long annual reports can still route many paragraphs into the risk candidate
  pool. v0.3.0 now consolidates common duplicate cards such as guarantee-vs-debt,
  warrant-vs-guarantee, litigation-vs-disclosure, and weak governance overlaps,
  but future versions should add better section-aware clustering.
- Some issuer-specific facts are extracted by deterministic sentence heuristics.
  They improve the read-through report but still require professional review.
- Chinese `zh-CN` output is intentionally bilingual guidance, not a full legal
  translation of every generated English field. Source excerpts remain in the
  original filing language.
- Earnings-release `6-K` routing is improved for ordinary revenue, shipment,
  margin, expense, and guidance KPI text, but disclosure/guidance boundaries may
  still need issuer-specific tuning.
- Risk priority is deterministic and rule-based. `Critical`, `High`, and
  `Medium` are triage priorities, not legal, accounting, audit, or investment
  conclusions.
- HTML extraction preserves visible text but does not yet reconstruct original
  EDGAR section hierarchy, tables, or page locations with full fidelity.

## v0.3.0 已知问题

- 很长的年报仍可能把较多段落 route 到 risk candidate pool。v0.3.0 已经会合并常见
  重复卡片，例如 guarantee-vs-debt、warrant-vs-guarantee、litigation-vs-disclosure
  和弱 governance overlap，但后续版本仍需要更强的 section-aware clustering。
- issuer-specific facts 目前由 deterministic sentence heuristics 抽取。它能改善
  read-through report，但仍需要专业 review。
- 中文 `zh-CN` 输出是有意设计的 bilingual guidance，不是把每个英文生成字段逐句法律
  翻译。Source excerpts 会保留 filing 原文语言。
- earnings-release `6-K` 对普通 revenue、shipment、margin、expense 和 guidance KPI
  的路由已经改进，但 disclosure/guidance 边界后续仍可能需要按发行人微调。
- 风险优先级是 deterministic rule-based triage。`Critical`、`High`、`Medium` 是阅读
  和跟进优先级，不是法律、会计、审计或投资结论。
- HTML extraction 会保留可见文本，但还不能完整还原 EDGAR 原始 section hierarchy、
  tables 或 page locations。

## Roadmap

v0.3.0:

- Added sharper read-first card consolidation for NVIDIA-style annual reports
- Suppressed duplicate debt/liquidity cards when partner lease guarantees already support a stronger guarantees card
- Suppressed warrant-only equity cards when warrants are only consideration inside a guarantee arrangement
- Suppressed disclosure/IR and weak governance cards when they duplicate legal proceedings, cybersecurity governance, or ordinary board/buyback language
- Added `financial_analysis_difference` to every risk card so each card opens with how the legal-risk read differs from ordinary financial analysis
- Sharpened tax review language around deferred tax assets, valuation allowance, more-likely-than-not support, jurisdictional taxable income, and one-time release risk
- Added `--lang zh-CN` and `--term-style english|bilingual|translated` for Chinese bilingual Markdown output

v0.2.1:

- Added `legal-risk-review.md` as the first-read integrated legal risk review
- Added evidence filtering and evidence quality scoring before report synthesis
- Added issuer-specific facts, issuer-specific interpretation, finance-reader implication, evidence summary, and review posture to each risk card
- Added `evidence-audit.md` for debugging accepted and suppressed source excerpts
- Reduced NVIDIA-style false positives from taxonomy definitions, `warranty` vs `warrant`, `non-affiliates`, and generic settlement/liquidity phrases
- Obsidian risk-card export now starts with `00 Legal Risk Review.md`

v0.2.0:

- Legal Risk Cards for Finance Readers
- `risk-cards` CLI command for issue-level cards instead of paragraph-by-paragraph noise
- Document mode detection for `10-K`, `10-Q`, `20-F`, `40-F`, `6-K`, and earnings-release `6-K`
- Paragraph routing for filing admin, ordinary KPI finance text, business updates, and legal-risk candidates
- Two-level risk-domain taxonomy covering going concern, ICFR, litigation, trade policy, related parties, debt/liquidity, commitments, dilution, tax, governance, disclosure, cybersecurity, and material contracts
- `review-overlay` CLI command for checking existing finance analysis against filing legal-risk cards
- v0.2 Obsidian export centered on risk-card notes
- False-positive fixes for date `May`, amount-only materiality, generic `has/is/was/were`, and ordinary guidance KPI paragraphs

v0.1.1:

- Obsidian-friendly default Markdown report output
- Obsidian vault export with YAML properties, tags, wikilinks, and official callouts
- Priority-only atomic paragraph notes for `DEEP_READ` and `ESCALATE`

v0.1:

- Rule-based legal-heavy paragraph classification
- Legal-to-finance note generation
- Escalation questions
- Markdown/JSON reports
- EDGAR HTML / Inline XBRL main document input
- Optional MinerU CLI fallback for PDF/Office

v0.3.x:

- Prior-year wording diff reviewer
- SEC `20-F` / `10-K` / `10-Q` / `40-F` section mapper
- EDGAR `.txt` submission package splitter
- Better source citation and page/section references
- Optional LLM adapter

v0.4:

- Finance-to-legal decoder
- Governance-to-investor decoder
- Board / management briefing packs
- DOCX report export
- CI-based redaction checks

## 路线图

v0.3.0:

- 针对 NVIDIA 这类长年报，新增更清晰的 read-first card consolidation
- 当 partner lease guarantee 已经支持更强的 guarantees card 时，压掉重复的 debt/liquidity card
- 当 warrants 只是 guarantee arrangement 的对价时，压掉 warrant-only equity card
- 当 disclosure/IR 或弱 governance card 只是重复 legal proceedings、cybersecurity governance 或普通 board/buyback language 时，压到主线之外
- 每张 risk card 新增 `financial_analysis_difference`，开头说明这张卡和普通财务分析的差异
- 强化 tax card，对 deferred tax assets、valuation allowance、more-likely-than-not support、jurisdictional taxable income 和 one-time release risk 做更明确的核查提示
- 新增 `--lang zh-CN` 和 `--term-style english|bilingual|translated`，支持中文双语 Markdown 输出

v0.2.1:

- 新增 `legal-risk-review.md`，作为第一阅读入口的 integrated legal risk review
- 在 report synthesis 前新增 evidence filtering 和 evidence quality scoring
- 每张 risk card 新增 issuer-specific facts、issuer-specific interpretation、finance-reader implication、evidence summary 和 review posture
- 新增 `evidence-audit.md`，用于调试 accepted / suppressed source excerpts
- 降低 NVIDIA 样本暴露出的 taxonomy definitions、`warranty` vs `warrant`、`non-affiliates`、generic settlement/liquidity phrases 等误报
- Obsidian risk-card export 现在以 `00 Legal Risk Review.md` 开始

v0.2.0:

- 面向金融读者的 Legal Risk Cards
- 新增 `risk-cards` CLI command，用事项级 cards 替代逐段噪音
- 支持 `10-K`、`10-Q`、`20-F`、`40-F`、`6-K` 和 earnings-release `6-K` 的 document mode detection
- 新增 paragraph routing，区分 filing admin、普通财务 KPI、业务更新和 legal-risk candidates
- 两层 risk-domain taxonomy，覆盖 going concern、ICFR、litigation、trade policy、related party、debt/liquidity、commitments、dilution、tax、governance、disclosure、cybersecurity 和 material contracts
- 新增 `review-overlay` CLI command，用于把已有 finance analysis 和 filing legal-risk cards 对照
- v0.2 Obsidian export 以 risk-card notes 为中心
- 修复 date `May`、amount-only materiality、generic `has/is/was/were` 和普通 guidance KPI paragraphs 的误报

v0.1.1:

- 默认输出 Obsidian-friendly Markdown report
- Obsidian vault export，包含 YAML properties、tags、wikilinks 和官方 callouts
- 只为 `DEEP_READ` 和 `ESCALATE` 生成 priority atomic paragraph notes

v0.1:

- 规则化法律段落分类
- Legal-to-finance note generation
- Escalation questions
- Markdown/JSON reports
- EDGAR HTML / Inline XBRL 主文件输入
- PDF/Office 场景下的可选 MinerU CLI fallback

v0.3.x:

- 去年 wording diff reviewer
- SEC `20-F` / `10-K` / `10-Q` / `40-F` section mapper
- EDGAR `.txt` submission package splitter
- 更好的 source citation 和 page/section references
- 可选 LLM adapter

v0.4:

- Finance-to-legal decoder
- Governance-to-investor decoder
- Board / management briefing packs
- DOCX report export
- CI-based redaction checks

## References

- SEC Inline XBRL overview: <https://www.sec.gov/data-research/structured-data/inline-xbrl>
- SEC EDGAR Filer Manual, Volume II, Chapter 5: <https://www.sec.gov/files/edgar/filermanual/efmvol2-c5.pdf>
- Obsidian Properties: <https://obsidian.md/help/properties>
- Obsidian Internal links: <https://obsidian.md/help/links>
- Obsidian Callouts: <https://obsidian.md/help/callouts>

## 参考资料

- SEC Inline XBRL overview: <https://www.sec.gov/data-research/structured-data/inline-xbrl>
- SEC EDGAR Filer Manual, Volume II, Chapter 5: <https://www.sec.gov/files/edgar/filermanual/efmvol2-c5.pdf>
- Obsidian Properties: <https://obsidian.md/help/properties>
- Obsidian Internal links: <https://obsidian.md/help/links>
- Obsidian Callouts: <https://obsidian.md/help/callouts>

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
