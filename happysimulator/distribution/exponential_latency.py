import random

from happysimulator.latency_distribution import LatencyDistribution
from happysimulator.time import Time


class ExponentialLatency(LatencyDistribution):
    def __init__(self, mean_latency: Time):
        super().__init__(mean_latency)
        self._lambda = 1 / self._mean_latency

    def get_latency(self, current_time: Time) -> Time:
        return Time.from_seconds(random.expovariate(self._lambda))