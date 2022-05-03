from ..dataclass.time_series_data import TimeSeriesData
from ..timeseries.time_series import TimeSeries


def take_first_available(a, b):
    if a is not None:
        return a
    elif b is not None:
        return b
    else:
        raise Exception("Both arguments are None.")


def intersection(tsl_a: TimeSeries, tsl_b: TimeSeries, conflict_method=take_first_available) -> TimeSeries:
    """
    Given two input time series, generates a new time series with only shared 
    days and all the contained values.

    Args:
        tsl_a (TimeSeries): First input time series.
        tsl_b (TimeSeries): Second input time series.
        conflict_method (None, optional): Method to apply when choosing
        data for matching days. Defaults to take_first_available.

    Returns:
        TimeSeries: Output timeseries with shared days.
    """
    intersection_dates = list(set(tsl_a.dates) & set(tsl_b.dates))
    intersection_dates.sort()
    intersection_result = []
    for int_date in intersection_dates:
        intersection_result.append(
            TimeSeriesData(
                day=int_date,
                data=conflict_method(tsl_a.get(day=int_date).data, tsl_b.get(day=int_date).data)
            )
        )
    return TimeSeries(intersection_result)


def union(tsl_a: TimeSeries, tsl_b: TimeSeries, conflict_method=take_first_available) -> TimeSeries:
    """
    Given two input time series, generates a new time series with the union of 
    all days of both series.

    Args:
        tsl_a (TimeSeries): First input time series.
        tsl_b (TimeSeries): Second input time series.
        conflict_method (None, optional): Method to apply when choosing
        data for matching days. Defaults to take_first_available.

    Returns:
        TimeSeries: Output timeseries with all days.
    """
    union_dates = list(set(tsl_a.dates) | set(tsl_b.dates))
    union_dates.sort()
    union_result = []
    for uni_date in union_dates:
        union_result.append(
            TimeSeriesData(
                day=uni_date,
                data=conflict_method(tsl_a.get(day=uni_date).data, tsl_b.get(day=uni_date).data)
            )
        )
    return TimeSeries(union_result)
