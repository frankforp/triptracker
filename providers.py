from abc import abstractmethod, ABCMeta

from blinker import signal
from dateutil.parser import parse
from gps3 import agps3


class DataProvider(metaclass=ABCMeta):
    @abstractmethod
    def collect(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class TimeProvider(DataProvider, metaclass=ABCMeta):
    _time_changed = signal('new_time_provided')


class PositionProvider(DataProvider, metaclass=ABCMeta):
    _position_changed = signal('new_position_provided')


class SpeedProvider(DataProvider, metaclass=ABCMeta):
    _speed_changed = signal('new_speed_provided')


class GpsProvider(PositionProvider, TimeProvider, SpeedProvider):

    _gpsd_socket = agps3.GPSDSocket()
    _data_stream = agps3.DataStream()
    _is_started = False

    def __init__(self, host, port):
        self.host = host
        self.port = port
    # for new_data in gpsd_socket:
    #     if new_data:
    #         data_stream.unpack(new_data)
    #         print('Altitude = ', data_stream.alt)
    #         print('Latitude = ', data_stream.lat)

    def start(self):
        if not self._is_started:
            self._gpsd_socket.connect()
            self._gpsd_socket.watch()
            self._is_started = True

    def stop(self):
        if self._is_started:
            self._gpsd_socket.close()
            self._is_started = False

    def collect(self):
        try:
            new_data = self._gpsd_socket.next()
            if new_data:
                self._data_stream.unpack(new_data)
                if self._data_stream.lat != 'n/a' and self._data_stream.lon != 'n/a':
                    self._position_changed.send(new_value=(float(self._data_stream.lat), float(self._data_stream.lon)))

                if self._data_stream.time != 'n/a':
                    time = parse(self._data_stream.time)
                    self._time_changed.send(new_value=time.timestamp())

                if self._data_stream.speed != 'n/a':
                    self._speed_changed.send(new_value=float(self._data_stream.speed))

        except Exception as e:
            print("Could not retrieve gps data ", e)
            self._position_changed.send(new_value=(None, None))
            self._time_changed.send(new_value=None)
            self._speed_changed.send(new_value=None)


