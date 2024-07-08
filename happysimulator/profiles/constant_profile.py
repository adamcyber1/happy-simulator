from ..profile import Profile
from ..time import Time


class ConstantProfile(Profile):
    def __init__(self, rate: float):
        if rate < 0.0:
            raise ValueError("Rate must be positive.")

        self._rate = rate

    def get_rate(self, time: Time) -> float:
        return self._rate

    @classmethod
    def from_period(cls, time: Time) -> 'ConstantProfile':
        return ConstantProfile(1 / time.to_seconds())
