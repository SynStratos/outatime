from outatime.dataclass.time_series_data import TimeSeriesData
from outatime.granularity.granularity import *
from ..util.bisect import *


def infer_ts_granularity(
        data: List[TimeSeriesData],
        granularity_list: list
):
    if len(data) < 2:
        return None

    granularity_list.sort(key=lambda gr: gr.delta, reverse=True)

    dates = [element.day for element in data]
    dates.sort()

    output_granularity: Granularity

    for granularity in granularity_list:
        g = granularity()
        f_day = g.get_beginning_of_granularity(dates[0])
        l_day = g.get_end_of_granularity(dates[-1])

        step_lengths = []
        while f_day <= l_day:
            step_l_day = g.get_end_of_granularity(f_day)
            low_d, high_d = find_delimiters(dates, f_day, step_l_day)
            batch = dates[low_d:high_d+1]
            step_lengths.append(len(batch))

            f_day += g.delta

        if max(step_lengths) == 1:
            output_granularity = g
            return output_granularity

    raise Exception("Unexpected granularity found in time series data.")
