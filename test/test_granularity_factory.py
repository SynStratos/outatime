from outatime.granularity.granularity_factory import *


def test_granularity_factory_daily():
    gf = GranularityFactory()

    granularity = gf.get_granularity('D')
    assert granularity == DailyGranularity, "Unxpected granularity"

    granularity = gf.get_granularity('daily')
    assert granularity == DailyGranularity, "Unxpected granularity"


def test_granularity_factory_weekly():
    gf = GranularityFactory()

    granularity = gf.get_granularity('W')
    assert granularity == WeeklyGranularity, "Unxpected granularity"

    granularity = gf.get_granularity('weekly')
    assert granularity == WeeklyGranularity, "Unxpected granularity"


def test_granularity_factory_monthly():
    gf = GranularityFactory()

    granularity = gf.get_granularity('M')
    assert granularity == MonthlyGranularity, "Unxpected granularity"

    granularity = gf.get_granularity('monthly')
    assert granularity == MonthlyGranularity, "Unxpected granularity"


def test_granularity_factory_quarterly():
    gf = GranularityFactory()

    granularity = gf.get_granularity('Q')
    assert granularity == QuarterlyGranularity, "Unxpected granularity"

    granularity = gf.get_granularity('quarterly')
    assert granularity == QuarterlyGranularity, "Unxpected granularity"


def test_granularity_factory_yaerly():
    gf = GranularityFactory()

    granularity = gf.get_granularity('Y')
    assert granularity == YearlyGranularity, "Unxpected granularity"

    granularity = gf.get_granularity('yearly')
    assert granularity == YearlyGranularity, "Unxpected granularity"