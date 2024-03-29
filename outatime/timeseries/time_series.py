import pickle
from datetime import date
from functools import cached_property
from typing import List, Callable, Any

from .filter_parser import FilterParserGenerator
from .inference import infer_ts_granularity
from ..dataclass.time_series_data import TimeSeriesData
from ..granularity.granularity import *
from ..util.bisect import index_of, find_delimiters


def get_day(x):
    return x.day


default_granularity_set = [YearlyGranularity, QuarterlyGranularity, MonthlyGranularity, WeeklyGranularity, DailyGranularity]


class TimeSeries(List[TimeSeriesData]):
    """
    Class that inherits list to add useful methods for time series management.
    It contains only TimeSeriesData objects as elements.
    """
    data_granularity: Granularity
    filter_parser = FilterParserGenerator().get_parser()
    possible_granularity_list = []

    def __init__(self,
                 data=None,
                 possible_granularity_list=None,
                 ):
        if possible_granularity_list is None:
            possible_granularity_list = default_granularity_set
        if data is None:
            data = []

        super().__init__(data)
        self.possible_granularity_list[:] = possible_granularity_list

        if len(data) > 1:
            self.__infer_data_granularity()
        else:
            self.data_granularity = None

    def __add__(self, other):
        ts = super(TimeSeries, self).__add__(other)
        return self.__class__(ts)

    def __deepcopy__(self, *args):
        return pickle.loads(pickle.dumps(self))

    def __delitem__(self, idx):
        super().__delitem__(idx)
        self.__refresh()

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__class__(super(TimeSeries, self).__getitem__(item))
        else:
            return super(TimeSeries, self).__getitem__(item)

    def __setitem__(self, key, value):
        super(TimeSeries, self).__setitem__(key, value)
        self.__refresh()

    def __sort__(self):
        """Sort the timeseries by date."""
        self.sort(key=get_day)

    def __clear_cache(self):
        """Clear all cached properties."""
        if hasattr(self, 'dates'):
            del self.dates

    def __infer_data_granularity(self):
        self.data_granularity = infer_ts_granularity(self, self.possible_granularity_list)

    def __refresh(self):
        """Sort the timeseries by date and reset its properties."""
        if self.__len__() > 1:
            self.__sort__()
            self.__infer_data_granularity()
        self.__clear_cache()

    @property
    def start_date(self) -> date:
        """First date of the time series."""
        return self[0].day

    @property
    def end_date(self) -> date:
        """Last date of the time series."""
        return self[-1].day

    @cached_property
    def dates(self):
        """List of all dates available in the time series."""
        return [data.day for data in self]

    def append(self, object_: TimeSeriesData):
        """Add a new TimeSeriesData object to the time series."""
        assert isinstance(object_, TimeSeriesData), "Only TimeSeriesData objects can be appended."
        try:
            self.delete(day=object_.day)
        except ValueError:
            pass
        finally:
            super(TimeSeries, self).append(object_)
            self.__refresh()

    def copy(self):
        """Return a deep copy of the list."""
        return self.__deepcopy__()

    def cut(self, min_date: date, max_date: date, inplace: bool = False):
        """
        Cut the time series selecting only the available days between the
        input delimiters.

        Args:
            min_date (date): Minimum date of range.
            max_date (date): Maximum date of range.
            inplace (bool, optional): Original time series is overwritten
            if set to True. Defaults to False.
        """
        idx_min, idx_max = find_delimiters(self.dates, min_date, max_date)

        if inplace:
            self[:] = self[idx_min:idx_max+1]
            self.__clear_cache()
        else:
            return self.__deepcopy__()[idx_min:idx_max+1]

    def delete(self, day: date):
        """Delete item by day."""
        idx = index_of(self.dates, day)
        self.__delitem__(idx)

    def get(self, day: date, value: ... = None) -> TimeSeriesData:
        """
        Search the time series element for the given day.

        Args:
            day (date): The day to search in the time series.
            value (None, optional): Give a default value to set as 'data' when
            the day is not found. Defaults to None.

        Returns:
            TimeSeriesData: A time series element for the searched day.
        """
        try:
            return self[index_of(self.dates, day)]
        except (KeyError, ValueError):
            return TimeSeriesData(day=day, data=value)

    def query(self, expr: str, inplace: bool = False):
        """
        Query the time series data with a boolean expression.

        Example:
            [TimeSeriesData(day=2022-01-14, data={'a': 1, 'b': 8}),
            TimeSeriesData(day=2022-02-16, data={'a': 3, 'b': 8}),
            TimeSeriesData(day=2022-03-16, data={'a': 3, 'b': 8}),
            TimeSeriesData(day=2022-04-16, data={'a': 3, 'b': 8})]

            expr = "month <= 2 and day < 20"

            Returns:
                [TimeSeriesData(day=2022-01-14, data={'a': 1, 'b': 8}),
                TimeSeriesData(day=2022-02-16, data={'a': 3, 'b': 8})]

        Args:
            expr (str): The query string to evaluate.
            inplace (bool, optional): Original time series is overwritten
            if set to True. Defaults to False.
        """
        query_filter, _ = self.filter_parser(expr)
        filtered = filter(lambda x: query_filter(x), self)
        filtered_ts = list(filtered)

        if inplace:
            self[:] = filtered_ts
        else:
            return self.__class__(filtered_ts)

    def resample(self,
                 granularity: Granularity = DailyGranularity(),
                 method: Callable[[List[Any]], Any] = None,
                 index_of_granularity: int = 0,
                 inplace: bool = False,
                 ):
        """
        Select only needed days for the given granularity.
        If a day is missing, create a new TimeSeriesData with empty series.

        Example:
            [TimeSeriesData(day=2022-04-14, data={'a': 1, 'b': 8}),
            TimeSeriesData(day=2022-04-16, data={'a': 3, 'b': 8})]

            granularity = DailyGranularity()

            Returns:
                [TimeSeriesData(day=2022-04-14, data={'a': 1, 'b': 8}),
                TimeSeriesData(day=2022-04-15, data=None),
                TimeSeriesData(day=2022-04-16, data={'a': 3, 'b': 8})]

        Args:
            granularity (Granularity, optional): Time step to use for
            selecting ranges. Defaults to DailyGranularity().
            method (Callable[[List[Any]], Any], optional): Method to
            apply when evaluating the value of data for a time step.
            Defaults to None.
            index_of_granularity (int, optional): The day of the time step
            to pick as reference (0-indexed). Defaults to 0.
            inplace (bool, optional): Original time series is overwritten
            if set to True. Defaults to False.
        """
        resampled = []
        temp_ts = self.__deepcopy__()

        resampling_end_date = granularity.get_end_of_granularity(self.end_date)

        step_first_day = granularity.get_beginning_of_granularity(day=self.start_date)
        step_last_day = granularity.get_end_of_granularity(day=step_first_day)

        while step_last_day <= resampling_end_date:
            day = granularity.get_n_day_of_granularity(day=step_first_day, idx=index_of_granularity)

            idx_min, idx_max = find_delimiters(temp_ts.dates, step_first_day, step_last_day)
            subset = temp_ts[idx_min:idx_max + 1]

            data = method([element.data for element in subset]) if method else None

            resampled.append(
                TimeSeriesData(
                    day=day,
                    data=data
                )
            )

            temp_ts = temp_ts[idx_max + 1:]
            step_first_day += granularity.delta
            step_last_day = granularity.get_end_of_granularity(day=step_first_day)

        if inplace:
            self[:] = resampled
            self.data_granularity = granularity
        else:
            return self.__class__(resampled, possible_granularity_list=self.possible_granularity_list)

    def update(self, __list: List[TimeSeriesData]):
        """
        Add all elements of the given list of TimeSeriesData to the time series.
        Updates existing elements if already in the time series.

        Args:
            __list (List[TimeSeriesData]): Input list of new elements.
        """
        res_ts_data = super(TimeSeries, self).__add__(__list)
        self[:] = res_ts_data
