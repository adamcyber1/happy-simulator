import unittest

from happysimulator.profiles import ConstantProfile
from happysimulator.time import Time


class TestConstantProfile(unittest.TestCase):
    def test_initialization(self):
        """Tests that the profile is initialized with the correct rate."""
        profile = ConstantProfile(10)
        self.assertEqual(profile._rate, 10)

    def test_get_rate(self):
        """Tests that get_rate returns the initialized rate, regardless of the time."""
        profile = ConstantProfile(5)
        time = Time.from_seconds(1)
        self.assertEqual(profile.get_rate(time), 5)

    def test_from_period(self):
        """Tests that from_period calculates the correct rate based on the period."""
        period_seconds = 10  # 10 seconds
        time = Time.from_seconds(period_seconds)  # Assuming Time() can be set or initialized to represent 10 seconds somehow
        profile = ConstantProfile.from_period(time)
        self.assertEqual(profile.get_rate(time), 0.1)  # Since rate = 1 / period

    def test_negative_rate_initialization(self):
        with self.assertRaises(ValueError):
            ConstantProfile(-1)

if __name__ == '__main__':
    unittest.main()
