import logging

from blinker import signal


class CurrentData:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("CurrentData")
    time_changed = signal('time_changed')
    position_changed = signal('position_changed')
    speed_changed = signal('speed_changed')

    _epoch_time = 0
    _position = (None, None)
    _speed_in_ms = 0

    @property
    def epoch_time(self):
        return self._epoch_time

    @epoch_time.setter
    def epoch_time(self, new_value):
        old_value = self._epoch_time
        if new_value is not None and new_value < 0:
            raise ValueError("Epoch time cannot be negative")

        self._epoch_time = new_value
        self.time_changed.send(old_value=old_value, new_value=new_value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_value):
        old_value = self._position

        new_lat = new_value[0]
        new_lon = new_value[1]

        if new_lat is not None and (new_lat < -90 or new_lat > 90):
            raise ValueError("Latitude should be between -90 and +90 degrees")

        if new_lon is not None and (new_lon < -180 or new_lon > 180):
            raise ValueError("Latitude should be between -180 and +180 degrees")

        self._position = new_value
        self.position_changed.send(old_value=old_value, new_value=new_value)

    @property
    def speed_in_ms(self):
        return self._speed_in_ms

    @speed_in_ms.setter
    def speed_in_ms(self, new_value):
        old_value = self._speed_in_ms
        if new_value is not None and new_value < 0:
            raise ValueError("Speed cannot be negative")

        self._speed_in_ms = new_value
        self.speed_changed.send(old_value=old_value, new_value=new_value)
