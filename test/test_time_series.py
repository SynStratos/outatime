from copy import deepcopy
from datetime import datetime

from outatime.granularity.granularity import MonthlyGranularity, WeeklyGranularity
from outatime.util.relativedelta import relativedelta

from test.utils import data_generation, compare


def test_deepcopy():
    tsl = data_generation()
    x = deepcopy(tsl)
    assert id(x) != id(tsl), "Objects' identities are the same."


def test_cut():
    min_date = datetime.strptime("2020-01-11", "%Y-%m-%d").date()
    max_date = datetime.strptime("2021-01-11", "%Y-%m-%d").date()

    tsl = data_generation()
    y = tsl.cut(min_date=min_date, max_date=max_date, inplace=False)

    assert y[0].day == min_date, "Starting date is wrong."
    assert y[-1].day == max_date, "Ending date is wrong."
    assert tsl[0].day != min_date and tsl[-1].day != max_date, "Original time series changed."


def test_cut_inplace():
    min_date = datetime.strptime("2020-01-11", "%Y-%m-%d").date()
    max_date = datetime.strptime("2021-01-11", "%Y-%m-%d").date()

    tsl = data_generation()
    tsl.cut(min_date=min_date, max_date=max_date, inplace=True)

    assert tsl[0].day == min_date, "Starting date is wrong."
    assert tsl[-1].day == max_date, "Ending date is wrong."


def test_resample():
    tsl = data_generation(start_date='2020-01-01', end_date='2020-04-01', step=relativedelta(months=1))
    res = tsl.resample(granularity=WeeklyGranularity())
    expected_res = [
        datetime.strptime('2019-12-30', '%Y-%m-%d').date(),
        datetime.strptime('2020-01-06', '%Y-%m-%d').date(),
        datetime.strptime('2020-01-13', '%Y-%m-%d').date(),
        datetime.strptime('2020-01-20', '%Y-%m-%d').date(),
        datetime.strptime('2020-01-27', '%Y-%m-%d').date(),
        datetime.strptime('2020-02-03', '%Y-%m-%d').date(),
        datetime.strptime('2020-02-10', '%Y-%m-%d').date(),
        datetime.strptime('2020-02-17', '%Y-%m-%d').date(),
        datetime.strptime('2020-02-24', '%Y-%m-%d').date(),
        datetime.strptime('2020-03-02', '%Y-%m-%d').date(),
        datetime.strptime('2020-03-09', '%Y-%m-%d').date(),
        datetime.strptime('2020-03-16', '%Y-%m-%d').date(),
        datetime.strptime('2020-03-23', '%Y-%m-%d').date(),
        datetime.strptime('2020-03-30', '%Y-%m-%d').date(),
    ]
    assert compare(expected_res, res.dates), "Unexpected resample result."
    assert not compare(expected_res, tsl.dates), "Original data changed."


def test_resample_inplace():
    tsl = data_generation(start_date='2020-01-01', end_date='2020-04-01', step=relativedelta(months=1))
    tsl.resample(granularity=WeeklyGranularity(), inplace=True)
    expected_res = [
        datetime.strptime('2019-12-30', '%Y-%m-%d').date(),
        datetime.strptime('2020-01-06', '%Y-%m-%d').date(),
        datetime.strptime('2020-01-13', '%Y-%m-%d').date(),
        datetime.strptime('2020-01-20', '%Y-%m-%d').date(),
        datetime.strptime('2020-01-27', '%Y-%m-%d').date(),
        datetime.strptime('2020-02-03', '%Y-%m-%d').date(),
        datetime.strptime('2020-02-10', '%Y-%m-%d').date(),
        datetime.strptime('2020-02-17', '%Y-%m-%d').date(),
        datetime.strptime('2020-02-24', '%Y-%m-%d').date(),
        datetime.strptime('2020-03-02', '%Y-%m-%d').date(),
        datetime.strptime('2020-03-09', '%Y-%m-%d').date(),
        datetime.strptime('2020-03-16', '%Y-%m-%d').date(),
        datetime.strptime('2020-03-23', '%Y-%m-%d').date(),
        datetime.strptime('2020-03-30', '%Y-%m-%d').date(),
    ]
    assert compare(expected_res, tsl.dates), "Unexpected resample result."
