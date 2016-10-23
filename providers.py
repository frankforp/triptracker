from abc import ABCMeta, abstractmethod

import gpxpy
from dateutil.parser import parse
from geopy.distance import vincenty
from gps3 import agps3


class DataProvider(metaclass=ABCMeta):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class TimeProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_time(self):
        pass

    @abstractmethod
    def has_error_occured(self):
        pass


class PositionProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def has_error_occured(self):
        pass


class SpeedProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_speed(self):
        pass

    @abstractmethod
    def has_error_occured(self):
        pass


class GpsProvider(DataProvider, TimeProvider, PositionProvider, SpeedProvider):
    __gpsd_socket = agps3.GPSDSocket()
    __data_stream = agps3.DataStream()
    __is_started = False
    __position = (None, None)
    __time = None
    __speed = None
    __fixtype = None
    __has_error_occurred = False
    __last_error = None

    def __init__(self, host="localhost", port=2947):
        self.__host = host
        self.__port = port

    def start(self):
        if not self.__is_started:
            self.__gpsd_socket.connect(self.__host, self.__port)
            self.__gpsd_socket.watch()
            self.__is_started = True

    def stop(self):
        if self.__is_started:
            self.__gpsd_socket.close()
            self.__is_started = False

    def update(self):
        self.__has_error_occurred = False
        try:
            new_data = self.__gpsd_socket.next()
            if new_data:
                self.__data_stream.unpack(new_data)
                if self.__data_stream.mode != 'n/a':
                    fixtype = int(self.__data_stream.mode)
                    if fixtype > 0:
                        self.__fixtype = fixtype
                else:
                    self.__fixtype = None

                if self.__data_stream.lat != 'n/a' and self.__data_stream.lon != 'n/a':
                    self.__position = (float(self.__data_stream.lat), float(self.__data_stream.lon))
                else:
                    self.__position = (None, None)

                if self.__data_stream.time != 'n/a':
                    time = parse(self.__data_stream.time)
                    self.__time = time.timestamp()
                else:
                    self.__time = None

                if self.__data_stream.speed != 'n/a':
                    self.__speed = float(self.__data_stream.speed)
                else:
                    self.__speed = None

        except Exception as e:
            print("Could not retrieve gps data ", e)
            self.__has_error_occurred = True
            self.__last_error = e

    def get_speed(self):
        self.update()
        return self.__speed

    def get_position(self):
        self.update()
        if self.__fixtype is not None and self.__position is not (None, None):
            return self.__fixtype, self.__position

        return None

    def get_time(self):
        self.update()
        return self.__time

    def has_error_occured(self):
        return self.__has_error_occurred

    def get_last_error(self):
        return self.__last_error


class StubbedProvider(DataProvider, TimeProvider, PositionProvider, SpeedProvider):
    gpxdata = None
    current_index = 0

    def start(self):
        gpx_file = open("/home/developer/playground/triptracker/test/sampledata/sample_locations.gpx")
        print("Loading sample gpx data..")
        gpx = gpxpy.parse(gpx_file)
        self.gpxdata = [point for track in gpx.tracks for segment in track.segments for point in segment.points]

    def stop(self):
        pass

    def update(self):
        self.current_index = (self.current_index + 1) % len(self.gpxdata)

    def get_position(self):
        result = (3, (self.gpxdata[self.current_index].latitude, self.gpxdata[self.current_index].longitude))
        return result

    def get_time(self):
        return self.gpxdata[self.current_index].time.timestamp()

    def get_speed(self):
        result = None
        if self.current_index > 0:
            curr_location = self.get_position()[1]
            previous_location = (self.gpxdata[self.current_index - 1].latitude, self.gpxdata[self.current_index - 1].longitude)
            curr_time = self.gpxdata[self.current_index].time.timestamp()
            previous_time = self.gpxdata[self.current_index - 1].time.timestamp()
            dist_meters = vincenty(previous_location, curr_location).meters
            duration = curr_time - previous_time

            if duration > 0:
                result = dist_meters / duration

        self.update()
        return result

    def has_error_occured(self):
        pass
