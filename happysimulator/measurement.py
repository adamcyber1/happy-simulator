from typing import List, Callable, Union

import pandas as pd

from happysimulator.sinks.basic_sink import BasicSink
from happysimulator.stat import Stat
from happysimulator.time import Time


class Measurement:
    TIME_NANOS = 'time_nanos'
    STAT = 'stat'

    def __init__(self, name: str, func: Callable, stats: Union[Stat, list[Stat]], interval: Time):
        self.name = name
        self.func = func
        self.stat = stats
        self.interval = interval

        if isinstance(stats, Stat):
            self._dataframe = pd.DataFrame(columns=[self.TIME_NANOS, self.stat.name])
        elif isinstance(stats, List):
            self._dataframe = pd.DataFrame(columns=[self.TIME_NANOS] + [stat.name for stat in self.stat])


        self.sinks = [BasicSink(name=name, stat_names=[stat.name for stat in stats])]