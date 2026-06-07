"""终端报告格式化输出。"""
from __future__ import annotations

import unicodedata

import pandas as pd

_CATEGORY_COL_WIDTH = 10


def display_width(text: str) -> int:
    width = 0
    for char in str(text):
        if unicodedata.east_asian_width(char) in ("F", "W"):
            width += 2
        else:
            width += 1
    return width


def pad_display(text: str, width: int) -> str:
    text = str(text)
    padding = width - display_width(text)
    return text if padding < 0 else text + " " * padding


def format_currency(amount: float) -> str:
    return f"¥{amount:,.2f}"


def print_report(
    overview: dict,
    breakdown: pd.DataFrame,
    trend: list[dict],
    export_paths: list[str] | None = None,
) -> None:
    month = overview["month"]
    print("═" * 38)
    print(f"  个人记账小助手 · {month} 收支报告")
    print("═" * 38)
    print()
    print("【收支概览】")
    print(f"  总收入：  {format_currency(overview['income']):>12}")
    print(f"  总支出：  {format_currency(overview['expense']):>12}")
    print(f"  结余：    {format_currency(overview['balance']):>12}")
    print()
    print("【支出分类明细】")
    print(
        f"  {pad_display('分类', _CATEGORY_COL_WIDTH)}"
        f"{'金额':>12}  {'占比':>8}"
    )
    print("  " + "─" * 31)
    if breakdown.empty:
        print("  （本月无支出）")
    else:
        for _, row in breakdown.iterrows():
            print(
                f"  {pad_display(row['分类'], _CATEGORY_COL_WIDTH)}"
                f"{format_currency(row['支出金额']):>12}  "
                f"{row['占比']:>8}"
            )
        total = breakdown["支出金额"].sum()
        print("  " + "─" * 31)
        print(
            f"  {pad_display('合计', _CATEGORY_COL_WIDTH)}"
            f"{format_currency(total):>12}  {'100.0%':>8}"
        )
    print()
    print("【近 3 个月支出趋势】")
    print(f"  {'月份':<10}{'总支出':>12}  {'环比变化':>10}")
    print("  " + "─" * 34)
    for item in trend:
        print(
            f"  {item['month']:<10}"
            f"{format_currency(item['expense']):>12}  "
            f"{item['change']:>10}"
        )
    print()
    if export_paths:
        print("【导出完成】")
        for path in export_paths:
            print(f"  → {path}")
