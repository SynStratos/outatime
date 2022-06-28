from outatime.granularity.granularity_factory import *


def test_granularity_factory_daily():
    gf = GranularityFactory()

    granularity = gf.get_granularity('D')
    assert granularity == DailyGranularity, "Unexpected granularity."

    granularity = gf.get_granularity('daily')
    assert granularity == DailyGranularity, "Unexpected granularity."


def test_granularity_factory_weekly():
    gf = GranularityFactory()

    granularity = gf.get_granularity('W')
    assert granularity == WeeklyGranularity, "Unexpected granularity."

    granularity = gf.get_granularity('weekly')
    assert granularity == WeeklyGranularity, "Unexpected granularity."


def test_granularity_factory_monthly():
    gf = GranularityFactory()

    granularity = gf.get_granularity('M')
    assert granularity == MonthlyGranularity, "Unexpected granularity."

    granularity = gf.get_granularity('monthly')
    assert granularity == MonthlyGranularity, "Unexpected granularity."


def test_granularity_factory_quarterly():
    gf = GranularityFactory()

    granularity = gf.get_granularity('Q')
    assert granularity == QuarterlyGranularity, "Unexpected granularity."

    granularity = gf.get_granularity('quarterly')
    assert granularity == QuarterlyGranularity, "Unexpected granularity."


def test_granularity_factory_yaerly():
    gf = GranularityFactory()

    granularity = gf.get_granularity('Y')
    assert granularity == YearlyGranularity, "Unexpected granularity."

    granularity = gf.get_granularity('yearly')
    assert granularity == YearlyGranularity, "Unexpected granularity."


def test_granularity_factory_bad_request():
    gf = GranularityFactory()

    try:
        _ = gf.get_granularity('bad')
        raise AssertionError("Uncaught exception.")
    except ValueError:
        pass
