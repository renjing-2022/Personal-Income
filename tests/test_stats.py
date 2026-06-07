from src.stats import category_breakdown, monthly_overview, trend_3months


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
