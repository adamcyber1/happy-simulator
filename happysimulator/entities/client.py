import logging
from typing import Optional

from happysimulator.data import Data
from happysimulator.entity import Entity
from happysimulator.event import Event
from happysimulator.events.measurement_event import MeasurementEvent
from happysimulator.time import Time

logger = logging.getLogger(__name__)

class Client(Entity):
    def __init__(self, name: str, timeout: Optional[Time] = None):
        super().__init__(name)

        self._timeout = timeout
        self._requests_count = Data()
        self._successful_requests_count = Data()
        self._failed_requests_count = Data()

        self._requests_latency = Data()
        self._responses = Data()

    def send_request(self, request: Event) -> list[Event]:
        logger.info(f"[{request.time.to_seconds()}][{self.name}][{request.name}] Client sending request")
        self._requests_count.add_stat(1, request.time)

        request.client_send_request_time = request.time
        request.callback = request.server.start_request
        request.time = request.time + request.network_latency.get_latency(request.time)

        return [request]

    def receive_response(self, request: Event) -> list[Event]:
        latency = (request.time - request.client_send_request_time).to_seconds()

        logger.info(f"[{request.time.to_seconds()}][{self.name}][{request.name}] Client received response after {latency} seconds")
        self._responses.add_stat(1, request.time)

        if latency > self._timeout.to_seconds():
            self._failed_requests_count.add_stat(1, request.time)
        else:
            self._successful_requests_count.add_stat(1, request.time)

        self._requests_latency.add_stat(latency, request.time)

        return [] # no further action needed for this request

    def requests_stats(self, event: MeasurementEvent) -> list[Event]:
        logger.info(f"[{event.time.to_seconds()}][{self.name}][{event.name}] Received measurement event for requests_stats.")

        self.sink_data(self._requests_count, event) # TODO implement all of the above and below logic

        return [] # measurement events don't generate additional events

    def requests_latency(self, event: MeasurementEvent) -> list[Event]:
        logger.info(f"[{event.time.to_seconds()}][{self.name}][{event.name}] Received measurement event for request latency")

        self.sink_data(self._requests_latency, event)

    def requests_count(self, event: MeasurementEvent) -> list[Event]:
        logger.info(f"[{event.time.to_seconds()}][{self.name}][{event.name}] Received measurement event for request count")

        self.sink_data(self._requests_count, event)

    def successful_requests_count(self, event: MeasurementEvent) -> list[Event]:
        logger.info(f"[{event.time.to_seconds()}][{self.name}][{event.name}] Received measurement event for successful request count")

        self.sink_data(self._successful_requests_count, event)

    def failed_requests_count(self, event: MeasurementEvent) -> list[Event]:
        logger.info(f"[{event.time.to_seconds()}][{self.name}][{event.name}] Received measurement event for failed request count")

        self.sink_data(self._failed_requests_count, event)