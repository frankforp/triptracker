from blinker import signal
from kivy.clock import mainthread
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.screenmanager import Screen

from models import CurrentData
from utils import format_time, get_location_string, get_speed


class CurrentDataScreen(Screen):
    time = StringProperty("N/A")
    locationString = StringProperty("N/A")
    speed = StringProperty("N/A")

    map = ObjectProperty(None)
    map_popup = ObjectProperty(None)

    _on_time_changed = signal('time_changed')
    _on_position_changed = signal('position_changed')
    _on_speed_changed = signal('speed_changed')

    def __init__(self, **kw):
        super().__init__(**kw)
        self._on_time_changed.connect(self._update_time)
        self._on_position_changed.connect(self._update_position)
        self._on_speed_changed.connect(self._update_speed)

    @mainthread
    def _update_time(self, sender, **kw):
        if kw['new_value'] is not None:
            self.time = format_time(kw['new_value'])
        else:
            self.time = "N/A"

    @mainthread
    def _update_position(self, sender, **kw):
        self.locationString = get_location_string(kw['new_value'])
        if kw['new_value'][0] is not None and kw['new_value'][1] is not None:
            self._updateMap(kw['new_value'][0], kw['new_value'][1])

    @mainthread
    def _update_speed(self, sender, **kw):
        self.speed = get_speed(kw['new_value'])

    def _updateMap(self, lat, lon):
        self.map_popup.lat = lat
        self.map_popup.lon = lon
        self.map.center_on(lat, lon)
