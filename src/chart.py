"""图表生成（matplotlib 延迟导入）。"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.stats import category_breakdown, trend_3months


def _setup_chinese_font():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    return plt


def _pie_data(breakdown: pd.DataFrame) -> tuple[list[str], list[float]]:
    if breakdown.empty:
        return ["无数据"], [1.0]
    labels = breakdown["分类"].tolist()
    values = breakdown["支出金额"].tolist()
    total = sum(values)
    merged_labels, merged_values = [], []
    other = 0.0
    for label, value in zip(labels, values):
        if value / total < 0.05:
            other += value
        else:
            merged_labels.append(label)
            merged_values.append(value)
    if other > 0:
        merged_labels.append("其他")
        merged_values.append(other)
    return merged_labels, merged_values


def generate_charts(df: pd.DataFrame, month: str, output_dir: str | Path) -> list[Path]:
    try:
        plt = _setup_chinese_font()
    except ImportError as exc:
        raise ImportError("请先安装 matplotlib: pip install matplotlib") from exc

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    # 饼图
    breakdown = category_breakdown(df, month)
    labels, values = _pie_data(breakdown)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.set_title(f"{month} 支出分类占比")
    pie_path = out / f"pie_{month}.png"
    fig.savefig(pie_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(pie_path)

    # 折线图
    trend = trend_3months(df, month)
    months = [t["month"] for t in trend]
    expenses = [t["expense"] for t in trend]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(months, expenses, marker="o")
    for x, y in zip(months, expenses):
        ax.annotate(f"¥{y:,.0f}", (x, y), textcoords="offset points", xytext=(0, 8), ha="center")
    ax.set_title("近 3 个月支出趋势")
    ax.set_xlabel("月份")
    ax.set_ylabel("总支出（元）")
    trend_path = out / "trend_3m.png"
    fig.savefig(trend_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(trend_path)

    return paths
