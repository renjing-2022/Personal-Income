"""个人记账小助手 — CLI 入口。"""
import argparse
import re
import sys

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
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

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
