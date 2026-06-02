# Source-Only Review Mode

`v0.4.1` treats the SEC filing itself as the evidence boundary.

The default and only supported review mode is:

```bash
--review-mode source-only
```

The tool does not enrich risk cards with news, analyst commentary, databases,
law-firm alerts, market data, or web search. It only uses the supplied filing
text plus deterministic rules inside this repository.

## 中文说明

`v0.4.1` 把 SEC filing 本身作为证据边界。

默认且唯一支持的 review mode 是：

```bash
--review-mode source-only
```

工具不会把新闻、卖方报告、外部数据库、律所文章、市场数据或网页搜索内容混入风险卡。
输出只基于用户提供的 filing 文本和本仓库内的 deterministic rules。

## Issuer Profiles

Issuer profiles adjust priority for under-covered issuer patterns. They do not
invent new facts and do not add external context.

Supported profiles:

- `general`
- `small-issuer`
- `foreign-private-issuer`
- `spac-de-spac`
- `manufacturing`
- `solar-manufacturing`

Example:

```bash
sec-filing-legal-decoder risk-cards examples/synthetic_small_fpi_20f.htm \
  --review-mode source-only \
  --issuer-profile foreign-private-issuer \
  --output-dir outputs/sample-small-fpi
```

## 中文说明

Issuer profile 只调整 under-covered issuer 常见风险模式的优先级，不会编造事实，也不会
引入外部背景。

支持的 profile：

- `general`
- `small-issuer`
- `foreign-private-issuer`
- `spac-de-spac`
- `manufacturing`
- `solar-manufacturing`
