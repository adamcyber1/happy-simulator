import math

from ..profile import Profile
from ..time import Time


class SinusoidProfile(Profile):
    def __init__(self, shift: float, amplitude: float, period: Time):
        self._shift = shift
        self._amplitude = amplitude
        self._period = period

    def get_rate(self, time: Time) -> float:
        return self._shift + self._amplitude * math.sin(2 * math.pi * time.to_seconds() / self._period.to_seconds())