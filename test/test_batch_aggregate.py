from datetime import datetime

from outatime.granularity.granularity import MonthlyGranularity
from outatime.timeseries.batches import aggregate
from test.utils import data_generation


def take_first(_list):
    if _list:
        return _list[0]
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