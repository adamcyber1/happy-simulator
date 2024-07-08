import logging
from typing import Callable

from happysimulator.entities.server import Server
from happysimulator.event import Event
from happysimulator.latency_distribution import LatencyDistribution

"""
A server whose latency increases as the concurrency increases. 
"""

logger = logging.getLogger(__name__)

class ConcurrencyLimitedServer(Server):
    def __init__(self, name: str, server_latency: LatencyDistribution, concurrency_penalty_func: Callable[[int], float]):
        super().__init__(name, server_latency)
        self._concurrency_penalty_func = concurrency_penalty_func
        self._baseline_latency = server_latency

    def start_request(self, request: Event) -> list[Event]:
        # adjust our latency for this request based on our concurrency
        self._latency = self._baseline_latency + self._concurrency_penalty_func(self._concurrent_requests)

        logger.info(f"[{request.time.to_seconds()}][{self.name}][{request.name}] Recomputed latency! Baseline: {self._baseline_latency._mean_latency} Mean is: {self._latency._mean_latency} because concurrency is {self._concurrent_requests}")

        return super().start_request(request)