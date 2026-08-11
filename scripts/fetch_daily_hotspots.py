#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def require_akshare():
    try:
        import akshare as ak  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "akshare is required for hotspot fetching. "
            "Install with: python3 -m pip install akshare"
        ) from exc
    return ak


def join_first(values: Any, limit: int = 8) -> str:
    return "、".join(str(item) for item in list(values)[:limit])


def build_hot_themes(zt_df) -> list[dict[str, str]]:
    grouped = (
        zt_df.groupby("所属行业")
        .agg(
            limit_count=("代码", "count"),
            max_ladder=("连板数", "max"),
            leaders=("名称", lambda s: join_first(s, 5)),
        )
        .sort_values(["limit_count", "max_ladder"], ascending=False)
        .head(8)
        .reset_index()
    )
    rows: list[dict[str, str]] = []
    for index, item in grouped.iterrows():
        rows.append(
            {
                "rank": str(index + 1),
                "name": str(item["所属行业"]),
                "heat": f"{int(item['limit_count'])}只涨停 / 最高{int(item['max_ladder'])}板",
                "leaders": str(item["leaders"]),
                "driver": "涨停池行业聚合",
                "review": "只作为市场热度参考；若账户无对应核心持仓，不追后排。",
            }
        )
    return rows


def build_ladder(zt_df) -> list[dict[str, str]]:
    ladder = (
        zt_df.groupby("连板数")
        .agg(
            count=("代码", "count"),
            stocks=("名称", lambda s: join_first(s, 12)),
            industries=("所属行业", lambda s: "、".join(sorted({str(x) for x in s}))),
        )
        .sort_index(ascending=False)
        .reset_index()
    )
    rows: list[dict[str, str]] = []
    for _, item in ladder.iterrows():
        height = int(item["连板数"])
        rows.append(
            {
                "height": f"{height}板" if height > 1 else "首板",
                "stocks": str(item["stocks"]),
                "theme": str(item["industries"]),
                "status": f"{int(item['count'])}只",
                "tomorrow": "观察晋级率和断板反馈；高度断层时优先降仓，不追新题材。",
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch daily A-share hotspot and limit-up ladder data.")
    parser.add_argument("date", help="Trading date, YYYYMMDD, for example 20260811")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()

    ak = require_akshare()
    zt_df = ak.stock_zt_pool_em(date=args.date)
    data = {
        "date": args.date,
        "source": "AkShare stock_zt_pool_em; limit-up pool is Eastmoney口径. 同花顺概念列表可由 stock_board_concept_name_ths 补充映射。",
        "limit_up_count": int(len(zt_df)),
        "hot_themes": build_hot_themes(zt_df),
        "limit_up_ladder": build_ladder(zt_df),
    }
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
