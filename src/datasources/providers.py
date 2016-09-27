from abc import ABCMeta, abstractmethod

import time

import gpsd


class TimeProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_time(self):
        return None


class LocationProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_location(self):
        return None, None

class SpeedProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_speed_in_meter_per_second(self):
        return None


class SystemTimeProvider(TimeProvider):
    def get_time(self):
        return time.time()


class GpsProvider(LocationProvider, TimeProvider, SpeedProvider):
    def __init__(self, host, port):
        self.lat = None
        self.lon = None
        self.time = None
        self.speed = None
        self.host = host
        self.port = port


    def connect(self):
        if self.host is None or self.port is None:
            gpsd.connect()
        else:
            gpsd.connect(self.host, self.port)

    def disconnect(self):
        gpsd.gpsd_socket.close()

    def poll(self):
        try:
            packet = gpsd.get_current()
            self.time = packet.time
            if packet.mode > 1:
                self.lat = packet.lat.real
                self.lon = packet.lon.real
                self.speed = packet.speed()
            else:
                self.lat = None
                self.lon = None
                self.speed = None

        except Exception as e:
            print("Could not retrieve gps data ", e)
            self.lat = None
            self.lon = None
            self.time = None
            self.speed = None

    def get_time(self):
        return self.time

    def get_location(self):
        return self.lat, self.lon
