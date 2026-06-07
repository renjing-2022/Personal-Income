# 个人记账小助手 — 设计规范

> **日期**：2026-06-07  
> **课程**：Vibe Coding Class19 方向 C（数据处理小工具）  
> **时间预算**：3 小时（图表为 `--chart` 可选加分项）

---

## 1. 项目概述

### 1.1 一句话介绍

读入收支 CSV，在终端展示当月收支全景与近 3 月趋势，支持汇总/明细导出，可选生成图表。

### 1.2 目标用户

课程学员本人 — 需要一个能 clone 下来直接跑、能演示、能写进 README 的 GitHub 小项目。

### 1.3 成功标准

- [ ] `python main.py --input data/expenses.csv` 终端打印完整报告
- [ ] 默认导出 `output/summary_YYYY-MM.csv`
- [ ] `--chart` 生成饼图 + 折线图 PNG
- [ ] 仓库含 README、requirements.txt、.gitignore、样本数据、至少 1 个测试
- [ ] 别人 clone 后按 README 步骤能复现

---

## 2. 功能范围

### 2.1 MVP 功能（必做）

| # | 功能 | 说明 |
|---|------|------|
| 1 | 读取 CSV | 解析 `expenses.csv`，清洗无效行 |
| 2 | 当月收支全景 | 总收入、总支出、结余 |
| 3 | 支出分类明细 | 按分类汇总支出金额与占比，降序排列 |
| 4 | 近 3 月趋势表 | 以目标月为基准，向前取 3 个月总支出 + 环比 |
| 5 | 终端格式化输出 | 三块分区打印，含分隔线 |
| 6 | 导出汇总 CSV | 默认 `--export summary` |
| 7 | 导出明细 CSV | `--export detail` |

### 2.2 加分功能（时间允许）

| # | 功能 | 说明 |
|---|------|------|
| 8 | 分类支出饼图 | `--chart` 生成 `pie_YYYY-MM.png` |
| 9 | 3 月趋势折线图 | `--chart` 生成 `trend_3m.png` |

### 2.3 明确不做（YAGNI）

- 用户登录 / 数据库 / Web 界面
- 交互式录入账单
- 多 CSV 合并
- 预算预警、智能分类

---

## 3. 命令行接口

### 3.1 用法

```bash
# 最简运行（分析 CSV 最新月份，终端打印，导出汇总 CSV）
python main.py --input data/expenses.csv

# 指定月份
python main.py --input data/expenses.csv --month 2026-01

# 导出明细
python main.py --input data/expenses.csv --month 2026-01 --export detail

# 生成图表（加分项）
python main.py --input data/expenses.csv --month 2026-01 --chart

# 指定输出目录
python main.py --input data/expenses.csv --output output/
```

### 3.2 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--input` | 是 | — | CSV 文件路径 |
| `--month` | 否 | CSV 最新月份 | 格式 `YYYY-MM` |
| `--export` | 否 | `summary` | `summary`（分类汇总）或 `detail`（原始明细） |
| `--output` | 否 | `output/` | 导出文件和图表目录 |
| `--chart` | 否 | 不生成 | 生成饼图 + 折线图 PNG |

### 3.3 月份默认逻辑

1. 读取 CSV 全部有效行
2. 取 `日期` 列最大值所在月份作为「最新月份」
3. 用户传 `--month` 时覆盖默认值

---

## 4. 数据模型

### 4.1 输入 CSV 列定义

与现有 `expenses.csv` 一致：

| 列名 | 类型 | 说明 | 示例 |
|------|------|------|------|
| 日期 | date | `YYYY-MM-DD` | 2026-01-05 |
| 收支类型 | str | `收入` 或 `支出` | 支出 |
| 分类 | str | 自由文本 | 餐饮 |
| 金额 | float | 正数 | 68.0 |
| 备注 | str | 可空 | 家庭聚餐 |

### 4.2 数据清洗规则

| 规则 | 处理方式 |
|------|----------|
| 日期解析失败 | 跳过该行，`warnings.warn` 提示行号 |
| 金额 ≤ 0 或无法解析 | 跳过并警告 |
| 收支类型不是「收入」「支出」 | 跳过并警告 |
| 分类为空 | 归为「未分类」 |
| 重复行 | 保留（不去重） |

### 4.3 内部 DataFrame 计算列

```python
df["年月"] = df["日期"].dt.to_period("M")   # 如 2026-01
df["是收入"] = df["收支类型"] == "收入"
df["是支出"] = df["收支类型"] == "支出"
```

### 4.4 导出文件格式

**summary 模式** → `output/summary_YYYY-MM.csv`

```csv
分类,支出金额,占比
房租,1800.00,72.1%
购物,320.00,12.8%
```

**detail 模式** → `output/detail_YYYY-MM.csv`（该月原始记录，列与输入一致）

---

## 5. 终端输出格式

运行后终端分三块打印：

### 5.1 块 1 — 当月收支全景

```
══════════════════════════════════════
  个人记账小助手 · 2026-01 收支报告
══════════════════════════════════════

【收支概览】
  总收入：    ¥7,100.00
  总支出：    ¥2,498.00
  结余：      ¥4,602.00

【支出分类明细】
  分类        金额        占比
  ─────────────────────────────
  房租      ¥1,800.00    72.1%
  购物        ¥320.00    12.8%
  ...
  ─────────────────────────────
  合计      ¥2,498.00   100.0%
```

规则：
- 收入项只在「收支概览」汇总，不进分类明细表
- 分类明细只统计支出，按金额降序
- 金额为 0 的分类不显示

### 5.2 块 2 — 近 3 个月支出趋势

以 `--month` 指定月为基准，向前取 3 个月（含当月）：

```
【近 3 个月支出趋势】
  月份        总支出      环比变化
  ─────────────────────────────
  2025-11   ¥2,318.50        —
  2025-12   ¥2,795.00    +20.5%
  2026-01   ¥2,498.00    -10.6%
```

规则：
- 某月无数据时显示 `¥0.00`
- 首月环比显示 `—`
- 环比 = (本月 - 上月) / 上月 × 100%，上月为 0 时显示 `—`

### 5.3 块 3 — 导出提示

```
【导出完成】
  汇总表 → output/summary_2026-01.csv
```

若 `--chart`：

```
  饼图 → output/pie_2026-01.png
  折线图 → output/trend_3m.png
```

---

## 6. 模块架构

### 6.1 目录结构

```
Personal-Income/
├── README.md
├── requirements.txt          # pandas, matplotlib
├── .gitignore
├── main.py                   # CLI 入口，argparse 解析，调度各模块
├── data/
│   └── expenses.csv          # 样本数据
├── src/
│   ├── __init__.py
│   ├── loader.py             # 读 CSV、清洗、校验
│   ├── stats.py              # 收支汇总、分类统计、趋势计算
│   ├── export.py             # 写 summary / detail CSV
│   ├── chart.py              # 饼图 + 折线图（--chart 时才 import matplotlib）
│   └── display.py            # 格式化终端输出
├── output/                   # 运行时生成，.gitignore 忽略
└── tests/
    └── test_stats.py         # 核心统计逻辑测试
```

### 6.2 模块接口

```
main.py
  ├── loader.load_csv(path) → DataFrame
  ├── loader.get_latest_month(df) → "YYYY-MM"
  ├── stats.monthly_overview(df, month) → dict
  ├── stats.category_breakdown(df, month) → DataFrame
  ├── stats.trend_3months(df, month) → list[dict]
  ├── display.print_report(overview, breakdown, trend)
  ├── export.write_summary(breakdown, month, output_dir)
  ├── export.write_detail(df, month, output_dir)
  └── chart.generate(df, month, output_dir)   # 仅 --chart 时调用
```

### 6.3 数据流

```
expenses.csv → loader → stats ─┬→ display → 终端
                               ├→ export  → output/*.csv
                               └→ chart    → output/*.png
```

### 6.4 关键设计决策

- `chart.py` 延迟导入 `matplotlib`，避免不用 `--chart` 时强依赖图形后端
- `stats.py` 为纯函数、不依赖 I/O，方便单测
- `display.py` 只管格式化字符串，不含计算逻辑

---

## 7. 图表规范（加分项）

### 7.1 饼图 `pie_YYYY-MM.png`

- 数据：当月各分类支出金额
- 标题：`YYYY-MM 支出分类占比`
- 显示分类名 + 百分比
- 金额 < 5% 的分类合并为「其他」

### 7.2 折线图 `trend_3m.png`

- 数据：近 3 个月每月总支出
- X 轴：月份（YYYY-MM）
- Y 轴：总支出金额
- 标题：`近 3 个月支出趋势`
- 数据点标注金额

### 7.3 matplotlib 配置

- 使用 `matplotlib.use("Agg")` 后端（无 GUI 环境可运行）
- 中文字体：`SimHei` 或 `Microsoft YaHei`，设置 `axes.unicode_minus = False`

---

## 8. 错误处理

| 场景 | 行为 |
|------|------|
| `--input` 文件不存在 | 打印友好错误，exit code 1 |
| CSV 为空或全部行被清洗丢弃 | 打印「无有效数据」，exit code 1 |
| `--month` 格式错误（非 YYYY-MM） | argparse 校验失败，打印用法 |
| 指定月份无数据 | 正常输出，收支均为 ¥0.00 |
| `--chart` 但 matplotlib 未安装 | 捕获 ImportError，提示 `pip install matplotlib` |
| `output/` 目录不存在 | 自动创建 |

---

## 9. 测试

### 9.1 测试文件

`tests/test_stats.py` — 内存构造小 DataFrame，不依赖外部文件。

### 9.2 测试用例

| 用例 | 验证内容 |
|------|----------|
| `test_monthly_overview` | 收入/支出/结余计算正确 |
| `test_category_breakdown` | 分类汇总 + 占比正确 |
| `test_trend_3months` | 3 个月趋势 + 环比计算正确 |

### 9.3 运行方式

```bash
pip install pytest
pytest tests/ -v
```

---

## 10. 依赖

### requirements.txt

```
pandas>=2.0
matplotlib>=3.7
```

开发依赖（可选，不写入 requirements.txt）：

```
pytest>=7.0
```

### 环境要求

- Python 3.10+
- 无需数据库、API Key、Ollama

---

## 11. 分阶段实现计划

| 阶段 | 时间 | 目标 | 验证方式 |
|------|------|------|----------|
| **阶段 1** 骨架 | ~40 min | 目录、requirements.txt、main.py --help | `python main.py --help` |
| **阶段 2** 核心 | ~40 min | 读 CSV → 终端打印三块报告 | `python main.py --input data/expenses.csv` |
| **阶段 3** 完善 | ~40 min | 导出 + 图表 + README + .gitignore + 测试 | 全流程 + `pytest` |

---

## 12. README 要点（实现阶段撰写）

README 须包含课程要求的 6 块：

1. 项目名称 + 一句话介绍
2. 功能列表（与本文档 §2 一致）
3. 环境要求（Python 3.10+）
4. 安装步骤（`pip install -r requirements.txt`）
5. 运行示例（含预期输出截图）
6. 项目结构说明（各文件职责）

额外：附演示截图，说明主要功能 + 实现方式。
