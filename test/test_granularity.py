from datetime import date

from outatime.granularity.granularity import DailyGranularity, WeeklyGranularity, MonthlyGranularity, QuarterlyGranularity, YearlyGranularity


def test_yearly_granularity():
    g = YearlyGranularity()
    test_date = date(2022, 6, 28)

    first_day = g.get_beginning_of_granularity(test_date)
    assert first_day == date(2022, 1, 1), "Bad first day of granularity."

    last_day = g.get_end_of_granularity(test_date)
    assert last_day == date(2022, 12, 31), "Bad last day of granularity."

    n_day = g.get_n_day_of_granularity(test_date, 2)
    assert n_day == date(2022, 1, 3), "Bad n day of granularity."

    n_weekday = g.get_n_weekday_of_granularity(test_date, 2, 0)
    assert n_weekday == date(2022, 1, 5), "Bad n weekday of granularity."

    try:
        g.assert_included_day(date(2022, 6, 29), 5)
    except AssertionError:
        raise AssertionError("Bad result for assert included day.")

    try:
        g.assert_included_day(date(2022, 6, 29), 400)
        raise AssertionError("Bad result for assert included day.")
    except AssertionError:
        pass


def test_quarterly_granularity():
    g = QuarterlyGranularity()
    test_date = date(2022, 6, 28)

    first_day = g.get_beginning_of_granularity(test_date)
    assert first_day == date(2022, 4, 1), "Bad first day of granularity."

    last_day = g.get_end_of_granularity(test_date)
    assert last_day == date(2022, 6, 30), "Bad last day of granularity."

    n_day = g.get_n_day_of_granularity(test_date, 2)
    assert n_day == date(2022, 4, 3), "Bad n day of granularity."

    n_weekday = g.get_n_weekday_of_granularity(test_date, 2, -1)
    assert n_weekday == date(2022, 6, 29), "Bad n weekday of granularity."

    try:
        g.assert_included_day(date(2022, 6, 29), 5)
    except AssertionError:
        raise AssertionError("Bad result for assert included day.")

    try:
        g.assert_included_day(date(2022, 6, 29), 100)
        raise AssertionError("Bad result for assert included day.")
    except AssertionError:
        pass


def test_monthly_granularity():
    g = MonthlyGranularity()
    test_date = date(2022, 6, 28)

    first_day = g.get_beginning_of_granularity(test_date)
    assert first_day == date(2022, 6, 1), "Bad first day of granularity."

    last_day = g.get_end_of_granularity(test_date)
    assert last_day == date(2022, 6, 30), "Bad last day of granularity."

    n_day = g.get_n_day_of_granularity(test_date, 2)
    assert n_day == date(2022, 6, 3), "Bad n day of granularity."

    n_weekday = g.get_n_weekday_of_granularity(test_date, 2, 0)
    assert n_weekday == date(2022, 6, 1), "Bad n weekday of granularity."

    try:
        g.assert_included_day(date(2022, 6, 29), 5)
    except AssertionError:
        raise AssertionError("Bad result for assert included day.")

    try:
        g.assert_included_day(date(2022, 6, 29), 32)
        raise AssertionError("Bad result for assert included day.")
    except AssertionError:
        pass


def test_weekly_granularity():
    g = WeeklyGranularity()
    test_date = date(2022, 6, 28)

    first_day = g.get_beginning_of_granularity(test_date)
    assert first_day == date(2022, 6, 27), "Bad first day of granularity."

    last_day = g.get_end_of_granularity(test_date)
    assert last_day == date(2022, 7, 3), "Bad last day of granularity."

    n_day = g.get_n_day_of_granularity(test_date, 2)
    assert n_day == date(2022, 6, 29), "Bad n day of granularity."

    n_weekday = g.get_n_weekday_of_granularity(test_date, 2, 0)
    assert n_weekday == date(2022, 6, 29), "Bad n weekday of granularity."

    try:
        g.assert_included_day(date(2022, 6, 29), 5)
    except AssertionError:
        raise AssertionError("Bad result for assert included day.")

    try:
        g.assert_included_day(date(2022, 6, 29), 8)
        raise AssertionError("Bad result for assert included day.")
    except AssertionError:
        pass


def test_daily_granularity():
    g = DailyGranularity()
    test_date = date(2022, 6, 28)

    first_day = g.get_beginning_of_granularity(test_date)
    assert first_day == date(2022, 6, 28), "Bad first day of granularity."

    last_day = g.get_end_of_granularity(test_date)
    assert last_day == date(2022, 6, 28), "Bad first day of granularity."

    n_day = g.get_n_day_of_granularity(test_date, 0)
    assert n_day == date(2022, 6, 28), "Bad first day of granularity."

    try:
        _ = g.assert_included_day()
        raise AssertionError("Uncaught exception.")
    except AttributeError:
        pass

    try:
        _ = g.get_n_weekday_of_granularity()
        raise AssertionError("Uncaught exception.")
    except AttributeError:
        pass
