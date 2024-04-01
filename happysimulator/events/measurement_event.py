from typing import Union, List

from happysimulator.datasink import DataSink
from happysimulator.event import Event
from happysimulator.stat import Stat
from happysimulator.time import Time


class MeasurementEvent(Event):
    def __init__(self, time: Time, callback, name: str, stat: Union[Stat, List[Stat]], interval: Time, sink: list[DataSink]):
        super().__init__(time, name, callback)
        self.stat = stat
        self.interval = interval
        self.sink = sink