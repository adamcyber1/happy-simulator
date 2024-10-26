** WORK IN PROGRESS **


# happy-simulator
Simulate systems in a few lines of Python code.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Quick Start
To configure logging, set your `HS_LOGGING` environment variable to `DEBUG`, `INFO`, `WARNING`, `ERROR`. Default is `INFO`.

## Examples 
See `examples/` folder for examples.

The following code simulates a congestive collapse scenario for a server with a queue, and generates CSV file and graphs:

```python
from happysimulator.arrival_distribution import ArrivalDistribution
from happysimulator.distribution.constant_latency import ConstantLatency
from happysimulator.entities.client import Client
from happysimulator.entities.queue import Queue
from happysimulator.entities.queued_server import QueuedServer
from happysimulator.events.client_server_request_event import Request
from happysimulator.generator import Generator
from happysimulator.measurement import Measurement
from happysimulator.profiles import ConstantProfile, SpikeProfile
from happysimulator.simulation import Simulation
from happysimulator.stat import Stat
from happysimulator.time import Time

SIMULATION_DURATION_SECONDS = 60
MEASUREMENT_PERIOD_SECONDS = 1

client = Client(name="Basic", retries=3, retry_delay=Time.from_seconds(0), timeout=Time.from_seconds(1.0))

queue = Queue(name="MyQueue", size=0) # adjust size to see how it impacts congestive collapse

failure_profile = SpikeProfile(rampup_start=Time.from_seconds(10),
                               rampdown_start=Time.from_seconds(15),
                               starting_rate=0.0,
                               rampup_factor=10,
                               rampdown_factor=10)

# Create a server with exponentially distributed service time
server = QueuedServer(name="Expo",
                server_latency=ConstantLatency(Time.from_seconds(0.1)),
                failure_rate=failure_profile,
                queue=queue)

network_latency = ConstantLatency(Time.from_seconds(0.0))

request_generator = Generator(func=lambda time: [Request(time=time, client=client, server=server, callback=client.send_request, network_latency=network_latency)],
                              profile=ConstantProfile(rate=10),
                              distribution=ArrivalDistribution.CONSTANT)

measurements = [
        Measurement(name="Client Request Count",
                    func=client.requests_count,
                    stats=[Stat.SUM],
                    interval=Time.from_seconds(MEASUREMENT_PERIOD_SECONDS)),
        Measurement(name="Client Failed Request Count",
                    func=client.failed_requests_count,
                    stats=[Stat.SUM],
                    interval=Time.from_seconds(MEASUREMENT_PERIOD_SECONDS)),
        Measurement(name="Client Successful Request Count",
                    func=client.successful_requests_count,
                    stats=[Stat.SUM],
                    interval=Time.from_seconds(MEASUREMENT_PERIOD_SECONDS)),
        Measurement(name="Client Latency",
                    func=client.requests_latency,
                    stats=[Stat.AVG],
                    interval=Time.from_seconds(MEASUREMENT_PERIOD_SECONDS)),
        Measurement(name="Queue Depth",
                    func=queue.depth,
                    stats=[Stat.AVG, Stat.P99, Stat.P0],
                    interval=Time.from_seconds(1))
    ]


result = Simulation(
    end_time=Time.from_seconds(SIMULATION_DURATION_SECONDS),
    generators=[request_generator],
    measurements=measurements
).run()

result.display_graphs()
result.print_csv()
```

## Development Plan
* Add oX and uX statistics (i.e. over X and under X)
* Add Server lambdas for arbitrarily complex server behavior
* Add Java ExecutorService pipeline simulation components and example
* Load balancer entity
* Retry explosion example 
* Full unit test coverage