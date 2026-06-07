from src.stats import category_breakdown, monthly_overview


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
