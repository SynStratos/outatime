import pickle
from dataclasses import dataclass
from datetime import date


@dataclass
class TimeSeriesData:
    day: date
    data: ...

    def __deepcopy__(self, *args):
        return pickle.loads(pickle.dumps(self))
