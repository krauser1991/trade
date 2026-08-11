#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "templates" / "daily-review-dark.html"
OUTPUT_DIR = ROOT / "output" / "html"
REQUIRED_NOTICE = "仅作个人复盘与交易计划，不构成投资建议。"
REQUIRED_FIELDS = [
    "date",
    "title",
    "summary",
    "metrics",
    "market_review",
    "themes",
    "stocks",
    "next_day_plan",
    "discipline",
    "risk_notice",
]


def esc(value: Any) -> str:
    if value is None or value == "":
        value = "未提供"
    return html.escape(str(value), quote=True)


def load_review(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    return data


def validate_review(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing required field: {field}")
    if data.get("risk_notice") and REQUIRED_NOTICE not in str(data["risk_notice"]):
        errors.append(f"risk_notice must contain: {REQUIRED_NOTICE}")
    if "summary" in data and not isinstance(data["summary"], dict):
        errors.append("summary must be an object")
    for list_field in ["metrics", "market_review", "themes", "hot_themes", "limit_up_ladder", "stocks", "discipline"]:
        if list_field in data and not isinstance(data[list_field], list):
            errors.append(f"{list_field} must be a list")
    if "next_day_plan" in data and not isinstance(data["next_day_plan"], dict):
        errors.append("next_day_plan must be an object")
    return errors


def safe_filename(value: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|\\s]+", "-", value.strip())
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    return cleaned or "daily-review"


def render_tags(tags: list[Any]) -> str:
    return "".join(f'<span class="tag">{esc(tag)}</span>' for tag in tags)


def render_metric_cards(metrics: list[dict[str, Any]]) -> str:
    cards = []
    for item in metrics:
        tone = esc(item.get("tone", "neutral"))
        cards.append(
            "\n".join(
                [
                    f'<article class="metric tone-{tone}">',
                    f'  <div class="label">{esc(item.get("label"))}</div>',
                    f'  <div class="value">{esc(item.get("value"))}</div>',
                    f'  <div class="change">{esc(item.get("change"))}</div>',
                    "</article>",
                ]
            )
        )
    return "\n".join(cards)


def render_list(items: list[Any]) -> str:
    return "\n".join(f"<li>{esc(item)}</li>" for item in items)


def render_market_sections(sections: list[dict[str, Any]]) -> str:
    rendered = []
    for item in sections:
        rendered.append(
            "\n".join(
                [
                    '<article class="mini-card">',
                    f'  <h3>{esc(item.get("title"))}</h3>',
                    f'  <p>{esc(item.get("content"))}</p>',
                    "</article>",
                ]
            )
        )
    return "\n".join(rendered)


def tone_class(value: Any) -> str:
    text = str(value)
    if text.startswith("+"):
        return "up"
    if text.startswith("-"):
        return "down"
    return ""


def render_theme_rows(themes: list[dict[str, Any]]) -> str:
    rows = []
    for item in themes:
        rows.append(
            "<tr>"
            f"<td class=\"cyan\">{esc(item.get('name'))}</td>"
            f"<td>{esc(item.get('status'))}</td>"
            f"<td class=\"hot\">{esc(item.get('strength'))}</td>"
            f"<td>{esc(item.get('core'))}</td>"
            f"<td>{esc(item.get('strategy'))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_hot_theme_rows(themes: list[dict[str, Any]]) -> str:
    if not themes:
        return '<tr><td colspan="6" class="muted">未提供</td></tr>'
    rows = []
    for item in themes:
        rows.append(
            "<tr>"
            f"<td class=\"hot\">{esc(item.get('rank'))}</td>"
            f"<td class=\"cyan\">{esc(item.get('name'))}</td>"
            f"<td>{esc(item.get('heat'))}</td>"
            f"<td>{esc(item.get('leaders'))}</td>"
            f"<td>{esc(item.get('driver'))}</td>"
            f"<td>{esc(item.get('review'))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_ladder_rows(ladder: list[dict[str, Any]]) -> str:
    if not ladder:
        return '<tr><td colspan="5" class="muted">未提供</td></tr>'
    rows = []
    for item in ladder:
        rows.append(
            "<tr>"
            f"<td class=\"hot\">{esc(item.get('height'))}</td>"
            f"<td class=\"cyan\">{esc(item.get('stocks'))}</td>"
            f"<td>{esc(item.get('theme'))}</td>"
            f"<td>{esc(item.get('status'))}</td>"
            f"<td>{esc(item.get('tomorrow'))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_stock_rows(stocks: list[dict[str, Any]]) -> str:
    rows = []
    for item in stocks:
        change = item.get("change")
        cls = tone_class(change)
        rows.append(
            "<tr>"
            f"<td class=\"cyan\">{esc(item.get('name'))}</td>"
            f"<td>{esc(item.get('role'))}</td>"
            f"<td class=\"{cls}\">{esc(change)}</td>"
            f"<td>{esc(item.get('signal'))}</td>"
            f"<td>{esc(item.get('action'))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_account_panel(account: dict[str, Any]) -> str:
    fields = [
        ("总资产", account.get("total_asset")),
        ("当日盈亏", account.get("daily_pnl")),
        ("仓位", account.get("position_ratio")),
        ("现金", account.get("cash")),
    ]
    metrics = " · ".join(f'<span class="cyan">{label}</span> {esc(value)}' for label, value in fields)
    note = esc(account.get("note", "未提供"))
    return f"<p>{metrics}</p><p class=\"muted\">{note}</p>"


def render_trade_rows(trades: list[dict[str, Any]]) -> str:
    rows = []
    for item in trades:
        rows.append(
            "<tr>"
            f"<td>{esc(item.get('time'))}</td>"
            f"<td class=\"cyan\">{esc(item.get('stock'))}</td>"
            f"<td>{esc(item.get('side'))}</td>"
            f"<td>{esc(item.get('price'))}</td>"
            f"<td>{esc(item.get('amount'))}</td>"
            f"<td>{esc(item.get('review'))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_holding_rows(holdings: list[dict[str, Any]]) -> str:
    rows = []
    for item in holdings:
        rows.append(
            "<tr>"
            f"<td class=\"cyan\">{esc(item.get('name'))}</td>"
            f"<td>{esc(item.get('position'))}</td>"
            f"<td>{esc(item.get('pnl'))}</td>"
            f"<td>{esc(item.get('plan'))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_next_day_plan(plan: dict[str, Any]) -> str:
    cards = [
        ("主攻方向", f"<p>{esc(plan.get('main_direction'))}</p>"),
        ("买入条件", f"<ul>{render_list(plan.get('buy_conditions', []))}</ul>"),
        ("卖出/禁买", f"<ul>{render_list(plan.get('sell_conditions', []))}{render_list(plan.get('forbidden', []))}</ul>"),
    ]
    return "\n".join(f'<article class="plan-card"><h3>{title}</h3>{body}</article>' for title, body in cards)


def render_review(data: dict[str, Any], template: str) -> str:
    summary = data.get("summary", {})
    replacements = {
        "title": esc(data.get("title")),
        "date": esc(data.get("date")),
        "subtitle": esc(data.get("subtitle", "盘后复盘")),
        "tags": render_tags(data.get("tags", [])),
        "metric_cards": render_metric_cards(data.get("metrics", [])),
        "summary_headline": esc(summary.get("headline")),
        "summary_points": render_list(summary.get("points", [])),
        "market_sections": render_market_sections(data.get("market_review", [])),
        "theme_rows": render_theme_rows(data.get("themes", [])),
        "hot_theme_rows": render_hot_theme_rows(data.get("hot_themes", [])),
        "limit_up_ladder_rows": render_ladder_rows(data.get("limit_up_ladder", [])),
        "stock_rows": render_stock_rows(data.get("stocks", [])),
        "account_panel": render_account_panel(data.get("account", {})),
        "trade_rows": render_trade_rows(data.get("trades", [])),
        "holding_rows": render_holding_rows(data.get("holdings", [])),
        "next_day_plan": render_next_day_plan(data.get("next_day_plan", {})),
        "discipline_items": render_list(data.get("discipline", [])),
        "risk_notice": esc(data.get("risk_notice")),
    }
    html_text = template
    for key, value in replacements.items():
        html_text = html_text.replace("{{" + key + "}}", value)
    return html_text


def write_html(data: dict[str, Any], html_text: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{safe_filename(str(data.get('date', 'date')))}-{safe_filename(str(data.get('title', 'daily-review')))}.html"
    output = OUTPUT_DIR / filename
    output.write_text(html_text, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a daily review JSON file into dark HTML.")
    parser.add_argument("json_path", type=Path)
    args = parser.parse_args()

    try:
        data = load_review(args.json_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"failed to load review JSON: {exc}", file=sys.stderr)
        return 1

    errors = validate_review(data)
    if errors:
        for error in errors:
            print(f"validation error: {error}", file=sys.stderr)
        return 1

    try:
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"failed to read template: {exc}", file=sys.stderr)
        return 1

    output = write_html(data, render_review(data, template))
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
