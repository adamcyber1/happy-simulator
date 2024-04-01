from happysimulator.distribution.constant_latency import ConstantLatency
from happysimulator.event import Event
from happysimulator.latency_distribution import LatencyDistribution
from happysimulator.time import Time


class Request(Event):
    def __init__(self, time: Time, client: Client, server: Server, callback, name: str, network_latency: LatencyDistribution = ConstantLatency(Time.from_seconds(0.1))):
        super().__init__(time, name, callback)
        self.client = client
        self.server = server
        self.client_send_request_time = None
        self.server_receive_request_time = None
        self.server_send_response_time = None
        self.client_receive_response_time = None
        self.network_latency = network_latency