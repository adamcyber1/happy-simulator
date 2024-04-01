from happysimulator.arrival_distribution import ArrivalDistribution
from happysimulator.entities.Client import Client
from happysimulator.entities.Server import Server
from happysimulator.events.client_server_request_event import Request
from happysimulator.generator import Generator
from happysimulator.measurement import Measurement
from happysimulator.profiles import SinusoidProfile
from happysimulator.simulation import Simulation
from happysimulator.stat import Stat
from happysimulator.time import Time

client = Client(name="MyClient")
server = Server(name="MyServer")

profile = SinusoidProfile(shift=10, amplitude=5, period=Time.from_seconds(30))

request_generator = Generator(func=lambda time: [Request(time=time, client=client, server=server, callback=client.send_request)],
                              profile=profile,
                              distribution=ArrivalDistribution.POISSON)

result = Simulation(
    end_time=Time.from_seconds(120),
    generators=[request_generator],
    measurements=[
        Measurement(name="Client Request Count",
                    func=client.requests_count,
                    stats=[Stat.SUM],
                    interval=Time.from_seconds(1)),
    ]
).run()

result.display_graphs()