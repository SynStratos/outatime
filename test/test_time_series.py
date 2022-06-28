import random
from copy import deepcopy, copy
from datetime import datetime, date

from outatime.dataclass.time_series_data import TimeSeriesData
from outatime.timeseries.time_series import TimeSeries
from test.utils import data_generation


def test_deepcopy():
    tsl = data_generation()
    x = deepcopy(tsl)
    assert id(x) != id(tsl), "Objects' identities are the same."


def test_copy():
    tsl = data_generation()
    x = tsl.copy()
    assert id(x) != id(tsl), "Objects' identities are the same."


def test_delitem():
    tsl = data_generation()
    idx = id(tsl[0])

    tsl.__delitem__(0)

    assert idx != id(tsl[0]), "Unexpected __delitem__ result."


def test_delete():
    tsl = data_generation()
    idx = id(tsl[0])

    date_to_del = copy(tsl[0].day)

    tsl.delete(date_to_del)

    assert idx != id(tsl[0]), "Unexpected delete result."


def test_add():
    tsl = data_generation(start_date='2021-06-01', end_date='2022-01-01')
    data = {'pippo': random.randint(200, 300), 'pluto': random.randint(200, 300)}
    days = [
        TimeSeriesData(day=date(2022, 12, 30), data=data),
        TimeSeriesData(day=date(2022, 12, 31), data=data)
    ]

    add_ts = tsl.__add__(days)
    assert add_ts.get(date(2022, 12, 30)).data and add_ts.get(date(2022, 12, 31)).data, "Unexpected __add__ result."


def test_update():
    tsl = data_generation(start_date='2021-06-01', end_date='2022-01-01')
    data = {'pippo': random.randint(200, 300), 'pluto': random.randint(200, 300)}
    days = [
        TimeSeriesData(day=date(2022, 12, 30), data=data),
        TimeSeriesData(day=date(2022, 12, 31), data=data)
    ]

    tsl.update(days)
    assert tsl.get(date(2022, 12, 30)).data and tsl.get(date(2022, 12, 31)).data, "Unexpected update result."


def test_cut():
    min_date = date(2020, 1, 11)
    max_date = date(2021, 1, 11)

    tsl = data_generation()
    y = tsl.cut(min_date=min_date, max_date=max_date, inplace=False)

    assert y[0].day == min_date, "Starting date is wrong."
    assert y[-1].day == max_date, "Ending date is wrong."
    assert tsl[0].day != min_date and tsl[-1].day != max_date, "Original time series changed."


def test_cut_inplace():
    min_date = date(2020, 1, 11)
    max_date = date(2021, 1, 11)

    tsl = data_generation()
    tsl.cut(min_date=min_date, max_date=max_date, inplace=True)

    assert tsl[0].day == min_date, "Starting date is wrong."
    assert tsl[-1].day == max_date, "Ending date is wrong."


def test_empty_timeseries():
    try:
        tsl = TimeSeries()
        assert len(tsl) == 0, "Unexpected length."
    except:
        raise AssertionError("Unable to create an empty time series.")


def test_single_element_timeseries():
    tsl = TimeSeries()
    try:
        data = {'pippo': random.randint(200, 300), 'pluto': random.randint(200, 300)}
        day = TimeSeriesData(day=date(2022, 1, 1), data=data)
        tsl.append(day)
    except:
        raise AssertionError("Unable to append a single element to empty time series.")
