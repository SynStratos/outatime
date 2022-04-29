import pickle
from datetime import date
from functools import cached_property
from typing import List

from ..dataclass.time_series_data import TimeSeriesData
from ..granularity.granularity import Granularity, DailyGranularity
from ..util.bisect import index_of, find_delimiters


def get_day(x):
    return x.day


class TimeSeries(List[TimeSeriesData]):
    """
    Class that inherits list to add useful methods for time series management.
    It contains only TimeSeriesData objects as elements.
    """
    data_granularity: Granularity

    def __init__(self, data=[], data_granularity: Granularity = DailyGranularity()):
        super().__init__(data)
        self.data_granularity = data_granularity
        self.__sort__()

    def __add__(self, other):
        super().__add__(other)
        self.__refresh()

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

    def __refresh(self):
        """Sort the timeseries by date and reset its properties."""
        self.__sort__()
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
            self[:] = self[idx_min:idx_max]
            self.__clear_cache()
        else:
            return self.__deepcopy__()[idx_min:idx_max]

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

    def resample(self,
                 granularity: Granularity = DailyGranularity(),
                 index_of_granularity: int = 0,
                 inplace: bool = False,
                 default_data: ... = None
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
            index_of_granularity (int, optional): The day of the time step
            to pick as reference (0-indexed). Defaults to 0.
            inplace (bool, optional): Original time series is overwritten
            if set to True. Defaults to False.
            default_data (None, optional): Data to store in days that
            can't be found. Defaults to None.
        """
        f_day = granularity.get_n_day_of_granularity(
            day=self.start_date,
            idx=index_of_granularity
        )
        resampled = []
        temp_ts = self.__deepcopy__()

        resampling_end_date = granularity.get_end_of_granularity(self.end_date)

        while f_day <= resampling_end_date:
            resampled.append(
                temp_ts.get(f_day, value=default_data)
            )
            f_day += granularity.delta
            f_day = granularity.get_n_day_of_granularity(
                day=f_day,
                idx=index_of_granularity
            )

        if inplace:
            self[:] = resampled
            self.data_granularity = granularity
        else:
            return self.__class__(resampled, data_granularity=granularity)

    def update(self, __list: List[TimeSeriesData]):
        """
        Add all elements of the given list of TimeSeriesData to the time series.
        Updates existing elements if already in the time series.

        Args:
            __list (List[TimeSeriesData]): Input list of new elements.
        """
        for new_element in __list:
            self.append(new_element)
