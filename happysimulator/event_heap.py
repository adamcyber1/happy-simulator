import heapq
from typing import Union

from happysimulator.event import Event


# TODO if event implements a comparison operator using time(), then there is no need to have time on the heap as well as a separate object
class EventHeap:
    def __init__(self, events: list[Event]):
        self._heap = [(event.time, event) for event in events] # need to use a tuple with first entry of time
        heapq.heapify(self._heap)

    def push(self, events: Union[Event, list[Event]]):
        # Pushes an event onto the heap, using its time as the comparison key
        if isinstance(events, Event):
            heapq.heappush(self._heap, (events.time, events))
        elif isinstance(events, list):
            for event in events:
                heapq.heappush(self._heap, (event.time, event))

        heapq.heapify(self._heap) # added events, re-heapify

    def pop(self) -> Event:
        # Pops the event with the smallest time off the heap
        _, event = heapq.heappop(self._heap)
        return event

    def peek(self) -> Event:
        # Peeks at the event with the smallest time without removing it
        _, event = self._heap[0]
        return event

    def has_events(self) -> bool:
        return len(self._heap) > 0