from datetime import datetime

from outatime.granularity.granularity import MonthlyGranularity
from outatime.timeseries.batches import pick_a_weekday
from test.utils import data_generation


def test_pick_a_weekday():
    tsl = data_generation()

    res = pick_a_weekday(
        ts=tsl,
        granularity=MonthlyGranularity(),
        day_of_batch=-1,
        weekday=0
    )
    assert len(res) == 60, "Unexpected number of elements in resulting time series."

    expected_dates = [
        res[0].day == datetime.strptime("2020-01-27", "%Y-%m-%d").date(),
        res[1].day == datetime.strptime("2020-02-24", "%Y-%m-%d").date(),
        res[-2].day == datetime.strptime("2024-11-25", "%Y-%m-%d").date(),
        res[-1].day == datetime.strptime("2024-12-30", "%Y-%m-%d").date()
    ]
    assert all(expected_dates), "Unexpected dates."

    assert all([day.weekday() == 0 for day in res.dates]), "Unexpected days of week in resulting time series."


def test_pick_a_weekday_first():
    tsl = data_generation()

    res = pick_a_weekday(
        ts=tsl,
        granularity=MonthlyGranularity(),
        day_of_batch=0,
        weekday=0
    )
    assert len(res) == 59, "Unexpected number of elements in resulting time series."

    expected_dates = [
        res[0].day == datetime.strptime("2020-02-03", "%Y-%m-%d").date(),
        res[1].day == datetime.strptime("2020-03-02", "%Y-%m-%d").date(),
        res[-2].day == datetime.strptime("2024-11-04", "%Y-%m-%d").date(),
        res[-1].day == datetime.strptime("2024-12-02", "%Y-%m-%d").date()
    ]
    assert all(expected_dates), "Unexpected dates."

    assert all([day.weekday() == 0 for day in res.dates]), "Unexpected days of week in resulting time series."


def test_pick_a_weekday_all_wds():
    tsl = data_generation()

    for i in range(7):
        res = pick_a_weekday(
            ts=tsl,
            granularity=MonthlyGranularity(),
            day_of_batch=0,
            weekday=i
        )
        assert all([day.weekday() == i for day in res.dates]), "Unexpected days of week in resulting time series."
