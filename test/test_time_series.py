from copy import deepcopy
from datetime import datetime

from test.utils import data_generation


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
