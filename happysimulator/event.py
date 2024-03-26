import uuid
from abc import ABC
from typing import Callable

from .time import Time


class Event(ABC):
    def __init__(self, time: Time, name: str, callback: Callable):
        self.time = time
        self.name = name
        self.callback = callback
        self._hash = hash(self.name + str(uuid.uuid4()))

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, Event):
            return NotImplemented
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, Event):
            return NotImplemented
        return hash(self) < hash(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

