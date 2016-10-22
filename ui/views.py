from blinker import signal
from kivy.clock import mainthread
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.screenmanager import Screen

from models import CurrentData, NO_FIX, TWOD_FIX, THREED_FIX
from utils import format_time, get_location_string, get_speed


class CurrentDataScreen(Screen):
    time = StringProperty("N/A")
    locationString = StringProperty("N/A")
    speed = StringProperty("N/A")
    fixText = StringProperty("NO FIX")
    fixColor = ObjectProperty((1, 0, 0, 1))

    map = ObjectProperty(None)
    map_popup = ObjectProperty(None)

    __on_time_changed = signal('time_changed')
    __on_position_changed = signal('position_changed')
    __on_speed_changed = signal('speed_changed')
    __on_fix_changed = signal('fix_changed')

    def __init__(self, **kw):
        super().__init__(**kw)
        self.__on_time_changed.connect(self.__update_time)
        self.__on_position_changed.connect(self.__update_position)
        self.__on_speed_changed.connect(self.__update_speed)
        self.__on_fix_changed.connect(self.__update_fix)

    @mainthread
    def __update_time(self, sender, **kw):
        if kw['new_value'] is not None:
            self.time = format_time(kw['new_value'])
        else:
            self.time = "N/A"

    @mainthread
    def __update_fix(self, sender, **kw):
        new_value = kw['new_value']
        if new_value is not None:
            self.__set_fix_related_fields(new_value)
        else:
            self.__set_fix_related_fields(NO_FIX)

    def __set_fix_related_fields(self, fix_type):
        if fix_type == NO_FIX:
            self.fixColor = (1, 0, 0, 1)
            self.fixText = "NO GPS SIGNAL"
            self.time = "N/A"
            self.locationString = "N/A"
            self.speed = "N/A"
        if fix_type == TWOD_FIX:
            self.fixColor = (1, 1, 0, 1)
            self.fixText = "BAD GPS SIGNAL"
        if fix_type == THREED_FIX:
            self.fixColor = (0, 1, 0, 1)
            self.fixText = "GPS WORKS OK"

    @mainthread
    def __update_position(self, sender, **kw):
        self.locationString = get_location_string(kw['new_value'])
        if kw['new_value'][0] is not None and kw['new_value'][1] is not None:
            self._updateMap(kw['new_value'][0], kw['new_value'][1])

    @mainthread
    def __update_speed(self, sender, **kw):
        self.speed = get_speed(kw['new_value'])

    def _updateMap(self, lat, lon):
        self.map_popup.lat = lat
        self.map_popup.lon = lon
        self.map.center_on(lat, lon)
