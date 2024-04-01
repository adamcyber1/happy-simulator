from happysimulator.data import Data
from happysimulator.entity import Entity
from happysimulator.event import Event
from happysimulator.events.measurement_event import MeasurementEvent


class Client(Entity):
    def __init__(self, name: str):
        super().__init__(name)
        self._requests_count = Data()
        self._requests_latency = Data()
        self._responses = Data()

    def send_request(self, request: Event) -> list[Event]:
        print(f"[{request.time.to_seconds()}][{self.name}][{request.name}] Client sending request")
        self._requests_count.add_stat(1, request.time)

        request.client_send_request_time = request.time
        request.callback = request.server.start_request
        request.time = request.time + request.network_latency.get_latency(request.time)

        return [request]

    def receive_response(self, request: Event) -> list[Event]:
        print(f"[{request.time.to_seconds()}][{self.name}][{request.name}] Client received response")
        self._responses.add_stat(1, request.time)
        self._requests_latency.add_stat((request.time - request.client_send_request_time).to_seconds(), request.time)

        return [] # no further action needed for this request

    def requests_stats(self, event: MeasurementEvent) -> list[Event]:
        print(f"[{event.time.to_seconds()}][{self.name}][{event.name}] Received measurement event for requests_stats.")

        self.sink_data(self._requests_count, event) # TODO implement all of the above and below logic

        return [] # measurement events don't generate additional events

    def requests_latency(self, event: MeasurementEvent) -> list[Event]:
        print(f"[{event.time.to_seconds()}][{self.name}][{event.name}] Received measurement event for request latency")

        self.sink_data(self._requests_latency, event)

    def requests_count(self, event: MeasurementEvent) -> list[Event]:
        print(f"[{event.time.to_seconds()}][{self.name}][{event.name}] Received measurement event for request count")

        self.sink_data(self._requests_count, event)