from datetime import datetime


def day_or_datetime(func):
    """
    Decorator that transform a datetime object to a date object when it is 
    given as input to the decorated function.
    """
    def _check_if_datetime(day, *args, **kwargs):
        if isinstance(day, datetime):
            return func(day=day.date(), *args, **kwargs)
        return func(day=day,  *args, **kwargs)
    return _check_if_datetime
