from happysimulator.arrival_distribution import ArrivalDistribution
from happysimulator.distribution.constant_latency import ConstantLatency
from happysimulator.distribution.exponential_latency import ExponentialLatency
from happysimulator.entities.Client import Client
from happysimulator.entities.Server import Server
from happysimulator.events.client_server_request_event import Request
from happysimulator.generator import Generator
from happysimulator.measurement import Measurement
from happysimulator.profiles import SinusoidProfile
from happysimulator.simulation import Simulation
from happysimulator.stat import Stat
from happysimulator.time import Time

SIMULATION_DURATION_SECONDS = 120
MEASUREMENT_PERIOD_SECONDS = 1

# Create a basic client - all this client does is send requests and get replies - no timeouts or retries or anything like that
client = Client(name="MyClient")

# Create a server with exponentially distributed service time
server = Server(name="Expo", server_latency=ExponentialLatency(Time.from_seconds(0.5)))

# create a generator profile which brings the simulation to life by telling the client to make requests to the server
# in this case, with a varying rated defined by a sinusoid, and exponentially distributed requests
request_generator = Generator(func=lambda time: [Request(time=time, client=client, server=server, callback=client.send_request)],
                              profile=SinusoidProfile(shift=10, amplitude=5, period=Time.from_seconds(30)),
                              distribution=ArrivalDistribution.POISSON)

# define what we want to measure in our simulation, and at what time-resolution
measurements = [
        Measurement(name="Client Request Count",
                    func=client.requests_count,
                    stats=[Stat.SUM],
                    interval=Time.from_seconds(MEASUREMENT_PERIOD_SECONDS)),
        Measurement(name="Client Request Latency",
                    func=client.requests_latency,
                    stats=[Stat.AVG, Stat.P99, Stat.P0],
                    interval=Time.from_seconds(MEASUREMENT_PERIOD_SECONDS)),
        Measurement(name="Server Latency",
                    func=server.requests_latency,
                    stats=[Stat.AVG, Stat.P99, Stat.P0],
                    interval=Time.from_seconds(MEASUREMENT_PERIOD_SECONDS))
    ]


result = Simulation(
    end_time=Time.from_seconds(SIMULATION_DURATION_SECONDS),
    generators=[request_generator],
    measurements=measurements
).run()

result.display_graphs()
result.print_csv()
result.save_csvs(directory="/tmp/")