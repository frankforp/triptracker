import datetime

from blinker import signal
from geopy.distance import vincenty

from models import CurrentData, TripData
from utils import IntervalTimer


class TripDataCollector:
    __trip_data = None
    __on_time_changed = signal('current_time_changed')
    __on_position_changed = signal('current_position_changed')
    __on_speed_changed = signal('current_speed_changed')
    __on_trip_started = signal('current_trip_started')
    __on_trip_stopped = signal('current_trip_stopped')

    def start(self, trip_type, odometer_reading):
        self.__trip_data = TripData(trip_type, odometer_reading)
        self.__on_time_changed.connect(self._update_time)
        self.__on_position_changed.connect(self._update_position)
        self.__on_trip_started.send()
        # self.__on_speed_changed.connect(self._update_speed)
        # self.__on_error_occurred.connect(self.__error_occurred)

    def stop(self):
        self.__on_time_changed.disconnect(self._update_time)
        self.__on_position_changed.disconnect(self._update_position)
        self.__on_trip_stopped.send()
        self.__trip_data = None

    def is_trip_active(self):
        return self.__trip_data is not None

    def _update_time(self, sender, **kw):
        new_time = kw['new_value']

        if new_time is not None:
            if self.__trip_data.started_on is None:
                self.__trip_data.started_on = kw['new_value']

            self.__trip_data.duration = self.__calculate_duration(self.__trip_data.started_on, new_time)
            self.__trip_data.average_speed = self.__calculate_avgspeed(self.__trip_data.distance_covered,
                                                                       self.__trip_data.duration)
            print(self.__trip_data)

    def _update_position(self, sender, **kw):
        old_pos = kw['old_value']
        new_pos = kw['new_value']
        self.__trip_data.distance_covered = self.__trip_data.distance_covered + self.__calculate_distance(old_pos,
                                                                                                          new_pos)
        self.__trip_data.average_speed = self.__calculate_avgspeed(self.__trip_data.distance_covered,
                                                                   self.__trip_data.duration)

        print(self.__trip_data)

    def __calculate_duration(self, start_time, end_time):
        if start_time is None or end_time is None:
            print("Warning: Cannot calculate duration because one of the times is None")
            return datetime.timedelta(0)

        if start_time > end_time:
            print("Error: Cannot calculate duration because start time > end_time")
            return datetime.timedelta(0)

        st = datetime.datetime.fromtimestamp(start_time)
        et = datetime.datetime.fromtimestamp(end_time)

        return et - st

    def __calculate_avgspeed(self, distance, duration):
        if duration.total_seconds() > 0:
            return distance / duration.total_seconds()

        return 0

    def __calculate_distance(self, old_pos, new_pos):
        if old_pos is (None, None) or new_pos is (None, None):
            return 0

        return vincenty(old_pos, new_pos).meters


class CurrentDataCollector:
    __current_data = None
    __on_time_changed = signal('new_time_available')
    __on_position_changed = signal('new_position_available')
    __on_speed_changed = signal('new_speed_available')
    __on_error_occurred = signal('provider_error_occured')

    def __init__(self):
        self.__current_data = CurrentData()
        self.__on_time_changed.connect(self._update_time)
        self.__on_position_changed.connect(self._update_position)
        self.__on_speed_changed.connect(self._update_speed)
        self.__on_error_occurred.connect(self.__error_occurred)

    def _update_time(self, sender, **kw):
        self.__current_data.epoch_time = kw['new_value']

    def _update_position(self, sender, **kw):
        new_value = kw['new_value']
        if new_value is not None:
            self.__current_data.position = new_value['lat'], new_value['lon']
            self.__current_data.fixtype = new_value['fixtype']
        else:
            self.__current_data.position = (None, None)
            self.__current_data.fixtype = None

    def _update_speed(self, sender, **kw):
        self.__current_data.speed_in_ms = kw['new_value']

    def __error_occurred(self, sender, **kw):
        print("Error getting data from {0}: {1}".format(kw['origin'], kw['error']))


class Poller:
    __time_changed = signal('new_time_available')
    __position_changed = signal('new_position_available')
    __speed_changed = signal('new_speed_available')
    __error_occurred = signal('provider_error_occured')

    def __init__(self, time_provider, position_provider, speed_provider, interval_in_seconds=1):
        self.__speed_provider = speed_provider
        self.__position_provider = position_provider
        self.__time_provider = time_provider
        self.__polltimer = IntervalTimer(interval_in_seconds=interval_in_seconds, function=self.__poll)

    def start(self):
        self.__speed_provider.start()
        self.__position_provider.start()
        self.__time_provider.start()
        self.__polltimer.start()

    def stop(self):
        self.__speed_provider.stop()
        self.__position_provider.stop()
        self.__time_provider.stop()
        self.__polltimer.stop()

    def __poll(self):
        epoch_time = self.__time_provider.get_time()
        print("Time {0}".format(epoch_time))
        if self.__time_provider.has_error_occured():
            self.__error_occurred.send(origin='time_provider', error=self.__time_provider.get_last_error())
        else:
            self.__time_changed.send(new_value=epoch_time)

        position = self.__position_provider.get_position()
        print("Pos {0}".format(position))
        if self.__time_provider.has_error_occured():
            self.__error_occurred.send(origin='position_provider', error=self.__position_provider.get_last_error())
        else:
            if position is None:
                self.__position_changed.send(new_value=None)
            else:
                self.__position_changed.send(
                    new_value=dict(lat=position[1][0], lon=position[1][1], fixtype=position[0]))

        speed = self.__speed_provider.get_speed()
        print("Speed {0}".format(speed))
        if self.__speed_provider.has_error_occured():
            self.__error_occurred.send(origin='speed_provider', error=self.__speed_provider.get_last_error())
        else:
            self.__speed_changed.send(new_value=speed)
