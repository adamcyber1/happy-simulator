from abc import ABC, abstractmethod
from typing import Union

from happysimulator.time import Time


class DataSink(ABC):
    @abstractmethod
    def add_stat(self, time: Time, stats: Union[float, dict]):
        pass

    @abstractmethod
    def print_csv(self):
        pass