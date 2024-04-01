from happysimulator.event import Event
from happysimulator.time import Time


class GenerateEvent(Event):
    def __init__(self, time: Time, callback, name: str):
        super().__init__(time, name, callback)
