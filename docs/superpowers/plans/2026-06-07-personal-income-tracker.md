# 个人记账小助手 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个命令行个人记账小助手，读取收支 CSV，终端展示当月收支全景与近 3 月趋势，支持汇总/明细导出，可选生成饼图与折线图。

**Architecture:** 扁平 `main.py` 作为 CLI 入口，业务逻辑拆分到 `src/` 下 5 个模块：`loader`（读洗数据）、`stats`（纯函数统计）、`display`（终端格式化）、`export`（CSV 写出）、`chart`（matplotlib 图表，延迟导入）。数据流单向：CSV → loader → stats → display/export/chart。

**Tech Stack:** Python 3.10+ · pandas ≥ 2.0 · matplotlib ≥ 3.7 · argparse（标准库）· pytest ≥ 7.0（开发依赖）

**Design Spec:** `docs/superpowers/specs/2026-06-07-personal-income-tracker-design.md`

---

## File Map

| 文件 | 职责 |
|------|------|
| `main.py` | argparse 解析、流程编排、错误退出 |
| `requirements.txt` | 运行时依赖 pandas、matplotlib |
| `.gitignore` | 忽略 `.venv`、`__pycache__`、`output/` |
| `data/expenses.csv` | 样本数据（从根目录移入） |
| `src/__init__.py` | 包标识 |
| `src/loader.py` | `load_csv()`、`get_latest_month()` |
| `src/stats.py` | `monthly_overview()`、`category_breakdown()`、`trend_3months()` |
| `src/display.py` | `format_currency()`、`print_report()` |
| `src/export.py` | `write_summary()`、`write_detail()` |
| `src/chart.py` | `generate_charts()` 饼图 + 折线图 |
| `tests/conftest.py` | pytest fixture、sys.path 配置 |
| `tests/test_stats.py` | 统计逻辑单元测试 |
| `README.md` | 项目说明（中文，6 块结构） |

---

## Task 1: 项目骨架与 CLI 入口

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `src/__init__.py`
- Create: `main.py`
- Create: `data/expenses.csv`（从根目录 `expenses.csv` 复制）

- [ ] **Step 1: 创建 requirements.txt**

```
pandas>=2.0
matplotlib>=3.7
```

- [ ] **Step 2: 创建 .gitignore**

```
.venv/
__pycache__/
*.pyc
output/
.pytest_cache/
.env
```

- [ ] **Step 3: 创建 src/__init__.py**

```python
"""个人记账小助手业务模块。"""
```

- [ ] **Step 4: 复制样本数据**

```bash
mkdir data
cp expenses.csv data/expenses.csv
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path data
Copy-Item expenses.csv data/expenses.csv
```

- [ ] **Step 5: 创建 main.py（仅 CLI 骨架）**

```python
"""个人记账小助手 — CLI 入口。"""
import argparse
import re
import sys


def parse_month(value: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}", value):
        raise argparse.ArgumentTypeError("月份格式须为 YYYY-MM，例如 2026-01")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="个人记账小助手：读取收支 CSV，生成统计报告"
    )
    parser.add_argument("--input", required=True, help="CSV 文件路径")
    parser.add_argument("--month", type=parse_month, help="分析月份 YYYY-MM，默认取最新月")
    parser.add_argument(
        "--export",
        choices=["summary", "detail"],
        default="summary",
        help="导出类型：summary（分类汇总）或 detail（原始明细）",
    )
    parser.add_argument("--output", default="output/", help="导出目录，默认 output/")
    parser.add_argument("--chart", action="store_true", help="生成饼图和折线图 PNG")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    # 业务逻辑在后续 Task 中接入
    print(f"参数解析成功: input={args.input}, month={args.month}, export={args.export}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: 验证 CLI 骨架**

```bash
pip install -r requirements.txt
python main.py --help
```

Expected: 显示帮助信息，列出 `--input`、`--month`、`--export`、`--output`、`--chart`

- [ ] **Step 7: Commit**

```bash
git add requirements.txt .gitignore src/__init__.py main.py data/expenses.csv
git commit -m "feat: scaffold project skeleton and CLI parser"
```

---

## Task 2: 统计模块 — monthly_overview

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/test_stats.py`
- Create: `src/stats.py`

- [ ] **Step 1: 创建 tests/conftest.py**

```python
import sys
from pathlib import Path

import pandas as pd
import pytest

# 将项目根目录加入 sys.path，使 `from src.xxx import` 可用
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """构造带计算列的测试 DataFrame。"""
    dates = pd.to_datetime(
        ["2026-01-05", "2026-01-07", "2026-01-12", "2025-12-14", "2025-12-06"]
    )
    types = ["收入", "支出", "支出", "支出", "收入"]
    return pd.DataFrame(
        {
            "日期": dates,
            "收支类型": types,
            "分类": ["工资", "购物", "餐饮", "娱乐", "工资"],
            "金额": [6800.0, 320.0, 68.0, 88.0, 6800.0],
            "备注": ["月薪", "年货", "聚餐", "聚会", "月薪"],
            "年月": dates.to_period("M"),
            "是收入": [t == "收入" for t in types],
            "是支出": [t == "支出" for t in types],
        }
    )
```

- [ ] **Step 2: 写失败测试 test_monthly_overview**

在 `tests/test_stats.py` 中：

```python
from src.stats import monthly_overview


def test_monthly_overview(sample_df):
    result = monthly_overview(sample_df, "2026-01")
    assert result["month"] == "2026-01"
    assert result["income"] == 6800.0
    assert result["expense"] == 388.0  # 320 + 68
    assert result["balance"] == 6412.0


def test_monthly_overview_empty_month(sample_df):
    result = monthly_overview(sample_df, "2020-06")
    assert result["income"] == 0.0
    assert result["expense"] == 0.0
    assert result["balance"] == 0.0
```

- [ ] **Step 3: 运行测试确认失败**

```bash
pip install pytest
pytest tests/test_stats.py::test_monthly_overview -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'src.stats'` 或 `cannot import name 'monthly_overview'`

- [ ] **Step 4: 实现 src/stats.py 中的 monthly_overview**

```python
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
```

- [ ] **Step 5: 运行测试确认通过**

```bash
pytest tests/test_stats.py::test_monthly_overview tests/test_stats.py::test_monthly_overview_empty_month -v
```

Expected: 2 passed

- [ ] **Step 6: Commit**

```bash
git add tests/conftest.py tests/test_stats.py src/stats.py
git commit -m "feat: add monthly_overview stats with tests"
```

---

## Task 3: 统计模块 — category_breakdown

**Files:**
- Modify: `tests/test_stats.py`
- Modify: `src/stats.py`

- [ ] **Step 1: 写失败测试 test_category_breakdown**

在 `tests/test_stats.py` 追加：

```python
from src.stats import category_breakdown


def test_category_breakdown(sample_df):
    result = category_breakdown(sample_df, "2026-01")
    assert list(result.columns) == ["分类", "支出金额", "占比"]
    assert len(result) == 2
    assert result.iloc[0]["分类"] == "购物"
    assert result.iloc[0]["支出金额"] == 320.0
    assert result.iloc[0]["占比"] == "82.5%"
    assert result.iloc[1]["分类"] == "餐饮"
    assert result.iloc[1]["支出金额"] == 68.0
    assert result.iloc[1]["占比"] == "17.5%"
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/test_stats.py::test_category_breakdown -v
```

Expected: FAIL — `cannot import name 'category_breakdown'`

- [ ] **Step 3: 实现 category_breakdown**

在 `src/stats.py` 追加：

```python
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
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/test_stats.py::test_category_breakdown -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_stats.py src/stats.py
git commit -m "feat: add category_breakdown stats with tests"
```

---

## Task 4: 统计模块 — trend_3months

**Files:**
- Modify: `tests/test_stats.py`
- Modify: `src/stats.py`

- [ ] **Step 1: 写失败测试 test_trend_3months**

在 `tests/test_stats.py` 追加：

```python
from src.stats import trend_3months


def test_trend_3months(sample_df):
    result = trend_3months(sample_df, "2026-01")
    assert len(result) == 3
    assert result[0]["month"] == "2025-11"
    assert result[0]["expense"] == 0.0
    assert result[0]["change"] == "—"
    assert result[1]["month"] == "2025-12"
    assert result[1]["expense"] == 88.0
    assert result[1]["change"] == "—"  # 上月为 0，环比显示 —
    assert result[2]["month"] == "2026-01"
    assert result[2]["expense"] == 388.0
    assert result[2]["change"] == "+340.9%"  # (388-88)/88*100
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/test_stats.py::test_trend_3months -v
```

Expected: FAIL

- [ ] **Step 3: 实现 trend_3months 及辅助函数**

在 `src/stats.py` 追加：

```python
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
```

- [ ] **Step 4: 运行全部 stats 测试**

```bash
pytest tests/test_stats.py -v
```

Expected: 5 passed

- [ ] **Step 5: Commit**

```bash
git add tests/test_stats.py src/stats.py
git commit -m "feat: add trend_3months stats with tests"
```

---

## Task 5: 数据加载模块 loader

**Files:**
- Create: `src/loader.py`

- [ ] **Step 1: 实现 src/loader.py**

```python
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
```

- [ ] **Step 2: 手动验证 loader**

```bash
python -c "from src.loader import load_csv, get_latest_month; df=load_csv('data/expenses.csv'); print(get_latest_month(df), len(df))"
```

Expected: `2026-05`（或样本数据最新月份）及行数约 42

- [ ] **Step 3: Commit**

```bash
git add src/loader.py
git commit -m "feat: add CSV loader with data cleaning"
```

---

## Task 6: 终端输出模块 display

**Files:**
- Create: `src/display.py`

- [ ] **Step 1: 实现 src/display.py**

```python
"""终端报告格式化输出。"""
from __future__ import annotations

import pandas as pd


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
    print(f"  {'分类':<8}{'金额':>12}  {'占比':>8}")
    print("  " + "─" * 29)
    if breakdown.empty:
        print("  （本月无支出）")
    else:
        for _, row in breakdown.iterrows():
            print(
                f"  {row['分类']:<8}"
                f"{format_currency(row['支出金额']):>12}  "
                f"{row['占比']:>8}"
            )
        total = breakdown["支出金额"].sum()
        print("  " + "─" * 29)
        print(f"  {'合计':<8}{format_currency(total):>12}  {'100.0%':>8}")
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
```

- [ ] **Step 2: Commit**

```bash
git add src/display.py
git commit -m "feat: add terminal report display module"
```

---

## Task 7: 导出模块 export

**Files:**
- Create: `src/export.py`

- [ ] **Step 1: 实现 src/export.py**

```python
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
```

- [ ] **Step 2: 手动验证导出**

```bash
python -c "
from src.loader import load_csv, get_latest_month
from src.stats import category_breakdown
from src.export import write_summary
df = load_csv('data/expenses.csv')
m = get_latest_month(df)
p = write_summary(category_breakdown(df, m), m, 'output')
print(p)
"
```

Expected: 打印 `output\summary_2026-05.csv`（或对应最新月）

- [ ] **Step 3: Commit**

```bash
git add src/export.py
git commit -m "feat: add CSV export for summary and detail"
```

---

## Task 8: 图表模块 chart

**Files:**
- Create: `src/chart.py`

- [ ] **Step 1: 实现 src/chart.py**

```python
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
```

- [ ] **Step 2: 手动验证图表**

```bash
python -c "from src.loader import load_csv; from src.chart import generate_charts; from src.loader import get_latest_month; df=load_csv('data/expenses.csv'); print(generate_charts(df, get_latest_month(df), 'output'))"
```

Expected: 生成 `output/pie_YYYY-MM.png` 和 `output/trend_3m.png`

- [ ] **Step 3: Commit**

```bash
git add src/chart.py
git commit -m "feat: add pie and line chart generation"
```

---

## Task 9: 串联 main.py 主流程

**Files:**
- Modify: `main.py`

- [ ] **Step 1: 替换 main.py 为完整实现**

```python
"""个人记账小助手 — CLI 入口。"""
import argparse
import re
import sys
from pathlib import Path

from src.chart import generate_charts
from src.display import print_report
from src.export import write_detail, write_summary
from src.loader import get_latest_month, load_csv
from src.stats import category_breakdown, monthly_overview, trend_3months


def parse_month(value: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}", value):
        raise argparse.ArgumentTypeError("月份格式须为 YYYY-MM，例如 2026-01")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="个人记账小助手：读取收支 CSV，生成统计报告"
    )
    parser.add_argument("--input", required=True, help="CSV 文件路径")
    parser.add_argument("--month", type=parse_month, help="分析月份 YYYY-MM，默认取最新月")
    parser.add_argument(
        "--export",
        choices=["summary", "detail"],
        default="summary",
        help="导出类型：summary（分类汇总）或 detail（原始明细）",
    )
    parser.add_argument("--output", default="output/", help="导出目录，默认 output/")
    parser.add_argument("--chart", action="store_true", help="生成饼图和折线图 PNG")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        df = load_csv(args.input)
    except FileNotFoundError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        sys.exit(1)

    month = args.month or get_latest_month(df)
    overview = monthly_overview(df, month)
    breakdown = category_breakdown(df, month)
    trend = trend_3months(df, month)

    export_paths: list[str] = []
    if args.export == "summary":
        path = write_summary(breakdown, month, args.output)
        export_paths.append(str(path))
    else:
        path = write_detail(df, month, args.output)
        export_paths.append(str(path))

    if args.chart:
        try:
            chart_paths = generate_charts(df, month, args.output)
            export_paths.extend(str(p) for p in chart_paths)
        except ImportError as exc:
            print(f"错误: {exc}", file=sys.stderr)
            sys.exit(1)

    print_report(overview, breakdown, trend, export_paths)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 端到端验证**

```bash
python main.py --input data/expenses.csv
python main.py --input data/expenses.csv --month 2026-01
python main.py --input data/expenses.csv --month 2026-01 --export detail
python main.py --input data/expenses.csv --month 2026-01 --chart
pytest tests/ -v
```

Expected:
- 终端打印三块报告（收支概览、分类明细、3 月趋势、导出提示）
- `output/` 下生成对应 CSV 和 PNG
- pytest 全部通过

- [ ] **Step 3: Commit**

```bash
git add main.py
git commit -m "feat: wire up CLI main flow end-to-end"
```

---

## Task 10: README 与最终验收

**Files:**
- Create: `README.md`

- [ ] **Step 1: 创建 README.md**

```markdown
# 个人记账小助手

读入收支 CSV，在终端展示当月收支全景与近 3 月趋势，支持汇总/明细导出，可选生成图表。

## 功能列表

1. 读取并清洗收支 CSV
2. 当月收支全景（收入、支出、结余）
3. 支出分类明细（金额 + 占比）
4. 近 3 个月支出趋势表（含环比）
5. 导出分类汇总 CSV（默认）或原始明细 CSV
6. 可选生成饼图 + 折线图 PNG（`--chart`）

## 环境要求

- Python 3.10+
- 依赖见 `requirements.txt`

## 安装步骤

```bash
git clone https://github.com/renjing-2022/Personal-Income.git
cd Personal-Income
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install pytest  # 可选，运行测试
```

## 运行示例

```bash
# 分析最新月份，终端打印报告，导出汇总 CSV
python main.py --input data/expenses.csv

# 指定月份 + 导出明细 + 生成图表
python main.py --input data/expenses.csv --month 2026-01 --export detail --chart
```

预期输出：终端显示收支概览、分类明细、3 月趋势，并在 `output/` 生成文件。

运行测试：

```bash
pytest tests/ -v
```

## 项目结构

| 文件 | 职责 |
|------|------|
| `main.py` | CLI 入口，流程编排 |
| `src/loader.py` | 读取 CSV、数据清洗 |
| `src/stats.py` | 统计计算（纯函数） |
| `src/display.py` | 终端格式化输出 |
| `src/export.py` | CSV 导出 |
| `src/chart.py` | matplotlib 图表 |
| `data/expenses.csv` | 样本数据 |
| `tests/test_stats.py` | 统计逻辑单元测试 |

## 实现方式

- 使用 **pandas** 做 CSV 读取、分组聚合、日期处理
- 使用 **argparse** 解析命令行参数
- 使用 **matplotlib Agg 后端** 生成无 GUI 依赖的 PNG 图表
- `stats.py` 采用纯函数设计，便于 pytest 单测
```

- [ ] **Step 2: 最终验收清单**

对照 design spec §1.3 成功标准逐项检查：

```bash
python main.py --input data/expenses.csv
python main.py --input data/expenses.csv --month 2026-01 --chart
pytest tests/ -v
ls output/
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add README with install and usage guide"
```

---

## Spec Coverage Self-Review

| Spec 要求 | 对应 Task |
|-----------|-----------|
| §2.1 读取 CSV + 清洗 | Task 5 loader |
| §2.1 当月收支全景 | Task 2 monthly_overview |
| §2.1 支出分类明细 | Task 3 category_breakdown |
| §2.1 近 3 月趋势 | Task 4 trend_3months |
| §2.1 终端格式化输出 | Task 6 display |
| §2.1 导出汇总/明细 | Task 7 export |
| §2.2 饼图 + 折线图 | Task 8 chart |
| §3 CLI 参数 | Task 1 + Task 9 main |
| §8 错误处理 | Task 5（文件不存在/无数据）+ Task 9（ImportError） |
| §9 测试 | Task 2–4 test_stats |
| §12 README | Task 10 |

无遗漏项。
