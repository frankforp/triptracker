from blinker import Signal
class CurrentData:
    on_updated = Signal()

    def __init__(self, *args, **kwargs):
        self._epoch_time = 0
        self._position = (None, None)
        self._speed_in_ms = 0

    @property
    def epoch_time(self):
        return self._epoch_time

    @epoch_time.setter
    def epoch_time(self, value):
        if value < 0:
            raise ValueError("Epoch time cannot be negative")
        self._epoch_time = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, lat, lon):
        if lat < -90 or lat > 90:
            raise ValueError("Latitude should be between -90 and +90 degrees")
        if lon < -180 or lon > 180:
            raise ValueError("Latitude should be between -180 and +180 degrees")

        self._position = (lat, lon)

    @property
    def speed_in_ms(self):
        return self._speed_in_ms

    @speed_in_ms.setter
    def speed_in_ms(self, value):
        if value < 0:
            raise ValueError("Speed cannot be negative")
        self._speed_in_ms = value

    #def __repr__(self):
        #return '<CurrentData time={0} lat={1:.3f} lon={2:.3f}'.format(location[0])


