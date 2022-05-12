import random
import time

from outatime.dataclass.time_series_data import TimeSeriesData
from outatime.granularity.granularity import *
from outatime.timeseries.time_series import TimeSeries

default_granularity_set = [YearlyGranularity, QuarterlyGranularity, MonthlyGranularity, WeeklyGranularity, DailyGranularity]


def data_generation(start_date='2020-01-07', end_date='2025-01-04', step=relativedelta(days=1), empty_data_step=2, empty_data={}, possible_granularity_list=default_granularity_set):
    z = []
    i = 0
    print("Generating input time series...")
    t = time.time()
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    while start_date <= end_date:
        i += 1
        data = empty_data
        if i % empty_data_step > 0:
            data = {'pippo': random.randint(200, 300), 'pluto': random.randint(200, 300)}
        day = TimeSeriesData(day=start_date, data=data)
        z.append(day)

        start_date += step

    tsl = TimeSeries(z, possible_granularity_list=possible_granularity_list)
    print(f"*** Executed in: {round(time.time() - t, 4)}s.")
    print("Done.")
    return tsl


def compare(expected_res, res) -> bool:
    return all([x == y for x, y in zip(res, expected_res)])
