from happysimulator.latency_distribution import LatencyDistribution
from happysimulator.time import Time


class ConstantLatency(LatencyDistribution):
    def __init__(self, latency: Time):
        super().__init__(latency)

    def get_latency(self, current_time: Time) -> Time:
        return Time.from_seconds(self._mean_latency)
