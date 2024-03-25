from abc import ABC
from typing import Union

from .data import Data


class Entity(ABC):
    def __init__(self, name):
        self.name = name

    def sink_data(self, data: Union[Data, float, int], event):
        for sink in event.sink:
            if isinstance(data, Data):
                if isinstance(event.stat, list):  # Handling multiple stats
                    stats = {}
                    for stat in event.stat:
                        stats[stat.name] = data.get_stats(begin=event.time - event.interval, end=event.time,
                                                    aggregator=stat)
                    sink.add_stat(event.time, stats)
                else:  # Handling a single stat
                    stats = data.get_stats(begin=event.time - event.interval, end=event.time,
                                           aggregator=event.stat)
                    sink.add_stat(event.time, stats)
            elif isinstance(data, (float, int)):
                if isinstance(event.stat, list) and len(event.stat) > 1:
                    raise RuntimeError("A single data value provided but multiple stat names are defined in the event.")
                else:
                    sink.add_stat(event.time, float(data))
            else:
                raise RuntimeError("Unsupported data type submitted to data_sink.")

