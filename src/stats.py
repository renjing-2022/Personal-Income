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
