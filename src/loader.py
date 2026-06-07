"""CSV 读取与数据清洗。"""
from __future__ import annotations

import warnings
from pathlib import Path

import pandas as pd

VALID_TYPES = {"收入", "支出"}
COLUMNS = ["日期", "收支类型", "分类", "金额", "备注"]


def load_csv(path: str | Path) -> pd.DataFrame:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"找不到文件: {file_path}")

    raw = pd.read_csv(file_path, dtype={"备注": str})
    missing = set(COLUMNS) - set(raw.columns)
    if missing:
        raise ValueError(f"CSV 缺少必需列: {', '.join(sorted(missing))}")

    valid_rows = []

    for idx, row in raw.iterrows():
        line_no = idx + 2  # 表头占第 1 行
        try:
            date = pd.to_datetime(row["日期"], errors="raise")
        except Exception:
            warnings.warn(f"第 {line_no} 行日期无效，已跳过")
            continue

        try:
            amount = float(row["金额"])
        except (TypeError, ValueError):
            warnings.warn(f"第 {line_no} 行金额无效，已跳过")
            continue

        if amount <= 0:
            warnings.warn(f"第 {line_no} 行金额 ≤ 0，已跳过")
            continue

        record_type = str(row["收支类型"]).strip()
        if record_type not in VALID_TYPES:
            warnings.warn(f"第 {line_no} 行收支类型无效，已跳过")
            continue

        category = str(row["分类"]).strip() if pd.notna(row["分类"]) else ""
        if not category:
            category = "未分类"

        note = "" if pd.isna(row["备注"]) else str(row["备注"])

        valid_rows.append(
            {
                "日期": date,
                "收支类型": record_type,
                "分类": category,
                "金额": amount,
                "备注": note,
            }
        )

    if not valid_rows:
        raise ValueError("无有效数据")

    df = pd.DataFrame(valid_rows)
    df["年月"] = df["日期"].dt.to_period("M")
    df["是收入"] = df["收支类型"] == "收入"
    df["是支出"] = df["收支类型"] == "支出"
    return df


def get_latest_month(df: pd.DataFrame) -> str:
    return str(df["日期"].max().to_period("M"))
