import logging

from blinker import signal

NON_BUSINESS = 0
BUSINESS = 1

NO_FIX = 1
TWOD_FIX = 2
THREED_FIX = 3


# class TripData:
#     _type = NON_BUSINESS
#     _odometer_start = 0
#     _started_on = None
#     _duration = 0
#     _dist = 0
#     _avg_speed = 0


class CurrentData:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("CurrentData")
    time_changed = signal('time_changed')
    position_changed = signal('position_changed')
    speed_changed = signal('speed_changed')
    fixtype_changed = signal('fixtype_changed')

    __epoch_time = 0
    __position = (None, None)
    __speed_in_ms = 0
    __fixtype = None

    @property
    def epoch_time(self):
        return self.__epoch_time

    @epoch_time.setter
    def epoch_time(self, new_value):
        old_value = self.__epoch_time
        if new_value is not None and new_value < 0:
            raise ValueError("Epoch time cannot be negative")

        self.__epoch_time = new_value
        self.time_changed.send(old_value=old_value, new_value=new_value)

    @property
    def fixtype(self):
        return self.__fixtype

    @fixtype.setter
    def fixtype(self, new_value):
        old_value = self.__fixtype

        if new_value is not None and (new_value < NO_FIX or new_value > THREED_FIX):
            raise ValueError("Fix type should be either NO_FIX (1), TWOD_FIX (2) or THREED_FIX (3)")

        self.__fixtype = new_value
        self.fixtype_changed.send(old_value=old_value, new_value=new_value)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_value):
        old_value = self.__position

        new_lat = new_value[0]
        new_lon = new_value[1]

        if new_lat is not None and (new_lat < -90 or new_lat > 90):
            raise ValueError("Latitude should be between -90 and +90 degrees")

        if new_lon is not None and (new_lon < -180 or new_lon > 180):
            raise ValueError("Latitude should be between -180 and +180 degrees")

        self.__position = new_value
        self.position_changed.send(old_value=old_value, new_value=new_value)

    @property
    def speed_in_ms(self):
        return self.__speed_in_ms

    @speed_in_ms.setter
    def speed_in_ms(self, new_value):
        old_value = self.__speed_in_ms
        if new_value is not None and new_value < 0:
            raise ValueError("Speed cannot be negative")

        self.__speed_in_ms = new_value
        self.speed_changed.send(old_value=old_value, new_value=new_value)
