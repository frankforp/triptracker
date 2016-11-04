import abc
import json

import time
from blinker import signal

from models import LogEventType


class LogWriter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def write(self, log_event):
        pass

    def start(self):
        pass

    def stop(self):
        pass


class JsonFileWriter(LogWriter):
    __lines = []

    def __init__(self, filename):
        self.__filename = filename

    def write(self, log_event):
        self.__lines.append(log_event)

    def start(self):
        self.__lines = []

    def stop(self):
        with open(self.__filename, 'a') as file:
            json_string = json.dumps(self.__lines)
            file.write(json_string)
            file.write('\n')


class ConsoleWriter(LogWriter):
    def write(self, log_event):
        json_string = json.dumps(log_event)
        print("Logged: {log} ".format(log=json_string))


class TripLogger:
    __on_tpv_received = signal('new_tpv_available')
    __on_trip_started = signal('current_trip_started')
    __on_trip_stopped = signal('current_trip_stopped')
    __on_trip_paused = signal('current_trip_paused')
    __on_trip_resumed = signal('current_trip_resumed')

    def __init__(self, *logwriters):
        self.__logwriters = logwriters

    def start(self):
        self.__on_tpv_received.connect(self.__tpv_received)
        self.__on_trip_started.connect(self.__trip_started)
        self.__on_trip_stopped.connect(self.__trip_stopped)
        self.__on_trip_paused.connect(self.__trip_paused)
        self.__on_trip_resumed.connect(self.__trip_resumed)
        for writer in self.__logwriters:
            writer.start()

    def stop(self):
        self.__on_tpv_received.disconnect(self.__tpv_received)
        self.__on_trip_started.disconnect(self.__trip_started)
        self.__on_trip_stopped.disconnect(self.__trip_stopped)
        self.__on_trip_paused.disconnect(self.__trip_paused)
        self.__on_trip_resumed.disconnect(self.__trip_resumed)
        for writer in self.__logwriters:
            writer.stop()


    def __tpv_received(self, sender, **kw):
        data = dict(timestamp=time.time(), eventtype=LogEventType.DATAPOINT.name, data=kw['newvalue'])
        self.__write_to_log(data)

    def __trip_started(self, sender, **kw):
        data = dict(timestamp=time.time(), eventtype=LogEventType.TRIP_STARTED.name, data=kw)
        self.__write_to_log(data)

    def __trip_stopped(self, sender, **kw):
        data = dict(timestamp=time.time(), eventtype=LogEventType.TRIP_STOPPED.name, data=kw)
        self.__write_to_log(data)

    def __trip_resumed(self, sender, **kw):
        data = dict(timestamp=time.time(), eventtype=LogEventType.TRIP_RESUMED.name, data=kw)
        self.__write_to_log(data)

    def __trip_paused(self, sender, **kw):
        data = dict(timestamp=time.time(), eventtype=LogEventType.TRIP_PAUSED.name, data=kw)
        self.__write_to_log(data)

    def __write_to_log(self, data):
        for writer in self.__logwriters:
            writer.write(log_event=data)