from abc import ABCMeta, abstractmethod

import time

from dateutil.parser import parse
from gps3 import agps3


class TimeProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_time(self):
        return None

    @abstractmethod
    def poll(self):
        pass


class LocationProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_location(self):
        return None, None

    @abstractmethod
    def poll(self):
        pass


class SpeedProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_speed_in_meter_per_second(self):
        return None

    @abstractmethod
    def poll(self):
        pass


class SystemTimeProvider(TimeProvider):
    def poll(self):
        pass

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
        self.gpsd_socket = agps3.GPSDSocket()
        self.data_stream = agps3.DataStream()
    # for new_data in gpsd_socket:
    #     if new_data:
    #         data_stream.unpack(new_data)
    #         print('Altitude = ', data_stream.alt)
    #         print('Latitude = ', data_stream.lat)

    def connect(self):
        self.gpsd_socket.connect()
        self.gpsd_socket.watch()

    def disconnect(self):
        self.gpsd_socket.close()

    def poll(self):
        try:
            new_data = self.gpsd_socket.next()
            if new_data:
                self.data_stream.unpack(new_data)
                if self.data_stream.lat != 'n/a':
                    self.lat = float(self.data_stream.lat)

                if self.data_stream.lon != 'n/a':
                    self.lon = float(self.data_stream.lon)

                if self.data_stream.time != 'n/a':
                    time = parse(self.data_stream.time)
                    self.time = time.timestamp()

                if self.data_stream.speed != 'n/a':
                    self.speed = float(self.data_stream.speed)

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

    def get_speed_in_meter_per_second(self):
        return None
