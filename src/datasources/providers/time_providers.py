from abc import ABCMeta, abstractmethod

import time


class TimeProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_time(self):
        pass


class SystemTimeProvider(TimeProvider):
    def get_time(self):
        return int(time.time())
