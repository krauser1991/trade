import csv
from pathlib import Path

ROOT = Path("/Users/krauser/Documents/Obsidian Vault/trade")
CSV_PATH = ROOT / "equity-curve/equity_curve.csv"
SVG_PATH = ROOT / "equity-curve/资金曲线.svg"

rows = []
deposits = [
    ("2026-07-08", 50000),
    ("2026-07-13", 80000),
    ("2026-07-14", 100000),
]


def cumulative_deposit(date: str) -> float:
    return sum(amount for start, amount in deposits if date >= start)


with CSV_PATH.open(encoding="utf-8") as f:
    for row in csv.DictReader(f):
        row["total_assets_num"] = float(row["total_assets"])
        row["daily_pnl_num"] = float(row["daily_pnl"])
        row["deposit_num"] = cumulative_deposit(row["date"])
        row["adjusted_assets_num"] = row["total_assets_num"] - row["deposit_num"]
        rows.append(row)

raw_min = min(min(r["total_assets_num"], r["adjusted_assets_num"]) for r in rows)
raw_max = max(max(r["total_assets_num"], r["adjusted_assets_num"]) for r in rows)
min_y = int((raw_min - 10000) // 10000 * 10000)
max_y = int((raw_max + 10000) // 10000 * 10000)
chart_left = 92
chart_right = 912
chart_top = 116
chart_bottom = 448
width = chart_right - chart_left
height = chart_bottom - chart_top
step = width / (len(rows) - 1)


def x_at(i):
    return chart_left + i * step


def y_at(value):
    return chart_bottom - (value - min_y) / (max_y - min_y) * height


points = " ".join(f"{x_at(i):.0f},{y_at(r['total_assets_num']):.0f}" for i, r in enumerate(rows))
adjusted_points = " ".join(f"{x_at(i):.0f},{y_at(r['adjusted_assets_num']):.0f}" for i, r in enumerate(rows))
last = rows[-1]
prev = rows[-2]
last_color = "#ef4444" if last["total_assets_num"] >= prev["total_assets_num"] else "#2563eb"
adjusted_last_color = "#ef4444" if last["adjusted_assets_num"] >= prev["adjusted_assets_num"] else "#2563eb"
high_value = max(r["total_assets_num"] for r in rows)
high_row = next(r for r in rows if r["total_assets_num"] == high_value)
adjusted_high_value = max(r["adjusted_assets_num"] for r in rows)
adjusted_high_row = next(r for r in rows if r["adjusted_assets_num"] == adjusted_high_value)

svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="980" height="560" viewBox="0 0 980 560" role="img" aria-labelledby="title desc">',
    '  <title id="title">资金曲线</title>',
    f'  <desc id="desc">{rows[0]["date"]} 至 {last["date"]}，展示券商总资产与剔除7月8日5万元、7月13日8万元、7月14日10万元入金后的调整资产。</desc>',
    '  <rect width="980" height="560" fill="#ffffff"/>',
    '  <text x="56" y="52" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="28" font-weight="700" fill="#202124">资金曲线</text>',
    '  <text x="56" y="82" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="14" fill="#6b7280">单位：人民币元 ｜ 数据来源：equity_curve.csv</text>',
    "",
    f'  <line x1="{chart_left}" y1="{chart_bottom}" x2="{chart_right}" y2="{chart_bottom}" stroke="#d1d5db" stroke-width="1"/>',
    f'  <line x1="{chart_left}" y1="{chart_top}" x2="{chart_left}" y2="{chart_bottom}" stroke="#d1d5db" stroke-width="1"/>',
]

grid_values = list(range(min_y + 10000, max_y + 1, 10000))
for value in grid_values:
    y = y_at(value)
    svg.append(f'  <line x1="{chart_left}" y1="{y:.0f}" x2="{chart_right}" y2="{y:.0f}" stroke="#eef2f7" stroke-width="1"/>')

for value in range(min_y, max_y + 1, 10000):
    label = f"{value / 10000:.1f}万"
    svg.append(f'  <text x="28" y="{y_at(value)+5:.0f}" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="12" fill="#6b7280">{label}</text>')

high_y = y_at(high_value)
adjusted_high_y = y_at(adjusted_high_value)
svg.extend([
    f'  <line x1="{chart_left}" y1="{high_y:.0f}" x2="{chart_right}" y2="{high_y:.0f}" stroke="#ef4444" stroke-width="1.9" stroke-dasharray="6 5" opacity="0.9"/>',
    f'  <text x="{chart_left + 8}" y="{high_y - 8:.0f}" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="12" font-weight="700" fill="#ef4444">总资产新高 {high_value:,.2f}（{high_row["date"]}）</text>',
    f'  <line x1="{chart_left}" y1="{adjusted_high_y:.0f}" x2="{chart_right}" y2="{adjusted_high_y:.0f}" stroke="#2563eb" stroke-width="1.9" stroke-dasharray="6 5" opacity="0.9"/>',
    f'  <text x="{chart_left + 8}" y="{adjusted_high_y + 18:.0f}" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="12" font-weight="700" fill="#2563eb">剔除入金新高 {adjusted_high_value:,.2f}（{adjusted_high_row["date"]}）</text>',
])

svg.extend([
    "",
    f'  <polyline points="{points}" fill="none" stroke="#ef4444" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
    f'  <polyline points="{adjusted_points}" fill="none" stroke="#2563eb" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="9 6"/>',
])

for i, row in enumerate(rows):
    color = last_color if i == len(rows) - 1 else ("#2563eb" if row["daily_pnl"].startswith("-") else "#ef4444")
    x = x_at(i)
    y = y_at(row["total_assets_num"])
    svg.append(f'  <circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{color}"/>')
    svg.append(f'  <circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="{color}" opacity="0.14"/>')

for i, row in enumerate(rows):
    if row["date"] >= "2026-07-08":
        x = x_at(i)
        y = y_at(row["adjusted_assets_num"])
        svg.append(f'  <rect x="{x-5:.0f}" y="{y-5:.0f}" width="10" height="10" rx="2" fill="#2563eb"/>')
        svg.append(f'  <rect x="{x-9:.0f}" y="{y-9:.0f}" width="18" height="18" rx="4" fill="#2563eb" opacity="0.12"/>')

for i, row in enumerate(rows):
    x = x_at(i) - 24
    y = 484 if i % 2 == 0 else 506
    label = row["date"][5:]
    svg.append(f'  <text x="{x:.0f}" y="{y}" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="11" fill="#374151">{label}</text>')

important = {
    "2026-06-26": "低仓位新高",
    "2026-06-30": "6月收官新高",
    "2026-07-02": "满仓大回撤",
    "2026-07-08": "入金5万后回撤",
    "2026-07-10": "总盈亏转正",
    "2026-07-13": "入金8万后大回撤",
    "2026-07-14": "入金10万仍回撤",
    "2026-07-15": "恢复标准券但仍亏",
}

for i, row in enumerate(rows):
    if row["date"] in important or i == len(rows) - 1:
        x = x_at(i)
        y = y_at(row["total_assets_num"])
        label_x = min(max(x - 56, 100), 790)
        label_y = max(y - 16, 112)
        color = "#ef4444" if row["daily_pnl_num"] >= 0 else "#2563eb"
        svg.append(f'  <text x="{label_x:.0f}" y="{label_y:.0f}" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="13" font-weight="700" fill="{color}">{float(row["total_assets"]):,.2f}</text>')
        svg.append(f'  <text x="{label_x:.0f}" y="{label_y + 20:.0f}" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="12" fill="#6b7280">{important.get(row["date"], "")}</text>')

svg.extend([
    "",
    '  <rect x="704" y="30" width="228" height="102" rx="8" fill="#fff7f7" stroke="#fecaca"/>',
    '  <text x="724" y="62" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="13" fill="#6b7280">当前记录</text>',
    f'  <text x="724" y="88" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="22" font-weight="700" fill="{last_color}">{last["total_assets_num"]:,.2f}</text>',
    f'  <text x="724" y="112" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="14" font-weight="700" fill="{adjusted_last_color}">剔除入金：{last["adjusted_assets_num"]:,.2f}</text>',
    '  <line x1="56" y1="100" x2="88" y2="100" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>',
    '  <text x="98" y="105" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="12" fill="#374151">券商总资产</text>',
    '  <line x1="190" y1="100" x2="222" y2="100" stroke="#2563eb" stroke-width="3" stroke-dasharray="9 6" stroke-linecap="round"/>',
    '  <text x="232" y="105" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="12" fill="#374151">剔除累计入金</text>',
    f'  <text x="92" y="524" font-family="Arial, \'PingFang SC\', \'Microsoft YaHei\', sans-serif" font-size="12" fill="#9ca3af">说明：蓝色虚线扣除7月8日50,000元、7月13日80,000元和7月14日100,000元入金；{last["date"]} 调整后资产 {last["adjusted_assets_num"]:,.2f}。</text>',
    "</svg>",
])

SVG_PATH.write_text("\n".join(svg), encoding="utf-8")
print(SVG_PATH)
