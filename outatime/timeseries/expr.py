from ..dataclass.time_series_data import TimeSeriesData
from ..timeseries.time_series import TimeSeries


def take_first_available(a, b):
    if all([a, b]):
        return a
    elif b:
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

    Returns:
        TimeSeries: Output timeseries with shared days.
    """
    intersection_dates = tsl_a.dates and tsl_b.dates
    res = []
    for int_date in intersection_dates:
        res.append(
            TimeSeriesData(
                day=int_date,
                data=conflict_method(tsl_a.get(day=int_date).data, tsl_b.get(day=int_date).data)
            )
        )
    return TimeSeries(res)


def union(tsl_a: TimeSeries, tsl_b: TimeSeries, conflict_method=take_first_available) -> TimeSeries:
    """
    Given two input time series, generates a new time series with the union of 
    all days of both series.

    Args:
        tsl_a (TimeSeries): First input time series.
        tsl_b (TimeSeries): Second input time series.

    Returns:
        TimeSeries: Output timeseries with all days.
    """
    union_dates = tsl_a.dates or tsl_b.dates
    res = []
    for int_date in union_dates:
        res.append(
            TimeSeriesData(
                day=int_date,
                data=conflict_method(tsl_a.get(day=int_date).data, tsl_b.get(day=int_date).data)
            )
        )
    return TimeSeries(res)
