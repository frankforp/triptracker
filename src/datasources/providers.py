from abc import ABCMeta, abstractmethod

import time


class TimeProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_time(self):
        pass


class LocationProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_location(self):
        return None, None


class SystemTimeProvider(TimeProvider):
    def get_time(self):
        return time.time()


class GpsProvider(LocationProvider, TimeProvider):
    def __init__(self, host, port):
        self.lat = None
        self.lon = None
        self.time = None
        if host is None or port is None:
            gpsd.connect()
        else:
            gpsd.connect(host, port)

    def poll(self):
        try:
            packet = gpsd.get_current()
            self.time = packet.time
            if packet.mode > 1:
                self.lat = packet.lat.real
                self.lon = packet.lon.real
            else:
                self.lat = None
                self.lon = None

        except Exception as e:
            print("Could not retrieve gps data ", e)
            self.lat = None
            self.lon = None
            self.time = None

    def get_time(self):
        return self.time

    def get_location(self):
        return (self.lat, self.lon)
