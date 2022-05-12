from outatime.dataclass.time_series_data import TimeSeriesData
from outatime.granularity.granularity import *
from outatime.timeseries.time_series import TimeSeries
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


def test_granularity_inference_after_insert():
    tsl = data_generation(start_date='2020-01-01', end_date='2021-01-01', step=relativedelta(months=1))
    assert isinstance(tsl.data_granularity, MonthlyGranularity), "Expected MonthlyGranularity."

    tsl.append(
        TimeSeriesData(
            day=datetime.strptime('2021-01-02', "%Y-%m-%d").date(),
            data={}
        )
    )

    assert isinstance(tsl.data_granularity, DailyGranularity), "Expected DailyGranularity after insertion."


def test_granularity_inference_after_resample():
    tsl = data_generation(start_date='2020-01-01', end_date='2021-01-01', step=relativedelta(days=1))
    assert isinstance(tsl.data_granularity, DailyGranularity), "Expected DailyGranularity."

    tsl.resample(granularity=MonthlyGranularity(), inplace=True)
    assert isinstance(tsl.data_granularity, MonthlyGranularity), "Expected MonthlyGranularity after insertion."


def test_granularity_inference_after_resample_reverse():
    tsl = data_generation(start_date='2020-01-01', end_date='2021-01-01', step=relativedelta(months=1))
    assert isinstance(tsl.data_granularity, MonthlyGranularity), "Expected MonthlyGranularity."

    tsl.resample(granularity=DailyGranularity(), inplace=True)
    assert isinstance(tsl.data_granularity, DailyGranularity), "Expected DailyGranularity after insertion."


def test_granularity_inference_irregular_steps():
    tsl = TimeSeries(
        [
            TimeSeriesData(day=datetime.strptime('2020-01-31', "%Y-%m-%d").date(), data={}),
            TimeSeriesData(day=datetime.strptime('2020-02-01', "%Y-%m-%d").date(), data={}),
            TimeSeriesData(day=datetime.strptime('2020-03-15', "%Y-%m-%d").date(), data={}),
            TimeSeriesData(day=datetime.strptime('2020-04-01', "%Y-%m-%d").date(), data={}),
        ]
    )
    assert isinstance(tsl.data_granularity, MonthlyGranularity), "Expected MonthlyGranularity."


def test_granularity_inference_custom_granularity():
    class TwoYearGranularity(Granularity):
        delta = relativedelta(years=2)

        def get_beginning_of_granularity(self, day: date) -> date:
            year = day.year
            year -= year % 4
            day.replace(year=year)
            return day

        def get_end_of_granularity(self, day: date) -> date:
            year = day.year + 4
            year -= year % 4
            day.replace(year=year)
            return day

        def assert_included_day(self, day: date, days: int):
            assert -1 <= days < 365*4 + 1, assertion_err_msg

    granularity_set = [
        TwoYearGranularity,
        YearlyGranularity,
        QuarterlyGranularity,
        MonthlyGranularity,
        WeeklyGranularity,
        DailyGranularity
    ]
    tsl = data_generation(
        start_date='2010-01-01',
        end_date='2025-01-31',
        step=relativedelta(years=2),
        possible_granularity_list=granularity_set
    )
    assert isinstance(tsl.data_granularity, TwoYearGranularity), "Expected custom TwoYearGranularity."


def test_granularity_inference_missing_granularity():
    granularity_set = [YearlyGranularity, QuarterlyGranularity, WeeklyGranularity, DailyGranularity]
    tsl = data_generation(
        start_date='2010-01-01',
        end_date='2025-01-31',
        step=relativedelta(months=1),
        possible_granularity_list=granularity_set
    )
    assert isinstance(tsl.data_granularity, WeeklyGranularity), "Expected WeeklyGranularity because missing MonthlyGranularity."
