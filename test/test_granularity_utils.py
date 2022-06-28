from outatime.granularity.granularity import *
from outatime.granularity.utils import get_first_available_beginning


def test_get_first_available_beginning_higher_granularity():
    input_granularity = DailyGranularity()
    output_granularity = MonthlyGranularity()

    day = datetime.fromisoformat('2020-01-01').date()
    res_day = get_first_available_beginning(
        input_granularity, output_granularity, day
    )

    assert res_day == day, "Unexpected first available beginning date."

    day = datetime.fromisoformat('2020-01-31').date()
    res_day = get_first_available_beginning(
        input_granularity, output_granularity, day
    )
    assert res_day == datetime.fromisoformat('2020-02-01').date(), "Unexpected first available beginning date."


def test_get_first_available_beginning_equal_granularity():
    input_granularity = MonthlyGranularity()
    output_granularity = MonthlyGranularity()

    day = datetime.fromisoformat('2020-01-01').date()
    res_day = get_first_available_beginning(
        input_granularity, output_granularity, day
    )

    assert res_day == day, "Unexpected first available beginning date."

    day = datetime.fromisoformat('2020-01-31').date()
    res_day = get_first_available_beginning(
        input_granularity, output_granularity, day
    )
    assert res_day == datetime.fromisoformat('2020-01-01').date(), "Unexpected first available beginning date."


def test_get_first_available_beginning_lower_granularity():
    input_granularity = MonthlyGranularity()
    output_granularity = DailyGranularity()

    day = datetime.fromisoformat('2020-01-01').date()
    try:
        _ = get_first_available_beginning(
            input_granularity, output_granularity, day
        )
        raise AssertionError("Uncaught exception.")
    except TypeError:
        pass
