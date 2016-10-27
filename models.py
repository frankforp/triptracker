import datetime
import logging

from blinker import signal

NON_BUSINESS = 0
BUSINESS = 1


class TripData:
    __type = NON_BUSINESS
    __odometer_start = 0
    __started_on = None
    __duration = datetime.timedelta(0)
    __dist = 0
    __avg_speed = 0

    __tripdata_changed = signal('tripdata_changed')

    __trip_type_changed = signal('trip_type_changed')
    __odometer_start_changed = signal('odometer_start_changed')
    __started_on_changed = signal('started_on_changed')
    __duration_changed = signal('duration_changed')
    __dist_changed = signal('dist_changed')
    __avg_speed_changed = signal('avg_speed_changed')

    def __init__(self, trip_type, odometer):
        self.trip_type = trip_type
        self.odometer_start = odometer

    @property
    def trip_type(self):
        return self.__type

    @trip_type.setter
    def trip_type(self, value):
        if value != NON_BUSINESS and value != BUSINESS:
            raise ValueError("Trip type must be BUSINESS or NON_BUSINESS")
        self.__type = value
        self.__trip_type_changed.send(newvalue=value)
        self.__tripdata_changed.send(self)

    @property
    def odometer_start(self):
        return self.__odometer_start

    @odometer_start.setter
    def odometer_start(self, value):
        if value < 0:
            raise ValueError("Odometer setting must be positive")
        self.__odometer_start = value
        self.__odometer_start_changed.send(newvalue=value)
        self.__tripdata_changed.send(self)

    @property
    def started_on(self):
        return self.__started_on

    @started_on.setter
    def started_on(self, value):
        if value < 0:
            raise ValueError("Invalid time stampt for start time")
        self.__started_on = value
        self.__started_on_changed.send(newvalue=value)
        self.__tripdata_changed.send(self)

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        if value.total_seconds() < 0:
            raise ValueError("Duration must be positive")
        self.__duration = value
        self.__duration_changed.send(newvalue=value)
        self.__tripdata_changed.send(self)

    @property
    def distance_covered(self):
        return self.__dist

    @distance_covered.setter
    def distance_covered(self, value):
        if value < 0:
            raise ValueError("Distance must be positive")
        self.__dist = value
        self.__dist_changed.send(newvalue=value)
        self.__tripdata_changed.send(self)

    @property
    def average_speed(self):
        return self.__avg_speed

    @average_speed.setter
    def average_speed(self, value):
        if value < 0:
            raise ValueError("Average speed must be positive")
        self.__avg_speed = value
        self.__avg_speed_changed.send(newvalue=value)
        self.__tripdata_changed.send(self)

    def __repr__(self, *args, **kwargs):
        return "[TripData: Type = {0}, odometer_start={1}, started_on={2}, " \
               "duration={3},distance_covered={4}, average_speed={5}".format(self.trip_type, self.odometer_start,
                                                                             self.started_on, self.duration,
                                                                             self.distance_covered, self.average_speed)


NO_FIX = 1
TWOD_FIX = 2
THREED_FIX = 3


class CurrentData:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("CurrentData")
    time_changed = signal('current_time_changed')
    position_changed = signal('current_position_changed')
    speed_changed = signal('current_speed_changed')
    fixtype_changed = signal('current_fix_changed')

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
