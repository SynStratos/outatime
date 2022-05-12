from datetime import datetime

from outatime.granularity.granularity import MonthlyGranularity
from outatime.timeseries.batches import split
from outatime.util.relativedelta import relativedelta
from test.utils import data_generation


def test_split():
    tsl = data_generation()
    res = split(tsl, granularity=MonthlyGranularity())
    assert len(res) == 61, "Unexpected number of batches."
    expected_dates = [
        res[0][0].day == datetime.strptime("2020-01-07", "%Y-%m-%d").date(),
        res[0][-1].day == datetime.strptime("2020-01-31", "%Y-%m-%d").date(),
        res[-1][0].day == datetime.strptime("2025-01-01", "%Y-%m-%d").date(),
        res[-1][-1].day == datetime.strptime("2025-01-04", "%Y-%m-%d").date()
    ]
    assert all(expected_dates), "Unexpected dates."


def test_split_indexed():
    tsl = data_generation()
    res = split(tsl, granularity=MonthlyGranularity(), first_day_of_batch=5, last_day_of_batch=10,)
    assert len(res) == 60, "Unexpected number of batches."
    expected_dates = [
        res[0][0].day == datetime.strptime("2020-01-07", "%Y-%m-%d").date(),
        res[0][-1].day == datetime.strptime("2020-01-11", "%Y-%m-%d").date(),
        res[-1][0].day == datetime.strptime("2024-12-06", "%Y-%m-%d").date(),
        res[-1][-1].day == datetime.strptime("2024-12-11", "%Y-%m-%d").date()
    ]
    assert all(expected_dates), "Unexpected dates."


def test_split_drop_tails():
    tsl = data_generation()
    res = split(tsl, granularity=MonthlyGranularity(), drop_tails=True)
    assert len(res) == 59, "Unexpected number of batches."
    expected_dates = [
        res[0][0].day == datetime.strptime("2020-02-01", "%Y-%m-%d").date(),
        res[0][-1].day == datetime.strptime("2020-02-29", "%Y-%m-%d").date(),
        res[-1][0].day == datetime.strptime("2024-12-01", "%Y-%m-%d").date(),
        res[-1][-1].day == datetime.strptime("2024-12-31", "%Y-%m-%d").date()
    ]
    assert all(expected_dates), "Unexpected dates."


def test_split_lower_granularity():
    tsl = data_generation(start_date='2020-01-31', end_date='2020-12-31', step=relativedelta(months=1))
    try:
        _ = split(tsl, granularity=MonthlyGranularity())
        raise AssertionError("Exception not caught.")
    except AssertionError:
        pass
