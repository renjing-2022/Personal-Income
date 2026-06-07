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
