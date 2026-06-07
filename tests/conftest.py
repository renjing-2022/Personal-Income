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
