from copy import deepcopy
from typing import List, Callable, Any
from ..dataclass.time_series_data import TimeSeriesData
from ..granularity.granularity import Granularity, WeeklyGranularity
from ..granularity.utils import get_first_available_beginning
from ..timeseries.time_series import TimeSeries
from ..util.bisect import *


def aggregate(
        ts: TimeSeries,
        method: Callable[[List[Any]], Any],
        granularity: Granularity = WeeklyGranularity(),
        first_day_of_batch: int = 0,
        last_day_of_batch: int = -1,
        drop_tails: bool = False,
        store_day_of_batch: int = 0,
) -> TimeSeries:
    """
    Divides the input time series in many sub-sets for each contained time step 
    of the given granularity. Then aggregates each sub-set data into a single 
    TimeSeriesData to generate a new TimeSeries output.

    Args:
        ts (TimeSeries): Input time series.
        granularity (Granularity, optional): Time step to use to divide the 
        input series. Defaults to WeeklyGranularity().
        method (Callable[[List[Any]], Any]): Aggregation function to apply.
        first_day_of_batch (int, optional): The day of the time step to use as
        first delimiter (0-indexed). Defaults to 0.
        last_day_of_batch (int, optional): The day of the time step to use as
        last delimiter (0-indexed). Defaults to -1.
        drop_tails (bool, optional): Choose to remove initial and final days if
        the granularity step is not complete.
        store_day_of_batch (int, optional): The day of the time step to store
        aggregated data into (0-indexed). Defaults to 0.

    Returns:
        TimeSeries: A new time series with aggregated values.
    """
    assert first_day_of_batch >= 0, "'first_day_of_batch' can't be lesser than 0."
    assert last_day_of_batch >= -1 and last_day_of_batch != 0, "'last_day_of_batch' can't be lesser than -1 or equal to 0."
    assert store_day_of_batch >= -1, "'store_day_of_batch' can't be lesser than -1."

    assert ts.data_granularity.delta <= granularity.delta, "Can't shrink the time series to a lower level granularity."

    res = []

    end_date = ts.end_date if drop_tails else granularity.get_end_of_granularity(ts.end_date)

    if drop_tails:
        start_date = get_first_available_beginning(
            day=ts.start_date,
            input_granularity=ts.data_granularity,
            output_granularity=granularity
        )
    else:
        start_date = ts.start_date

    batch_beginning = granularity.get_n_day_of_granularity(start_date, first_day_of_batch)
    batch_end = granularity.get_n_day_of_granularity(day=batch_beginning, idx=last_day_of_batch)

    temp_ts = deepcopy(ts)

    while batch_end <= end_date:
        reference_day = granularity.get_n_day_of_granularity(day=batch_beginning, idx=store_day_of_batch)

        idx_min, idx_max = find_delimiters(temp_ts.dates, batch_beginning, batch_end)

        subset = temp_ts[idx_min:idx_max+1]
        if len(subset) > 0:
            res.append(
                TimeSeriesData(
                    day=reference_day,
                    data=method([element.data for element in subset])
                )
            )

        temp_ts = temp_ts[idx_max+1:]
        batch_beginning += granularity.delta
        batch_beginning = granularity.get_n_day_of_granularity(batch_beginning, first_day_of_batch)
        batch_end = granularity.get_n_day_of_granularity(day=batch_beginning, idx=last_day_of_batch)

    return TimeSeries(res)


def pick_a_day(
        ts: TimeSeries,
        granularity: Granularity = WeeklyGranularity(),
        day_of_batch: int = -1,
        default=None,
) -> TimeSeries:
    """
    Divides the input time series in many sub-sets for each contained time step 
    of the given granularity. Then returns a new TimeSeries with only the n-th
    day of each batch.

    Args:
        ts (TimeSeries): Input time series.
        granularity (Granularity, optional): Time step to use to divide the 
        input series. Defaults to WeeklyGranularity().
        day_of_batch (int, optional): The day of the time step to retrieve
        (0-indexed). Defaults to -1.
        default (optional): Set a default value for missing days.
        Defaults to None.

    Returns:
        TimeSeries: A new time series with only a day for each step.
    """
    assert day_of_batch >= -1, "'day_of_batch' can't be lesser than -1."
    assert ts.data_granularity.delta <= granularity.delta, "Can't shrink the time series to a lower level granularity."

    res = []

    f_day = granularity.get_n_day_of_granularity(ts.start_date, day_of_batch)
    if f_day < ts.start_date:
        f_day += granularity.delta

    while f_day <= ts.end_date:
        res.append(
            deepcopy(ts.get(day=f_day, value=default))
        )

        f_day += granularity.delta
        f_day = granularity.get_n_day_of_granularity(f_day, day_of_batch)

    return TimeSeries(res)


def pick_a_weekday(
        ts: TimeSeries,
        granularity: Granularity = WeeklyGranularity(),
        day_of_batch: int = -1,
        weekday: int = 0,
        default=None,
) -> TimeSeries:
    """
    Divides the input time series in many sub-sets for each contained time step
    of the given granularity. Then returns a new TimeSeries with only the n-th 
    chosen day of the week of each batch.

    Args:
        ts (TimeSeries): Input time series.
        granularity (Granularity, optional): Time step to use to divide the
        input series. Defaults to WeeklyGranularity().
        day_of_batch (int, optional): The weekday of the time step to retrieve
        (0-indexed). Defaults to -1.
        weekday (int, optional): The day of the time step to use as
        first delimiter (1-indexed). Defaults to 1.
        default (optional): Set a default value for missing days.
        Defaults to None.

    Returns:
        TimeSeries: A new time series with only a day for each step.
    """
    assert day_of_batch >= -1, "'day_of_batch' can't be lesser than -1."
    assert ts.data_granularity.delta <= granularity.delta, "Can't shrink the time series to a lower level granularity."

    res = []
    f_day = granularity.get_n_weekday_of_granularity(day=ts.start_date, weekday=weekday, idx=day_of_batch)
    if f_day < ts.start_date:
        f_day = granularity.get_n_weekday_of_granularity(day=ts.start_date+granularity.delta, weekday=weekday, idx=day_of_batch)

    while f_day <= ts.end_date:
        res.append(
            deepcopy(ts.get(day=f_day, value=default))
        )

        f_day += granularity.delta
        f_day = granularity.get_n_weekday_of_granularity(day=f_day, weekday=weekday, idx=day_of_batch)

    return TimeSeries(res)


def split(
        ts: TimeSeries,
        granularity: Granularity = WeeklyGranularity(),
        first_day_of_batch: int = 0,
        last_day_of_batch: int = -1,
        drop_tails: bool = False
) -> List[TimeSeries]:
    """
    Divides the input time series in many sub-sets for each contained time step
    of the given granularity.

    Args:
        ts (TimeSeries): Input time series.
        granularity (Granularity, optional): Time step to use to divide the
        input series. Defaults to WeeklyGranularity().
        first_day_of_batch (int, optional): The day of the time step to use as
        first delimiter (0-indexed). Defaults to 0.
        last_day_of_batch (int, optional): The day of the time step to use as
        last delimiter (0-indexed). Defaults to -1.
        drop_tails (bool, optional): Choose to remove initial and final days if
        the granularity step is not complete.

    Returns:
        List[TimeSeries]: A list of smaller time series.
    """
    assert first_day_of_batch >= 0, "'first_day_of_batch' can't be lesser than 0."
    assert last_day_of_batch >= -1 and last_day_of_batch != 0, "'last_day_of_batch' can't be lesser than -1 or equal to 0."
    assert ts.data_granularity.delta <= granularity.delta, "Can't shrink the time series to a lower level granularity."

    res = []

    end_date = ts.end_date if drop_tails else granularity.get_end_of_granularity(ts.end_date)

    if drop_tails:
        start_date = get_first_available_beginning(
            day=ts.start_date,
            input_granularity=ts.data_granularity,
            output_granularity=granularity
        )
    else:
        start_date = ts.start_date

    batch_beginning = granularity.get_n_day_of_granularity(start_date, first_day_of_batch)
    batch_end = granularity.get_n_day_of_granularity(day=batch_beginning, idx=last_day_of_batch)

    temp_ts = deepcopy(ts)

    while batch_end <= end_date:
        idx_min, idx_max = find_delimiters(temp_ts.dates, batch_beginning, batch_end)

        subset = temp_ts[idx_min:idx_max+1]
        if len(subset) > 0:
            res.append(
                subset
            )

        temp_ts = temp_ts[idx_max+1:]
        batch_beginning += granularity.delta
        batch_beginning = granularity.get_n_day_of_granularity(batch_beginning, first_day_of_batch)
        batch_end = granularity.get_n_day_of_granularity(day=batch_beginning, idx=last_day_of_batch)

    return res
