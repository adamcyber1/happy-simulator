from happysimulator.arrival_distribution import ArrivalDistribution
from happysimulator.distribution.exponential_latency import ExponentialLatency
from happysimulator.entities.client import Client
from happysimulator.entities.concurrency_limited_server import ConcurrencyLimitedServer
from happysimulator.entities.queue import Queue
from happysimulator.entities.queued_server import QueuedServer
from happysimulator.events.client_server_request_event import Request
from happysimulator.generator import Generator
from happysimulator.measurement import Measurement
from happysimulator.profiles import SpikeProfile
from happysimulator.simulation import Simulation
from happysimulator.stat import Stat
from happysimulator.time import Time

SIMULATION_DURATION_SECONDS = 120
MEASUREMENT_PERIOD_SECONDS = 1

# Create a basic client - all this client does is send requests and get replies - no timeouts or retries or anything like that
client = Client(name="Basic")

queue = Queue(name="MyQueue")
server = QueuedServer(name="MyQueuedServer",
                      server_latency=ExponentialLatency(Time.from_seconds(0.5)),
                      threads=10,
                      queue=queue)

# define our network latency, in this case equal to our server latency, and also exponentially distributed
network_latency = ExponentialLatency(Time.from_seconds(0.5))

# create a generator profile which brings the simulation to life by telling the client to make requests to the server
# in this case, we send requests at a constant rate, then a spike of requests arrives, then we return
# to normal level.
profile = SpikeProfile(rampup_start=Time.from_seconds(30),
                       rampdown_start=Time.from_seconds(32),
                       starting_rate=20,
                       rampup_factor=50,
                       rampdown_factor=50)

request_generator = Generator(func=lambda time: [Request(time=time, client=client, server=server, callback=client.send_request, network_latency=network_latency)],
                              profile=profile,
                              distribution=ArrivalDistribution.POISSON)

# define what we want to measure in our simulation, and at what time-resolution
measurements = [
        Measurement(name="Client Request Count",
                    func=client.requests_count,
                    stats=[Stat.SUM],
                    interval=Time.from_seconds(MEASUREMENT_PERIOD_SECONDS)),
        Measurement(name="Client Request Latency",
                    func=client.requests_latency,
                    stats=[Stat.AVG],
                    interval=Time.from_seconds(MEASUREMENT_PERIOD_SECONDS)),
        Measurement(name="Server Latency",
                    func=server.requests_latency,
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
#result.print_csv()
#result.save_csvs(directory="/tmp/")