import logging

from happysimulator.data import Data
from happysimulator.distribution.constant_latency import ConstantLatency
from happysimulator.entity import Entity
from happysimulator.event import Event
from happysimulator.events.measurement_event import MeasurementEvent
from happysimulator.latency_distribution import LatencyDistribution
from happysimulator.time import Time

logger = logging.getLogger(__name__)

class Server(Entity):
    def __init__(self, name: str, server_latency: LatencyDistribution = ConstantLatency(Time.from_seconds(0.1))):
        super().__init__(name)
        self._latency = server_latency
        self._requests_count = Data()
        self._requests_finished_count = Data()
        self._responses_count = Data()
        self._server_side_latency = Data()
        self._concurrent_requests = 0

    def start_request(self, request: Event) -> list[Event]:
        logger.info(f"[{request.time.to_seconds()}][{self.name}][{request.name}] Server started request")
        self._requests_count.add_stat(1, request.time)
        self._concurrent_requests += 1
        request.server_receive_request_time = request.time

        request.callback = self.done_request
        request.time = request.time + self._latency.get_latency(request.time)

        return [request]

    def done_request(self, request: Event) -> list[Event]:
        logger.info(f"[{request.time.to_seconds()}][{self.name}][{request.name}] Server completed request")
        self._requests_finished_count.add_stat(1, request.time)
        self._concurrent_requests -= 1
        request.server_send_response_time = request.time
        self._server_side_latency.add_stat((request.time - request.server_receive_request_time).to_seconds(),  request.time)

        request.callback = request.client.receive_response
        request.time = request.time + request.network_latency.get_latency(request.time)

        return [request]

    def concurrency_stats(self, event: MeasurementEvent) -> list[Event]:
        logger.info(f"[{event.time.to_seconds()}][{self.name}][{event.name}] Server measurement event for concurrency_stats.")
        self.sink_data(self._concurrent_requests, event)
        return []

    def requests_latency(self, event: MeasurementEvent) -> list[Event]:
        logger.info(f"[{event.time.to_seconds()}][{self.name}][{event.name}] Received measurement event for request latency")

        self.sink_data(self._server_side_latency, event)

    def requests_count(self, event: MeasurementEvent) -> list[Event]:
        logger.info(f"[{event.time.to_seconds()}][{self.name}][{event.name}] Received measurement event for request count")

        self.sink_data(self._requests_count, event)