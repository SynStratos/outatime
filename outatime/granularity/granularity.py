from datetime import date
from abc import abstractmethod, ABC

from ..util.agenda import *
from ..util.relativedelta import relativedelta

assertion_err_msg = "Given number exceeds the time range limit."


class Granularity(ABC):
    """
    Abstract class used to manage time ranges of different lengths.
    """
    delta: relativedelta

    @abstractmethod
    def get_beginning_of_granularity(self, day: date) -> date:
        """
        Move the given date to the beginning of its granularity period.

        Example:
            (with a Monthly granularity)
            day = 2022-04-16
            returns 2022-04-01

        Args:
            day (date): Input date.

        Returns:
            date: First day of the granularity step.
        """
        pass

    @abstractmethod
    def get_end_of_granularity(self, day: date) -> date:
        """
        Move the given date to the end of its granularity period.

        Example:
            (with a Monthly granularity)
            day = 2022-04-16
            returns 2022-04-30

        Args:
            day (date): Input date.

        Returns:
            date: Last day of the granularity step.
        """
        pass

    @abstractmethod
    def assert_included_day(self, day: date, days: int):
        """
        Checks if a range of days is included in the number of days of 
        the granularity step for the given day.

        Args:
            day (date): Reference day for the granularity step.
            days (int): Number of the days to check.
        """
        pass

    def get_n_day_of_granularity(self, day: date, idx: int) -> date:
        """
        Move the given date to N-th day of its granularity period.

        Example:
            (with a Monthly granularity)
            day = 2022-04-16
            n = 8
            returns 2022-04-08

        Args:
            day (date): Input date.
            idx (int): Number of the day to retrieve (0-indexed).

        Returns:
            date: N-th day of the granularity step.
        """
        self.assert_included_day(day=day, days=idx)
        if idx == -1:
            return self.get_end_of_granularity(day)
        return self.get_beginning_of_granularity(day) + relativedelta(days=idx)

    def get_n_weekday_of_granularity(self, day: date, weekday: int, idx: int) -> date:
        """
        Move the given date to N-th required day of the week of its granularity 
        period.

        Example:
            (with Monthly Granularity)
            day: 2020-04-19
            weekday: 3 (Wednesday)
            idx: 2 (the 3rd one starting from zero)

            returns 2020-04-20 (the 3rd Wednesday of the month)

        Args:
            day (date): Input date.
            weekday (int): Number of the day of the week (0-indexed).
            idx (int): Number of the day to retrieve (0-indexed).

        Returns:
            date: N-th day of the week of the granularity step.
        """
        assert 0 <= weekday <= 6, "Weekday must be between 0 and 6."
        first_day = self.get_beginning_of_granularity(day)
        last_day = self.get_end_of_granularity(day)
        n_days, days = weekdays_of_range(first_day, last_day, weekday)
        assert -1 <= idx < n_days, "Index must be between -1 and the total number of the specific weekday in the granularity."
        return days[idx]


class YearlyGranularity(Granularity):

    delta = relativedelta(months=12)

    def get_beginning_of_granularity(self, day: date) -> date:
        return first_day_of_year(day)

    def get_end_of_granularity(self, day: date) -> date:
        return last_day_of_year(day)

    def assert_included_day(self, day: date, days: int):
        assert -1 <= days < days_of_year(day), assertion_err_msg


class QuarterlyGranularity(Granularity):

    delta = relativedelta(months=3)

    def get_beginning_of_granularity(self, day: date) -> date:
        return first_day_of_quarter(day)

    def get_end_of_granularity(self, day: date) -> date:
        return last_day_of_quarter(day)

    def assert_included_day(self, day: date, days: int):
        assert -1 <= days < days_of_quarter(day), assertion_err_msg


class MonthlyGranularity(Granularity):

    delta = relativedelta(months=1)

    def get_beginning_of_granularity(self, day: date) -> date:
        return first_day_of_month(day)

    def get_end_of_granularity(self, day: date) -> date:
        return last_day_of_month(day)

    def assert_included_day(self, day: date, days: int):
        assert -1 <= days < days_of_month(day), assertion_err_msg


class WeeklyGranularity(Granularity):

    delta = relativedelta(weeks=1)

    def get_beginning_of_granularity(self, day: date) -> date:
        return first_day_of_week(day)

    def get_end_of_granularity(self, day: date) -> date:
        return last_day_of_week(day)

    def assert_included_day(self, day: date, days: int):
        assert -1 <= days < 7, assertion_err_msg


class DailyGranularity(Granularity):

    delta = relativedelta(days=1)

    def assert_included_day(self, *args, **kwargs):
        raise AttributeError("Not available method for Daily Granularity.")

    def get_n_weekday_of_granularity(self, *args, **kwargs):
        raise AttributeError("Not available method for Daily Granularity.")

    def get_n_day_of_granularity(self, day: date, *args, **kwargs) -> date:
        return day

    def get_beginning_of_granularity(self, day: date) -> date:
        return day

    def get_end_of_granularity(self, day: date) -> date:
        return day
