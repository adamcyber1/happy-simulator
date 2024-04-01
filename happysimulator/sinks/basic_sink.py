import pandas as pd
from typing import Union, List

from happysimulator.datasink import DataSink
from happysimulator.time import Time

class BasicSink(DataSink):
    def __init__(self, name: str, stat_names: Union[str, List[str]]):
        if isinstance(stat_names, str):
            stat_names = [stat_names]  # Convert to list for uniform processing
        self.stat_names = stat_names  # Store as list
        self.df = pd.DataFrame(columns=['TIME_SECONDS'] + self.stat_names)
        self.name = name

    def add_stat(self, time: Time, stats: Union[float, dict]):
        if isinstance(stats, dict):
            # Ensure stats dict only contains keys that are in self.stat_names
            filtered_stats = {k: v for k, v in stats.items() if k in self.stat_names}
            new_row = {'TIME_SECONDS': time.to_seconds(), **filtered_stats}
        else:
            if len(self.stat_names) != 1:
                raise ValueError("A single stat value provided but multiple stat names are defined.")
            new_row = {'TIME_SECONDS': time.to_seconds(), self.stat_names[0]: stats}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

    def generate_csv_string(self) -> str:
        return self.df.to_csv(index=False)

    def print_csv(self):
        print(self.generate_csv_string())

    def save_csv(self, filename: str):
        self.df.to_csv(filename, index=False)