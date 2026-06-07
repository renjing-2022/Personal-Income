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
