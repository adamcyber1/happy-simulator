from ..profile import Profile
from ..time import Time


class SpikeProfile(Profile):
    def __init__(self, rampup_start: Time, rampdown_start: Time, starting_rate: float, rampup_factor: float,
                 rampdown_factor: float = 1):
        self.rampup_start = rampup_start
        self.rampdown_start = rampdown_start
        self.starting_rate = starting_rate
        self.rampup_factor = rampup_factor
        self.rampdown_factor = rampdown_factor
        self.peak_rate = starting_rate + (rampdown_start - rampup_start).to_seconds() * rampup_factor

    def get_rate(self, time: Time) -> float:
        if time < self.rampup_start:
            return self.starting_rate
        elif self.rampup_start <= time < self.rampdown_start:
            return self.starting_rate + (self.rampup_factor * (time - self.rampup_start).to_seconds())
        else:  # After rampdown_start
            return max(self.starting_rate, self.peak_rate - (self.rampdown_factor * (time - self.rampdown_start).to_seconds()))