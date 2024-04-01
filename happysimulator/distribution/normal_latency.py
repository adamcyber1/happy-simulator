import random

from happysimulator.latency_distribution import LatencyDistribution
from happysimulator.time import Time


class NormalLatency(LatencyDistribution):
    def __init__(self, mean_latency: Time, std_dev: Time):
        super().__init__(mean_latency)
        self._std_dev = std_dev.to_seconds()

    def get_latency(self, current_time: Time) -> Time:
        generated_latency_seconds = random.gauss(self._mean_latency, self._std_dev)
        return Time.from_seconds(max(0.0, generated_latency_seconds))