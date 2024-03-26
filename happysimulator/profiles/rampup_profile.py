from ..profile import Profile
from ..time import Time

class RampupProfile(Profile):
    def __init__(self, starting_rate: float, rampup_factor: float):
        if starting_rate <= 0:
            raise ValueError("Starting Rate must be positive.")

        self._rate = starting_rate
        self._factor = rampup_factor

    def get_rate(self, time: Time) -> float:
        return self._rate + (time.to_seconds() * self._factor)
