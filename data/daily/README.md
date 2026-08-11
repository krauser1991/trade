# 每日复盘结构化数据

本目录存放每日复盘视觉化输出使用的 JSON 数据。

## 文件命名

正式数据文件使用：

```text
YYYY-MM-DD-market.json
```

例如：

```text
2026-08-11-market.json
```

## 数据来源

| 数据类型 | 推荐来源 | 要求 |
|---|---|---|
| 指数、成交额、涨跌家数 | 同花顺、东方财富、交易软件收盘页 | 必须确认交易日期 |
| 涨停、跌停、连板高度 | 同花顺涨停复盘、东方财富涨停池 | 口径要在当天复盘中保持一致 |
| 题材与核心股 | 同花顺概念、东财概念、盘中观察 | 必须区分主线、分支和蹭题材 |
| 热门题材排行 | 同花顺涨停复盘、连板网、交易软件题材涨停池 | 无法核验时写 `待核验` |
| 连板梯队 | 同花顺涨停复盘、连板网、交易软件涨停池 | 必须记录最高板、2板以上、首板扩散 |
| 账户、持仓、成交 | 券商截图、成交记录、手动填写 | 必须以用户提供为准 |
| 纪律问题 | 用户盘中行为描述 | 不能从行情数据猜测 |

## 填写规则

- 必填字段不能删除；
- 不知道的数据写 `未提供`，不要猜；
- 百分比和金额可以用字符串，保留原始阅读格式；
- A 股颜色口径固定为红涨绿跌；
- `risk_notice` 必须包含 `仅作个人复盘与交易计划，不构成投资建议。`

## 生成命令

```bash
python3 scripts/render_daily_review.py data/daily/YYYY-MM-DD-market.json
node scripts/verify_daily_review_html.js output/html/YYYY-MM-DD-标题.html
node scripts/screenshot_daily_review.js output/html/YYYY-MM-DD-标题.html
```
