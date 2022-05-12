from datetime import datetime

from outatime.granularity.granularity import MonthlyGranularity, QuarterlyGranularity, YearlyGranularity, \
    DailyGranularity
from outatime.timeseries.batches import aggregate
from outatime.util.relativedelta import relativedelta
from test.utils import data_generation


def take_first(list_):
    if list_:
        return list_[0]
    return None


def take_last(list_):
    if list_:
        return list_[-1]
    return None


def test_aggregate():
    tsl = data_generation()

    res = aggregate(tsl, granularity=MonthlyGranularity(), method=take_first)
    assert len(res) == 61, "Unexpected number of elements in resulting time series."

    expected_dates = [
        res[0].day == datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
        res[1].day == datetime.strptime("2020-02-01", "%Y-%m-%d").date(),
        res[-2].day == datetime.strptime("2024-12-01", "%Y-%m-%d").date(),
        res[-1].day == datetime.strptime("2025-01-01", "%Y-%m-%d").date()
    ]
    assert all(expected_dates), "Unexpected dates."

    expected_data = [
        res[0].data == tsl[0].data,
        res[1].data == tsl.get(datetime.strptime("2020-02-01", "%Y-%m-%d").date()).data,
        res[-2].data == tsl.get(datetime.strptime("2024-12-01", "%Y-%m-%d").date()).data,
        res[-1].data == tsl.get(datetime.strptime("2025-01-01", "%Y-%m-%d").date()).data,
    ]
    assert all(expected_data), "Unexpected results."


def test_aggregate_on_last():
    tsl = data_generation()

    res = aggregate(tsl, granularity=MonthlyGranularity(), method=take_last)
    assert len(res) == 61, "Unexpected number of elements in resulting time series."

    expected_dates = [
        res[0].day == datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
        res[1].day == datetime.strptime("2020-02-01", "%Y-%m-%d").date(),
        res[-2].day == datetime.strptime("2024-12-01", "%Y-%m-%d").date(),
        res[-1].day == datetime.strptime("2025-01-01", "%Y-%m-%d").date()
    ]
    assert all(expected_dates), "Unexpected dates."

    expected_data = [
        res[0].data == tsl.get(datetime.strptime("2020-01-31", "%Y-%m-%d").date()).data,
        res[1].data == tsl.get(datetime.strptime("2020-02-29", "%Y-%m-%d").date()).data,
        res[-2].data == tsl.get(datetime.strptime("2024-12-31", "%Y-%m-%d").date()).data,
        res[-1].data == tsl[-1].data
    ]
    assert all(expected_data), "Unexpected results."


def test_aggregate_indexed():
    tsl = data_generation()

    res = aggregate(tsl, granularity=MonthlyGranularity(), first_day_of_batch=5, last_day_of_batch=10, method=take_first)
    assert len(res) == 60, "Unexpected number of elements in resulting time series."

    expected_dates = [
        res[0].day == datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
        res[1].day == datetime.strptime("2020-02-01", "%Y-%m-%d").date(),
        res[-2].day == datetime.strptime("2024-11-01", "%Y-%m-%d").date(),
        res[-1].day == datetime.strptime("2024-12-01", "%Y-%m-%d").date()
    ]
    assert all(expected_dates), "Unexpected dates."

    expected_data = [
        res[0].data == tsl[0].data,
        res[1].data == tsl.get(datetime.strptime("2020-02-06", "%Y-%m-%d").date()).data,
        res[-2].data == tsl.get(datetime.strptime("2024-11-06", "%Y-%m-%d").date()).data,
        res[-1].data == tsl.get(datetime.strptime("2024-12-06", "%Y-%m-%d").date()).data,
    ]
    assert all(expected_data), "Unexpected results."


def test_aggregate_store_day():
    tsl = data_generation()

    res = aggregate(tsl, granularity=MonthlyGranularity(), method=take_first, store_day_of_batch=8)
    assert len(res) == 61, "Unexpected number of elements in resulting time series."

    expected_dates = [
        res[0].day == datetime.strptime("2020-01-09", "%Y-%m-%d").date(),
        res[1].day == datetime.strptime("2020-02-09", "%Y-%m-%d").date(),
        res[-2].day == datetime.strptime("2024-12-09", "%Y-%m-%d").date(),
        res[-1].day == datetime.strptime("2025-01-09", "%Y-%m-%d").date()
    ]
    assert all(expected_dates), "Unexpected dates."

    expected_data = [
        res[0].data == tsl[0].data,
        res[1].data == tsl.get(datetime.strptime("2020-02-01", "%Y-%m-%d").date()).data,
        res[-2].data == tsl.get(datetime.strptime("2024-12-01", "%Y-%m-%d").date()).data,
        res[-1].data == tsl.get(datetime.strptime("2025-01-01", "%Y-%m-%d").date()).data,
    ]
    assert all(expected_data), "Unexpected results."


def test_aggregate_drop_tails():
    tsl = data_generation()

    res = aggregate(tsl, granularity=MonthlyGranularity(), first_day_of_batch=5, last_day_of_batch=10, method=take_first, drop_tails=True)
    assert len(res) == 59, "Unexpected number of batches."

    expected_dates = [
        res[0].day == datetime.strptime("2020-02-01", "%Y-%m-%d").date(),
        res[1].day == datetime.strptime("2020-03-01", "%Y-%m-%d").date(),
        res[-2].day == datetime.strptime("2024-11-01", "%Y-%m-%d").date(),
        res[-1].day == datetime.strptime("2024-12-01", "%Y-%m-%d").date()
    ]
    assert all(expected_dates), "Unexpected dates."

    expected_data = [
        res[0].data == tsl.get(datetime.strptime("2020-02-06", "%Y-%m-%d").date()).data,
        res[1].data == tsl.get(datetime.strptime("2020-03-06", "%Y-%m-%d").date()).data,
        res[-2].data == tsl.get(datetime.strptime("2024-11-06", "%Y-%m-%d").date()).data,
        res[-1].data == tsl.get(datetime.strptime("2024-12-06", "%Y-%m-%d").date()).data,
    ]
    assert all(expected_data), "Unexpected results."


def test_aggregate_same_granularity():
    tsl = data_generation(start_date='2020-01-31', end_date='2020-12-31', step=relativedelta(months=1))
    res = aggregate(tsl, granularity=MonthlyGranularity(), first_day_of_batch=0, method=take_first)

    assert all(tsl_day.data == res_day.data for tsl_day, res_day in zip(tsl, res)), "Unexpected result content"


def test_aggregate_lower_granularity():
    tsl = data_generation(start_date='2020-01-31', end_date='2020-12-31', step=relativedelta(months=1))
    try:
        _ = aggregate(tsl, granularity=DailyGranularity(), first_day_of_batch=0, method=take_first)
        raise AssertionError("Exception not caught.")
    except AssertionError:
        pass
