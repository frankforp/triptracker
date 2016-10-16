import time

from blinker import signal

from models import CurrentData
from utils import IntervalTimer


class CurrentDataCollector:
    _current_data = CurrentData()
    _on_time_changed = signal('new_time_provided')
    _on_position_changed = signal('new_position_provided')
    _on_speed_changed = signal('new_speed_provided')

    def __init__(self, time_provider, position_provider, speed_provider, interval_in_seconds=1):
        self._speed_provider = speed_provider
        self._position_provider = position_provider
        self._time_provider = time_provider
        self._collecttimer = IntervalTimer(interval_in_seconds=interval_in_seconds, function=self._collect_data)
        self._on_time_changed.connect(self._update_time)
        self._on_position_changed.connect(self._update_position)
        self._on_speed_changed.connect(self._update_speed)

    def start(self):
        self._time_provider.start()
        self._position_provider.start()
        self._speed_provider.start()
        self._collecttimer.start()

    def stop(self):
        self._collecttimer.stop()
        self._time_provider.stop()
        self._position_provider.stop()
        self._speed_provider.stop()

    def _update_time(self, sender, **kw):
        self._current_data.epoch_time = kw['new_value']

    def _update_position(self, sender, **kw):
        self._current_data.position = kw['new_value']

    def _update_speed(self, sender, **kw):
        self._current_data.speed_in_ms = kw['new_value']

    def _collect_data(self):
        self._speed_provider.collect()
        self._position_provider.collect()
        self._time_provider.collect()

