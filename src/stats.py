"""收支统计纯函数。"""
from __future__ import annotations

import pandas as pd


def monthly_overview(df: pd.DataFrame, month: str) -> dict:
    period = pd.Period(month, freq="M")
    month_df = df[df["年月"] == period]
    income = month_df.loc[month_df["是收入"], "金额"].sum()
    expense = month_df.loc[month_df["是支出"], "金额"].sum()
    return {
        "month": month,
        "income": float(income),
        "expense": float(expense),
        "balance": float(income - expense),
    }


def category_breakdown(df: pd.DataFrame, month: str) -> pd.DataFrame:
    period = pd.Period(month, freq="M")
    expenses = df[(df["年月"] == period) & (df["是支出"])]
    if expenses.empty:
        return pd.DataFrame(columns=["分类", "支出金额", "占比"])

    grouped = (
        expenses.groupby("分类", as_index=False)["金额"]
        .sum()
        .rename(columns={"金额": "支出金额"})
        .sort_values("支出金额", ascending=False)
    )
    total = grouped["支出金额"].sum()
    if total == 0:
        grouped["占比"] = "0.0%"
    else:
        grouped["占比"] = grouped["支出金额"].apply(
            lambda x: f"{x / total * 100:.1f}%"
        )
    return grouped.reset_index(drop=True)


def _format_change(current: float, previous: float) -> str:
    if previous == 0:
        return "—"
    pct = (current - previous) / previous * 100
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct:.1f}%"


def trend_3months(df: pd.DataFrame, month: str) -> list[dict]:
    target = pd.Period(month, freq="M")
    months = [target - 2, target - 1, target]
    result = []
    prev_expense = None
    for period in months:
        month_str = str(period)
        expense = float(
            df[(df["年月"] == period) & (df["是支出"])]["金额"].sum()
        )
        if prev_expense is None:
            change = "—"
        else:
            change = _format_change(expense, prev_expense)
        result.append({"month": month_str, "expense": expense, "change": change})
        prev_expense = expense
    return result
