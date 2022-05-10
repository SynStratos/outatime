from outatime.dataclass.time_series_data import TimeSeriesData
from outatime.granularity.granularity import *
from outatime.util.relativedelta import relativedelta
from test.utils import data_generation


def test_granularity_inference():
    tsl = data_generation(start_date='2020-01-01', end_date='2025-01-31', step=relativedelta(days=1))
    assert isinstance(tsl.data_granularity, DailyGranularity), "Expected DailyGranularity."

    tsl = data_generation(start_date='2020-01-06', end_date='2025-01-31', step=relativedelta(days=7))
    assert isinstance(tsl.data_granularity, WeeklyGranularity), "Expected WeeklyGranularity."

    tsl = data_generation(start_date='2020-01-01', end_date='2025-01-31', step=relativedelta(months=1))
    assert isinstance(tsl.data_granularity, MonthlyGranularity), "Expected MonthlyGranularity."

    tsl = data_generation(start_date='2020-01-01', end_date='2025-01-31', step=relativedelta(months=3))
    assert isinstance(tsl.data_granularity, QuarterlyGranularity), "Expected QuarterlyGranularity."

    tsl = data_generation(start_date='2020-01-01', end_date='2025-01-31', step=relativedelta(years=1))
    assert isinstance(tsl.data_granularity, YearlyGranularity), "Expected YearlyGranularity."


def test_granularity_after_insert():
    tsl = data_generation(start_date='2020-01-01', end_date='2021-01-01', step=relativedelta(months=1))
    assert isinstance(tsl.data_granularity, MonthlyGranularity), "Expected MonthlyGranularity."

    tsl.append(
        TimeSeriesData(
            day=datetime.strptime('2021-01-02', "%Y-%m-%d").date(),
            data={}
        )
    )

    assert isinstance(tsl.data_granularity, DailyGranularity), "Expected DailyGranularity after insertion."


def test_granularity_after_resample():
    tsl = data_generation(start_date='2020-01-01', end_date='2021-01-01', step=relativedelta(days=1))
    assert isinstance(tsl.data_granularity, DailyGranularity), "Expected DailyGranularity."

    tsl.resample(granularity=MonthlyGranularity(), inplace=True)
    assert isinstance(tsl.data_granularity, MonthlyGranularity), "Expected MonthlyGranularity after insertion."


def test_granularity_after_resample_reverse():
    tsl = data_generation(start_date='2020-01-01', end_date='2021-01-01', step=relativedelta(months=1))
    assert isinstance(tsl.data_granularity, MonthlyGranularity), "Expected MonthlyGranularity."

    tsl.resample(granularity=DailyGranularity(), inplace=True)
    assert isinstance(tsl.data_granularity, DailyGranularity), "Expected DailyGranularity after insertion."