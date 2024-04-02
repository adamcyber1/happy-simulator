from happysimulator.event import Event
from happysimulator.time import Time


class QueueEvent(Event):
    def __init__(self, time: Time, callback, name: str, queued_event, immediate_pop: bool):
        super().__init__(time, name, callback)
        self.queued_event = queued_event
        self.immediate_pop = immediate_pop