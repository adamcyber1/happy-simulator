from happysimulator.arrival_distribution import ArrivalDistribution
from happysimulator.entity import Entity
from happysimulator.event_heap import EventHeap
from happysimulator.events.generate_event import GenerateEvent
from happysimulator.events.measurement_event import MeasurementEvent
from happysimulator.generator import Generator
from happysimulator.measurement import Measurement
from happysimulator.profiles import ConstantProfile
from happysimulator.simulation_result import SimulationResult
from happysimulator.time import Time


def create_generators(measurements: list[Measurement], end_time):
    generators = []

    for measurement in measurements:

        # the default arg fixes outerscope issue: https://stackoverflow.com/questions/50298582/why-does-python-asyncio-loop-call-soon-overwrite-data
        def create_measurement_event_func(time: Time, measurement=measurement):
            return [MeasurementEvent(name=measurement.name, callback=measurement.func, time=time, interval=measurement.interval, stat=measurement.stat, sink=measurement.sinks)]

        generators.append(Generator(name=f"{measurement.name}_generator", end_time=end_time, func=create_measurement_event_func, distribution=ArrivalDistribution.CONSTANT, profile=ConstantProfile.from_period(measurement.interval)))

    return generators

class Simulation:
    def __init__(self, end_time: Time, entities: list[Entity], generators: list[Generator], measurements: list[Measurement]):
        self._end_time = end_time
        self._entities = entities
        self._generators = generators
        self._measurements = measurements


        self._measurement_generators = create_generators(measurements, end_time)

        self._event_heap = EventHeap(
            [item for generator in self._generators for item in generator.generate(event=GenerateEvent(time=Time.from_seconds(0), callback=None, name="BootstrapEvent"))] +
            [item for generator in self._measurement_generators for item in generator.generate(event=GenerateEvent(time=Time.from_seconds(0), callback=None, name="SecondBootstrappedEvent"))]
                                     )

    def run(self) -> SimulationResult:
        time = Time.from_seconds(0)

        while self._event_heap.has_events() and self._end_time > time:
            event = self._event_heap.pop() # heap is in descending order,
            time = event.time # moves time forward in the sim

            new_events = event.callback(event)

            # If the callback returned any new events, add them to the event queue `q` and make sure its still a valid heap
            if new_events is not None:
                self._event_heap.push(new_events)


        return SimulationResult(sinks=[sink for measurement in self._measurements for sink in measurement.sinks])

