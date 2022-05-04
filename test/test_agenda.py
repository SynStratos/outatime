from outatime.util.agenda import *


def test_get_quarter():
    day = datetime.strptime("2020-01-07", "%Y-%m-%d").date()
    q = get_quarter(day)
    assert q == 1, "Wrong quarter returned, expected 1."
    day = datetime.strptime("2020-05-07", "%Y-%m-%d")
    q = get_quarter(day)
    assert q == 2, "Wrong quarter returned, expected 2."
    day = datetime.strptime("2020-08-07", "%Y-%m-%d")
    q = get_quarter(day)
    assert q == 3, "Wrong quarter returned, expected 3."
    day = datetime.strptime("2020-11-07", "%Y-%m-%d")
    q = get_quarter(day)
    assert q == 4, "Wrong quarter returned, expected 4."


def test_first_day_of_week():
    day = datetime.strptime("2020-01-07", "%Y-%m-%d").date()
    res = first_day_of_week(day)
    assert res == datetime.strptime("2020-01-06", "%Y-%m-%d").date(), "Wrong day returned."


def test_last_day_of_week():
    day = datetime.strptime("2020-01-07", "%Y-%m-%d").date()
    res = last_day_of_week(day)
    assert res == datetime.strptime("2020-01-12", "%Y-%m-%d").date(), "Wrong day returned."


def test_first_day_of_month():
    day = datetime.strptime("2020-01-07", "%Y-%m-%d").date()
    res = first_day_of_month(day)
    assert res == datetime.strptime("2020-01-01", "%Y-%m-%d").date(), "Wrong day returned."


def test_last_day_of_month():
    day = datetime.strptime("2020-01-07", "%Y-%m-%d").date()
    res = last_day_of_month(day)
    assert res == datetime.strptime("2020-01-31", "%Y-%m-%d").date(), "Wrong day returned."


def test_first_day_of_quarter():
    day = datetime.strptime("2020-01-07", "%Y-%m-%d").date()
    res = first_day_of_quarter(day)
    assert res == datetime.strptime("2020-01-01", "%Y-%m-%d").date(), "Wrong day returned."


def test_last_day_of_quarter():
    day = datetime.strptime("2020-01-07", "%Y-%m-%d").date()
    res = last_day_of_quarter(day)
    assert res == datetime.strptime("2020-03-31", "%Y-%m-%d").date(), "Wrong day returned."


def test_first_day_of_year():
    day = datetime.strptime("2020-01-07", "%Y-%m-%d").date()
    res = first_day_of_year(day)
    assert res == datetime.strptime("2020-01-01", "%Y-%m-%d").date(), "Wrong day returned."


def test_last_day_of_year():
    day = datetime.strptime("2020-01-07", "%Y-%m-%d").date()
    res = last_day_of_year(day)
    assert res == datetime.strptime("2020-12-31", "%Y-%m-%d").date(), "Wrong day returned."


def test_days_of_month():
    days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for month_n, month_days in enumerate(days):
        day = datetime.strptime(f"2020-{month_n+1}-07", "%Y-%m-%d").date()
        res = days_of_month(day)
        assert res == month_days, f"Wrong number of days in month {month_n+1}."


def test_days_of_quarter():
    day = datetime.strptime("2020-01-07", "%Y-%m-%d").date()
    res = days_of_quarter(day)
    assert res == 91, "Wrong number of days in quarter 1."

    day = datetime.strptime("2020-03-07", "%Y-%m-%d").date()
    res = days_of_quarter(day)
    assert res == 91, "Wrong number of days in quarter 2."

    day = datetime.strptime("2020-08-07", "%Y-%m-%d").date()
    res = days_of_quarter(day)
    assert res == 92, "Wrong number of days in quarter 3."

    day = datetime.strptime("2020-12-07", "%Y-%m-%d").date()
    res = days_of_quarter(day)
    assert res == 92, "Wrong number of days in quarter 3."


def test_days_of_year():
    day = datetime.strptime("2020-01-01", "%Y-%m-%d").date()
    res = days_of_year(day)
    assert res == 366, "Wrong number of days in leap year."

    day = datetime.strptime("2021-01-01", "%Y-%m-%d").date()
    res = days_of_year(day)
    assert res == 365, "Wrong number of days in normal year."


def test_is_business_day():
    day = datetime.strptime("2020-01-06", "%Y-%m-%d").date()
    assert is_business_day(day), "Expected a business day."

    day = datetime.strptime("2020-01-05", "%Y-%m-%d").date()
    assert not is_business_day(day), "Expected a week-end day."

    day = datetime.strptime("2020-12-25", "%Y-%m-%d").date()
    assert not is_business_day(day, holidays=[datetime.strptime("2020-12-25", "%Y-%m-%d").date()]), "Expected a holiday."


def test_weekdays_of_range():
    day_sx = datetime.strptime("2020-01-01", "%Y-%m-%d").date()
    day_dx = datetime.strptime("2020-01-31", "%Y-%m-%d").date()
    n_days, days = weekdays_of_range(day_sx, day_dx, 0)
    assert n_days == 4, "Unexpected number of mondays in given range."

    expected_days = [
        datetime.strptime("2020-01-06", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-13", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-20", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-27", "%Y-%m-%d").date()
    ]

    assert expected_days == days, "Unexpected days returned."


def test_calendar_by_steps():
    day_sx = datetime.strptime("2020-01-01", "%Y-%m-%d").date()
    day_dx = datetime.strptime("2020-01-10", "%Y-%m-%d").date()
    res = calendar_by_steps(day_sx, day_dx, step=relativedelta(days=2))

    expected_days = [
        datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-03", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-05", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-07", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-09", "%Y-%m-%d").date()
    ]
    assert expected_days == res, "Unexpected days returned."

    try:
        _ = calendar_by_steps(day_dx, day_sx, step=relativedelta(days=2))
        raise AssertionError("Inverted days exception not caught.")
    except AssertionError:
        pass
