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
