"""Chinese bilingual Markdown rendering for risk-card reports."""

from __future__ import annotations

from collections import defaultdict

from sec_filing_legal_decoder.schemas import RiskCard, RiskCardReport


TERM_STYLES = {"english", "bilingual", "translated"}

DOMAIN_TERMS: dict[str, tuple[str, str]] = {
    "audit_going_concern": ("持续经营 / 重大疑虑", "Going Concern / Substantial Doubt"),
    "internal_control_reporting": ("内部控制 / SOX / ICFR", "Internal Control / SOX / ICFR"),
    "legal_proceedings_litigation": ("诉讼及法律程序", "Legal Proceedings / Litigation"),
    "regulatory_trade_policy": ("监管 / 贸易政策", "Regulatory / Trade Policy"),
    "related_party_governance": ("关联方交易 / 治理", "Related Party Transactions / Governance"),
    "debt_liquidity_covenant": ("债务 / 流动性 / 契约", "Debt / Liquidity / Covenant"),
    "guarantees_commitments": ("担保 / 承诺 / 约束性订单", "Guarantees / Commitments / Binding Backlog"),
    "equity_dilution_control": ("认股权证 / 可转换工具 / 稀释", "Earnout / Warrants / Convertible Notes / Dilution"),
    "tax_cross_border": ("税务 / 跨境结构", "Tax / Cross-Border Structure"),
    "management_board_governance": ("管理层 / 董事会治理", "Management / Board Governance"),
    "disclosure_ir_consistency": ("披露 / IR 口径一致性", "Disclosure / IR Consistency"),
    "cybersecurity_governance": ("网络安全治理", "Cybersecurity Governance"),
    "material_contracts": ("重大合同 / 商业依赖", "Material Contracts / Commercial Dependencies"),
}

OWNER_LABELS = {
    "Legal": "Legal / 法务",
    "Finance": "Finance / 财务",
    "Auditor": "Auditor / 审计师",
    "IR": "IR / 投资者关系",
    "Management": "Management / 管理层",
    "Board": "Board / 董事会",
}

DOMAIN_READS = {
    "legal_proceedings_litigation": (
        "这张卡不判断公司是否已经违法，也不直接判断赔付金额。它把诉讼阶段、probable / reasonably possible / remote、accrual、range of loss 和披露阈值拆成需要核查的问题。"
    ),
    "material_contracts": (
        "这张卡关注合同权利义务、终止权、IP / license、goodwill、intangible asset 和 useful life。它不是普通收入预测，也不能直接推断合同已经保证未来收入。"
    ),
    "guarantees_commitments": (
        "这张卡关注 guarantee、commitment、off-balance-sheet exposure、partner default、escrow 和 warrant consideration。它不等同于普通 debt schedule，也不宜直接推断为即期现金流出。"
    ),
    "tax_cross_border": (
        "这张卡关注 deferred tax assets、valuation allowance、more-likely-than-not、uncertain tax position 和 jurisdictional taxable income。ETR 变化只是入口，关键是税务假设是否可持续。"
    ),
    "cybersecurity_governance": (
        "这张卡关注 cybersecurity governance、incident response、materiality assessment 和 board oversight。除非原文说明发生 material incident，否则不能据此认定已经发生重大网络事件。"
    ),
    "internal_control_reporting": (
        "这张卡关注 ICFR / disclosure controls 的可靠性、remediation evidence 和审计结论，不是简单解释利润表或现金流趋势。"
    ),
    "regulatory_trade_policy": (
        "这张卡关注监管规则、market access、tariffs、sanctions、export controls 或 compliance evidence 对财务假设的影响。模型结果需要和监管状态一起核查。"
    ),
    "related_party_governance": (
        "这张卡关注 related-party policy、approval path、arm's-length pricing、collectability 和 disclosure completeness。不能仅按普通收入或采购交易阅读。"
    ),
    "equity_dilution_control": (
        "这张卡关注 instrument terms、exercise / conversion triggers、fair value、registration rights 和 dilution。它不是只看当前 shares outstanding。"
    ),
    "debt_liquidity_covenant": (
        "这张卡关注 covenant definitions、default、waiver、maturity classification 和 acceleration rights。不能只看现金余额或流动性指标。"
    ),
    "management_board_governance": (
        "这张卡关注 governance process、committee oversight、independence 和 transition controls。普通资本配置动作本身不应自动被读成法律风险。"
    ),
    "disclosure_ir_consistency": (
        "这张卡关注 management / IR wording 是否保留 filing 的 uncertainty。模型结论不能把原文的 conditional language 改写成确定结论。"
    ),
}

CAUTION_BY_DOMAIN = {
    "legal_proceedings_litigation": "不能据此认定公司已经违法、一定败诉或一定赔偿；应核查程序阶段、会计计提和披露口径。",
    "material_contracts": "不宜直接推断重大合同保证未来收入；应核查 termination、performance obligations、accounting treatment 和 concentration risk。",
    "guarantees_commitments": "不能把 maximum exposure 直接当成预期损失；应区分 gross exposure、mitigation、fair value 和实际现金流风险。",
    "tax_cross_border": "不宜把 valuation allowance release 直接视为可持续收益；应核查 DTA realizability、jurisdictional projections 和 one-time / recurring 性质。",
    "cybersecurity_governance": "不能据此认定已经发生 material cyber incident；应核查事件事实、materiality assessment、board reporting 和 response controls。",
}


def render_integrated_legal_risk_review_zh_cn(report: RiskCardReport, term_style: str = "bilingual") -> str:
    """Render the read-first integrated report in Chinese bilingual style."""

    _validate_term_style(term_style)
    read_first = [card for card in report.risk_cards if card.recommended_review_posture == "read-first"]
    appendix = [card for card in report.risk_cards if card.recommended_review_posture != "read-first"]
    lines = [
        *_frontmatter(report, "法律风险复核", "integrated-review"),
        f"# 法律风险复核: {report.document.title}",
        "",
        "> [!summary] 阅读目的",
        "> 这是一份 read-first 的 legal-to-finance 复核报告。它先给出主线风险，再把原文证据和卡片细节放到后面，方便 agent 或人工继续深读。",
        "",
        "## 核心结论",
        "",
        _zh_executive_takeaway(report, read_first, appendix, term_style),
        "",
    ]
    lines.extend(_zh_priority_map(read_first, appendix, term_style))
    lines.extend(_zh_themes(read_first, term_style))
    lines.extend(_zh_cross_risk_connections(read_first))
    lines.extend(_zh_management_checklist(report, term_style))
    lines.extend(_zh_appendix_notes(appendix, term_style))
    lines.extend(["> [!caution] 免责声明", *_quote_lines(_zh_disclaimer()), ""])
    return "\n".join(lines).rstrip() + "\n"


def render_legal_risk_cards_report_zh_cn(report: RiskCardReport, term_style: str = "bilingual") -> str:
    """Render detailed risk cards in Chinese bilingual style."""

    _validate_term_style(term_style)
    lines = [
        *_frontmatter(report, "法律风险卡片", "risk-cards"),
        f"# 法律风险卡片: {report.document.title}",
        "",
        "> [!summary] v0.3 范围",
        "> 本报告不复述普通 revenue、margin、EPS、valuation 或 peer-comparison 分析；它把法律、监管、审计、治理、披露、税务、担保和重大合同语言转成 finance reader 可执行的核查卡片。",
        "",
        "## Filing Context / 文件背景",
        "",
        f"- Source: `{report.document.source_path}`",
        f"- Parser backend: `{report.document.parser_backend}`",
        f"- Form type: `{report.document.form_type}`",
        f"- Document mode: `{report.document.mode}`",
        "",
    ]
    lines.extend(_zh_coverage_table(report))
    lines.extend(_zh_priority_map(
        [card for card in report.risk_cards if card.recommended_review_posture == "read-first"],
        [card for card in report.risk_cards if card.recommended_review_posture != "read-first"],
        term_style,
    ))
    lines.extend(["## Risk Cards / 风险卡片", ""])
    if not report.risk_cards:
        lines.extend(["未生成法律风险卡片；普通财务 KPI 段落可能已被 route out。", ""])
    for card in report.risk_cards:
        lines.extend(_zh_card(card, term_style))
    lines.extend(["> [!caution] 免责声明", *_quote_lines(_zh_disclaimer()), ""])
    return "\n".join(lines).rstrip() + "\n"


def render_escalation_questions_report_zh_cn(report: RiskCardReport, term_style: str = "bilingual") -> str:
    """Render escalation questions in Chinese bilingual style."""

    _validate_term_style(term_style)
    by_owner: dict[str, list[tuple[RiskCard, str]]] = defaultdict(list)
    for card in report.risk_cards:
        for owner, questions in card.questions.items():
            cleaned_owner = owner.replace("Ask ", "")
            for question in questions:
                by_owner[cleaned_owner].append((card, question))

    lines = [
        *_frontmatter(report, "升级问题清单", "escalation-questions"),
        f"# 升级问题清单: {report.document.title}",
        "",
    ]
    if not by_owner:
        lines.extend(["未生成升级问题。", ""])
    for owner, entries in by_owner.items():
        lines.extend([f"## {_owner(owner)}", ""])
        for card, question in entries:
            lines.append(f"- **{card.card_id} {_domain_title(card, term_style)}** (`{card.priority}`): 应核查 / Please verify: {question}")
        lines.append("")
    lines.extend(["> [!caution] 免责声明", *_quote_lines(_zh_disclaimer()), ""])
    return "\n".join(lines).rstrip() + "\n"


def render_management_follow_up_report_zh_cn(report: RiskCardReport, term_style: str = "bilingual") -> str:
    """Render management follow-up in Chinese bilingual style."""

    _validate_term_style(term_style)
    lines = [
        *_frontmatter(report, "管理层跟进事项", "management-follow-up"),
        f"# 管理层跟进事项: {report.document.title}",
        "",
        "> [!summary] 用途",
        "> 这是一份 Legal、Finance、Auditor、IR、Management 和 Board 的 triage checklist，不是专业结论。",
        "",
        "## 优先跟进事项",
        "",
    ]
    read_first = [card for card in report.risk_cards if card.recommended_review_posture == "read-first"]
    if not read_first:
        lines.extend(["未生成 read-first 跟进事项。", ""])
    for card in read_first:
        lines.append(f"- **{card.card_id} {_domain_title(card, term_style)}**: 需要确认 / Confirm: {card.suggested_management_follow_up}")
    lines.extend(["", "## 披露口径校准", ""])
    if report.disclosure_consistency_questions:
        for question in report.disclosure_consistency_questions:
            lines.append(f"- 不宜直接推断；应核查 / Calibrate wording: {question}")
    else:
        lines.append("- 未生成 disclosure calibration 问题。")
    lines.extend(["", "> [!caution] 免责声明", *_quote_lines(_zh_disclaimer()), ""])
    return "\n".join(lines).rstrip() + "\n"


def _zh_executive_takeaway(
    report: RiskCardReport,
    read_first: list[RiskCard],
    appendix: list[RiskCard],
    term_style: str,
) -> str:
    if not report.risk_cards:
        return "经过证据过滤后未生成 legal-risk cards。"
    names = "、".join(_domain_title(card, term_style) for card in read_first[:5])
    if not names:
        names = "、".join(_domain_title(card, term_style) for card in report.risk_cards[:5])
    suppressed = sum(len(card.weak_or_suppressed_sources) for card in report.risk_cards)
    return (
        f"本次应优先阅读的法律风险主线是：{names}。系统分析了 {report.coverage_summary.paragraphs_total} 个段落，"
        f"route out 了 {report.coverage_summary.financial_kpi_routed_out} 个普通财务 KPI 段落，生成 "
        f"{len(report.risk_cards)} 张事项级风险卡，其中 {len(appendix)} 张属于 appendix / lower-priority。"
        f"{suppressed} 个弱证据、taxonomy-like 或非发行人具体事实的 excerpt 已从主叙事中压低或剔除。"
    )


def _zh_priority_map(read_first: list[RiskCard], appendix: list[RiskCard], term_style: str) -> list[str]:
    lines = [
        "## 风险优先级地图",
        "",
        "| 阅读位置 | Priority | Risk | 为什么重要 | 主要 owner |",
        "| --- | --- | --- | --- | --- |",
    ]
    for card in read_first + appendix:
        lines.append(
            f"| {_posture(card.recommended_review_posture)} | {card.priority} | {card.card_id} {_domain_title(card, term_style)} | "
            f"{_table_cell(_zh_domain_read(card))} | {', '.join(_owner(owner) for owner in card.owners)} |"
        )
    lines.append("")
    return lines


def _zh_themes(cards: list[RiskCard], term_style: str) -> list[str]:
    lines = ["## 重点法务风险主题", ""]
    if not cards:
        return lines + ["没有卡片达到 read-first 证据阈值。", ""]
    for index, card in enumerate(cards, start=1):
        lines.extend(_zh_theme(index, card, term_style))
    return lines


def _zh_theme(index: int, card: RiskCard, term_style: str) -> list[str]:
    lines = [
        f"### {index}. {_domain_title(card, term_style)}",
        "",
        f"- Card: `{card.card_id}`",
        f"- Domain: `{card.risk_domain}`",
        f"- Priority: `{card.priority}`",
        f"- Evidence quality: `{card.evidence_quality}`",
        f"- Owners: {', '.join(_owner(owner) for owner in card.owners)}",
        "",
        "#### 这和普通财务分析的差异",
        "",
        _zh_domain_difference(card),
        "",
        "#### Filing 原文事实（英文证据）",
        "",
    ]
    if card.issuer_specific_facts:
        lines.extend([f"- {fact}" for fact in card.issuer_specific_facts[:6]])
    else:
        lines.append("- 未抽取到足够简洁的 issuer-specific facts；需要回看 Source Excerpts。")
    lines.extend(
        [
            "",
            "#### Finance Reader 应如何理解",
            "",
            _zh_domain_read(card),
            "",
            "#### Legal / Audit / Disclosure 核查重点",
            "",
            _zh_verification(card),
            "",
            "#### 需要问的问题",
            "",
        ]
    )
    questions = _first_questions(card)
    if questions:
        lines.extend([f"- 应核查 / Please verify: {question}" for question in questions])
    else:
        lines.append("- 应指定 Legal、Finance、Auditor、IR 或 Management 核查原文事实和披露口径。")
    lines.extend(
        [
            "",
            "#### 不宜过度表述",
            "",
            _zh_caution(card),
            "",
            "#### Source Support / 原文证据",
            "",
        ]
    )
    for excerpt in card.source_excerpts[:3]:
        lines.append(f"- P{excerpt.paragraph_id:04d} (`{excerpt.evidence_quality}`): {_trim(excerpt.excerpt, 260)}")
    lines.append("")
    return lines


def _zh_card(card: RiskCard, term_style: str) -> list[str]:
    lines = [
        f"### {card.card_id} - {_domain_title(card, term_style)}",
        "",
        f"> [!{_callout(card.priority)}] {card.priority} / {card.reading_decision}",
        f"> Domain: `{card.risk_domain}`",
        f"> Owners: {', '.join(_owner(owner) for owner in card.owners)}",
        f"> Confidence: {card.confidence:.2f}",
        f"> Evidence quality: `{card.evidence_quality}`",
        f"> Review posture: `{card.recommended_review_posture}`",
        "",
        "#### 这和普通财务分析的差异",
        "",
        _zh_domain_difference(card),
        "",
        "#### Finance Reader 应如何理解",
        "",
        _zh_domain_read(card),
        "",
        "#### Filing 原文事实（英文证据）",
        "",
        *([f"- {fact}" for fact in card.issuer_specific_facts] or ["- 未抽取到简洁的 issuer-specific facts。"]),
        "",
        "#### Legal / Regulatory / Audit / Governance Relevance",
        "",
        _zh_verification(card),
        "",
        "#### Financial Statement Linkage / 财报科目连接",
        "",
        *[f"- {item}" for item in card.financial_statement_linkage],
        "",
        "#### Questions To Ask / 应问问题",
        "",
    ]
    for role, questions in card.questions.items():
        lines.extend([f"> [!question] {_owner(role.replace('Ask ', ''))}"])
        for question in questions:
            lines.append(f"> - 应核查 / Please verify: {question}")
        lines.append("")
    lines.extend(
        [
            "#### Suggested Management Follow-Up / 管理层跟进",
            "",
            f"需要确认 / Confirm: {card.suggested_management_follow_up}",
            "",
            "#### What Not To Overstate / 不宜过度表述",
            "",
            _zh_caution(card),
            "",
            "#### Source Excerpts / 原文摘录",
            "",
        ]
    )
    for excerpt in card.source_excerpts:
        lines.extend(
            [
                f"> [!quote] P{excerpt.paragraph_id:04d} `{excerpt.source_ref}` / evidence `{excerpt.evidence_quality}`",
                *_quote_lines(excerpt.excerpt),
                "",
            ]
        )
    return lines


def _zh_coverage_table(report: RiskCardReport) -> list[str]:
    coverage = report.coverage_summary
    return [
        "## Coverage Summary / 覆盖情况",
        "",
        "| Routing bucket | Count |",
        "| --- | ---: |",
        f"| Total paragraphs | {coverage.paragraphs_total} |",
        f"| Filing admin skipped | {coverage.paragraphs_skipped_admin} |",
        f"| Ordinary financial KPI routed out | {coverage.financial_kpi_routed_out} |",
        f"| Business update routed out | {coverage.business_update_routed_out} |",
        f"| Risk-relevant paragraphs | {coverage.risk_relevant_paragraphs} |",
        f"| Risk cards generated | {coverage.risk_cards_generated} |",
        "",
    ]


def _zh_cross_risk_connections(cards: list[RiskCard]) -> list[str]:
    domains = {card.risk_domain for card in cards}
    lines = ["## 跨风险连接", ""]
    connections: list[str] = []
    if {"guarantees_commitments", "material_contracts"}.issubset(domains):
        connections.append("重大合同、license、goodwill / intangible asset 与 guarantee / commitment 可能共同影响收益质量、现金流和披露口径。")
    if {"legal_proceedings_litigation", "tax_cross_border"}.issubset(domains):
        connections.append("诉讼或监管不确定性与 tax reserve、valuation allowance、contingency disclosure 之间需要保持一致。")
    if {"cybersecurity_governance", "legal_proceedings_litigation"}.issubset(domains):
        connections.append("Cybersecurity governance 应与 legal proceedings / incident disclosure 口径分开核查，避免把流程披露写成事件结论。")
    if not connections:
        connections.append("规则未识别出强 cross-risk pattern；仍建议人工复核 read-first 卡片之间的事实连接。")
    lines.extend([f"- {item}" for item in connections])
    lines.append("")
    return lines


def _zh_management_checklist(report: RiskCardReport, term_style: str) -> list[str]:
    by_owner: dict[str, list[str]] = defaultdict(list)
    for card in report.risk_cards:
        if card.recommended_review_posture != "read-first":
            continue
        for owner in card.owners:
            by_owner[_owner(owner)].append(f"{card.card_id} {_domain_title(card, term_style)}: {card.suggested_management_follow_up}")

    lines = ["## 管理层跟进清单", ""]
    if not by_owner:
        return lines + ["未生成 read-first 管理层跟进事项。", ""]
    for owner, items in sorted(by_owner.items()):
        lines.extend([f"### {owner}", ""])
        lines.extend([f"- 需要确认 / Confirm: {item}" for item in items[:6]])
        lines.append("")
    return lines


def _zh_appendix_notes(cards: list[RiskCard], term_style: str) -> list[str]:
    lines = ["## 附录级或低置信卡片", ""]
    if not cards:
        return lines + ["未生成 appendix-level 卡片。", ""]
    for card in cards:
        lines.append(
            f"- {card.card_id} {_domain_title(card, term_style)}: `{card.priority}`, evidence `{card.evidence_quality}`. "
            f"这张卡目前不作为 read-first 主线；需要时可回看原文证据。"
        )
    lines.append("")
    return lines


def _domain_title(card: RiskCard, term_style: str) -> str:
    zh, en = DOMAIN_TERMS.get(card.risk_domain, (card.title, card.title))
    if term_style == "english":
        return en
    if term_style == "translated":
        return zh
    return f"{zh}（{en}）"


def _owner(owner: str) -> str:
    return OWNER_LABELS.get(owner, owner)


def _posture(posture: str) -> str:
    if posture == "read-first":
        return "优先阅读 / read-first"
    return "附录 / appendix"


def _zh_domain_difference(card: RiskCard) -> str:
    return DOMAIN_READS.get(card.risk_domain, card.financial_analysis_difference)


def _zh_domain_read(card: RiskCard) -> str:
    base = DOMAIN_READS.get(card.risk_domain)
    if not base:
        return f"这可能提示需要把 `{card.risk_domain}` 从普通财务叙事中拆出来，由 Legal / Finance / Auditor 核查。"
    if card.risk_domain == "tax_cross_border" and any("711" in fact for fact in card.issuer_specific_facts):
        return f"{base} 如果原文涉及 $711 million release，应特别区分 one-time valuation allowance release 和可持续税务收益。"
    return base


def _zh_verification(card: RiskCard) -> str:
    if card.risk_domain == "tax_cross_border":
        return "应核查 DTA realizability、valuation allowance、more-likely-than-not 证据、jurisdictional projections、uncertain tax positions 和审计支持。"
    if card.risk_domain == "legal_proceedings_litigation":
        return "应核查 matter stage、probable / reasonably possible / remote、accrual、loss range、insurance / indemnity 和 disclosure wording。"
    if card.risk_domain == "guarantees_commitments":
        return "应核查 guarantee 是否 firm / conditional、maximum exposure、mitigation、fair-value treatment、counterparty default 和 termination rights。"
    if card.risk_domain == "material_contracts":
        return "应核查 exclusivity、termination、change of control、performance obligations、IP rights、goodwill / intangible asset 和 revenue-recognition 连接。"
    if card.risk_domain == "cybersecurity_governance":
        return "应核查 board oversight、incident-response ownership、vendor risk、materiality assessment 和 disclosure timing。"
    return f"应核查原文是否支持 `{card.risk_domain}` 的法律、审计、披露和财务影响，避免把 review item 写成确定结论。"


def _zh_caution(card: RiskCard) -> str:
    return CAUTION_BY_DOMAIN.get(
        card.risk_domain,
        f"不宜直接推断为确定的法律、会计、审计或投资结论。除非原文或专业审阅支持，应使用“可能提示 / 应核查 / 需要确认”的表述。",
    )


def _first_questions(card: RiskCard) -> list[str]:
    result: list[str] = []
    for role, questions in card.questions.items():
        for question in questions[:1]:
            result.append(f"{_owner(role.replace('Ask ', ''))}: {question}")
    return result[:5]


def _frontmatter(report: RiskCardReport, title_prefix: str, note_type: str) -> list[str]:
    return [
        "---",
        f'title: "{_yaml_escape(title_prefix + " - " + report.document.title)}"',
        "tags:",
        "  - sec-filing",
        "  - legal-risk",
        "  - zh-CN",
        "  - sec-filing-legal-decoder/v0.3.0",
        f"note_type: {note_type}",
        f'form_type: "{_yaml_escape(report.document.form_type)}"',
        f'document_mode: "{_yaml_escape(report.document.mode)}"',
        f'source_path: "{_yaml_escape(report.document.source_path)}"',
        f"risk_cards: {len(report.risk_cards)}",
        "---",
        "",
    ]


def _zh_disclaimer() -> str:
    return (
        "本项目只是 filing-reading 与 legal-to-finance triage 辅助工具，不构成 legal advice、investment advice、"
        "accounting advice、audit advice，也不能替代合格专业人士审阅。输出应被视为问题清单和阅读线索。"
    )


def _callout(priority: str) -> str:
    return {
        "Critical": "danger",
        "High": "warning",
        "Medium": "attention",
        "Low": "info",
        "Monitor": "note",
    }.get(priority, "info")


def _quote_lines(text: str) -> list[str]:
    return [f"> {line}" if line else ">" for line in text.splitlines()]


def _table_cell(value: str) -> str:
    return _trim(value.replace("|", "/"), 170)


def _trim(value: str, limit: int) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def _yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _validate_term_style(term_style: str) -> None:
    if term_style not in TERM_STYLES:
        raise ValueError(f"Unsupported --term-style: {term_style}")
