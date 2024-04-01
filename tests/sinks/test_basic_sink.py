import unittest
import pandas as pd
import os

from happysimulator.sinks.basic_sink import BasicSink
from happysimulator.time import Time


class TestBasicSinkCSV(unittest.TestCase):
    def setUp(self):
        self.stat_name = 'SampleStat'
        self.csv_sink = BasicSink(name="basic", stat_names=self.stat_name)

    def test_initialization(self):
        expected_columns = ['TIME_SECONDS', self.stat_name]
        self.assertEqual(list(self.csv_sink.df.columns), expected_columns)

    def test_add_stat(self):
        test_time = Time.from_seconds(1.5)
        test_stat = 10.5
        self.csv_sink.add_stat(test_time, test_stat)

        expected_df = pd.DataFrame({'TIME_SECONDS': [test_time.to_seconds()], self.stat_name: [test_stat]})
        pd.testing.assert_frame_equal(self.csv_sink.df, expected_df)

    def test_save_csv(self):
        """Test if the CSV file is saved correctly."""
        filename = 'test_output.csv'
        test_time = Time.from_seconds(1.56)
        test_stat = 20.75
        self.csv_sink.add_stat(test_time, test_stat)
        self.csv_sink.save_csv(filename)

        self.assertTrue(os.path.isfile(filename))

        saved_df = pd.read_csv(filename)
        expected_df = pd.DataFrame({'TIME_SECONDS': [test_time.to_seconds()], self.stat_name: [test_stat]})
        pd.testing.assert_frame_equal(saved_df, expected_df)

        os.remove(filename)

    def test_generate_csv_string(self):

        self.csv_sink.add_stat(Time.from_seconds(1.65), 10.5)
        self.csv_sink.add_stat(Time.from_seconds(4354), 20.75)

        csv_string = self.csv_sink.generate_csv_string()

        expected_csv_string = "TIME_SECONDS,SampleStat\n1.65,10.5\n4354.0,20.75\n"

        assert csv_string == expected_csv_string, f"The generated CSV string does not match the expected output: \n{csv_string} \n{expected_csv_string}"


if __name__ == '__main__':
    unittest.main()