
"""
A server with a queue. There is an extra step before requests are started: the work must go into a queue
"""
from happysimulator.entities.queue import Queue
from happysimulator.entities.server import Server
from happysimulator.event import Event
from happysimulator.events.queue_event import QueueEvent
from happysimulator.latency_distribution import LatencyDistribution


class QueuedServer(Server):
    def __init__(self, name: str, server_latency: LatencyDistribution, threads: int, queue: Queue):
        super().__init__(name, server_latency)
        self._baseline_latency = server_latency
        self._queue = queue
        self._threads = threads

    def start_request(self, request: Event) -> list[Event]:
        # instead of processing this request, put it in the queue.
        # If I currently have capacity, I will also schedule a queue Pop.
        print(f"[{request.time.to_seconds()}][{self.name}][{request.name}] Queued Server received request.")

        queued_event = request
        queued_event.callback = super().start_request # so that when we get this event back, we skip the queueing

        return [
            QueueEvent(name="QueuePut", time=request.time, callback=self._queue.put, queued_event=queued_event,
                       immediate_pop=self._concurrent_requests < self._threads)
        ]


    def done_request(self, request: Event) -> list[Event]:
        print(f"[{request.time.to_seconds()}][{self.name}][{request.name}] Queued Server completed request. Calling server.")

        events = super().done_request(request)

        if self._concurrent_requests < self._threads:
            # the server has capacity to start the next task
            events.append(Event(name="QueuePop", time=request.time, callback=self._queue.pop))

        return events