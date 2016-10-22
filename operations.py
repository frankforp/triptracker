from blinker import signal

from models import CurrentData
from utils import IntervalTimer


class CurrentDataCollector:
    __current_data = CurrentData()
    __on_time_changed = signal('new_time_available')
    __on_position_changed = signal('new_position_available')
    __on_speed_changed = signal('new_speed_available')
    __on_error_occurred = signal('provider_error_occured')

    def __init__(self):
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
        print ("Time {0}".format(epoch_time))
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
