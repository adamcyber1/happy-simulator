from typing import Callable

from happysimulator import ArrivalDistribution
from happysimulator.event import Event
from happysimulator.events.GenerateEvent import GenerateEvent
from happysimulator.profile import Profile
from happysimulator.time import Time

"""
Generators are only approximate because events are what generate the next event, so if your dynamic rate 
function ever has a rate of 0 - the next event never comes. There are ways to fix this, but usually generators
are generating a lot of events anyways so I haven't seen a reason to improve this yet.

As one idea, we could pre-populate the event heap with events (not great for memory)
Another idea, we could have another internal generator that re-evaluates the rate every N milliseconds.
"""
class Generator:
    def __init__(self, end_time: Time, func: Callable[[Time], list[Event]], profile: Profile, distribution: ArrivalDistribution, name: str):
        self._func = func
        self._profile = profile
        self._distribution = distribution
        self._end_time = end_time
        self._nmb_events = 0
        self._name = name # TODO generate this name using profile and distribution

    def generate(self, event: GenerateEvent) -> list[Event]:
        print(f"[{event.time.to_seconds()}][{event.name}] Generating event")

        rate_per_second = self._profile.get_rate(event.time)
        next_generate_time = self._distribution.get_next_arrival_time(event.time, rate_per_second)

        # the first event is the event this generator generates, the second event is the next load gen event.
        ret = [*self._func(event.time), GenerateEvent(time=next_generate_time, callback=self.generate, name=f"{self._name}_{self._nmb_events}")]
        self._nmb_events += 1
        return ret

    def name(self):
        return self._name