from enum import Enum
import random

from happysimulator.time import Time


class ArrivalDistribution(Enum):
    CONSTANT = 1
    POISSON = 2

    def get_next_arrival_time(self, current_time: Time, rate_per_second: float) -> Time:
        if self == ArrivalDistribution.CONSTANT:
            return current_time + (1.0 / rate_per_second)
        elif self == ArrivalDistribution.POISSON:
            return current_time + Time.from_seconds(random.expovariate(rate_per_second))
        else:
            raise NotImplementedError("This ArrivalDistribution type not implemented")