from outatime.granularity.granularity import *
from outatime.util.relativedelta import relativedelta

from test.utils import data_generation, compare


def resample_take_first(list_: list):
    if len(list_) > 0:
        return list_[0]
    else:
        return None


def test_resample_to_higher_granularity():
    tsl = data_generation(start_date='2020-01-01', end_date='2020-04-01', step=relativedelta(months=1))
    res = tsl.resample(granularity=WeeklyGranularity(), method=resample_take_first)
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
    assert compare(expected_res, res.dates), "Unexpected resample dates."
    assert res[0].data == tsl[0].data, "Unexpected resample data."
    assert res[1].data is None, "Unexpected resample data."
    assert not compare(expected_res, tsl.dates), "Original data changed."


def test_resample_to_higher_granularity_inplace():
    tsl = data_generation(start_date='2020-01-01', end_date='2020-04-01', step=relativedelta(months=1))
    tsl.resample(granularity=WeeklyGranularity(), inplace=True, method=resample_take_first)
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


def test_resample_to_lower_granularity():
    tsl = data_generation(start_date='2020-01-01', end_date='2020-02-01', step=relativedelta(days=1))
    res = tsl.resample(granularity=MonthlyGranularity(), method=resample_take_first)
    expected_res = [
        datetime.strptime('2020-01-01', '%Y-%m-%d').date(),
        datetime.strptime('2020-02-01', '%Y-%m-%d').date(),
    ]
    assert compare(expected_res, res.dates), "Unexpected resample dates."
    assert res[0].data == tsl[0].data, "Unexpected resample data."
    assert res[-1].data == tsl[-1].data, "Unexpected resample data."
    assert not compare(expected_res, tsl.dates), "Original data changed."


def test_resample_to_lower_granularity_inplace():
    tsl = data_generation(start_date='2020-01-01', end_date='2020-02-01', step=relativedelta(days=1))
    tsl.resample(granularity=MonthlyGranularity(), method=resample_take_first, inplace=True)
    expected_res = [
        datetime.strptime('2020-01-01', '%Y-%m-%d').date(),
        datetime.strptime('2020-02-01', '%Y-%m-%d').date(),
    ]
    assert compare(expected_res, tsl.dates), "Unexpected resample dates."


def test_resample_to_lower_granularity_no_method():
    tsl = data_generation(start_date='2020-01-01', end_date='2020-02-01', step=relativedelta(days=1))
    res = tsl.resample(granularity=MonthlyGranularity())
    expected_res = [
        datetime.strptime('2020-01-01', '%Y-%m-%d').date(),
        datetime.strptime('2020-02-01', '%Y-%m-%d').date(),
    ]
    assert compare(expected_res, res.dates), "Unexpected resample dates."
    assert res[0].data is None, "Unexpected resample data."
    assert res[-1].data is None, "Unexpected resample data."


def test_resample_bad_method():
    tsl = data_generation(start_date='2020-01-01', end_date='2020-02-01', step=relativedelta(days=1))
    try:
        _ = tsl.resample(granularity=MonthlyGranularity(), method=sum)
        raise AssertionError("Exception not caught.")
    except TypeError:
        pass
