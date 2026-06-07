"""CSV 导出。"""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def _ensure_dir(output_dir: str | Path) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_summary(
    breakdown: pd.DataFrame, month: str, output_dir: str | Path
) -> Path:
    out = _ensure_dir(output_dir)
    file_path = out / f"summary_{month}.csv"
    breakdown.to_csv(file_path, index=False, encoding="utf-8-sig")
    return file_path


def write_detail(df: pd.DataFrame, month: str, output_dir: str | Path) -> Path:
    out = _ensure_dir(output_dir)
    period = pd.Period(month, freq="M")
    month_df = df[df["年月"] == period][
        ["日期", "收支类型", "分类", "金额", "备注"]
    ].copy()
    month_df["日期"] = month_df["日期"].dt.strftime("%Y-%m-%d")
    file_path = out / f"detail_{month}.csv"
    month_df.to_csv(file_path, index=False, encoding="utf-8-sig")
    return file_path
