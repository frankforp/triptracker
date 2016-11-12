from enum import Enum

from blinker import signal
from kivy.app import App
from kivy.clock import mainthread
from kivy.factory import Factory
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen

from models import CurrentData, NO_FIX, TWOD_FIX, THREED_FIX, BUSINESS
from utils import format_time, get_location_string, format_speed




class CurrentDataScreen(Screen):
    time = StringProperty("N/A")
    locationString = StringProperty("N/A")
    speed = StringProperty("N/A")
    fixText = StringProperty("NO FIX")
    fixColor = ObjectProperty((1, 0, 0, 1))
    activeTripText = StringProperty("")

    map = ObjectProperty(None)
    map_popup = ObjectProperty(None)

    __on_time_changed = signal('current_time_changed')
    __on_position_changed = signal('current_position_changed')
    __on_speed_changed = signal('current_speed_changed')
    __on_fix_changed = signal('current_fix_changed')

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
        self.speed = format_speed(kw['new_value'])


    def _updateMap(self, lat, lon):
        self.map_popup.lat = lat
        self.map_popup.lon = lon
        self.map.center_on(lat, lon)


class InactiveTripScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

        self.start_trip_box = Factory.NewTripInfo()

    def start_trip(self):
        self.start_trip_box.bind(on_dismiss=self.modal_closed)
        self.start_trip_box.open()

    def modal_closed(self, instance):
        print(instance.entered_odometer_reading)
        print(instance.trip_type)
        if instance.entered_odometer_reading == "":
            return False

        odometer = int(instance.entered_odometer_reading)
        triptype = instance.trip_type

        is_logging_enabled = App.get_running_app().config.get('logging', 'is_logging_enabled')
        is_file_logging_enabled = App.get_running_app().config.get('logging', 'is_file_logging_enabled')
        logdir = App.get_running_app().config.get('logging', 'file_log_dir')

        if is_logging_enabled == '1' and is_file_logging_enabled == '1':
            App.get_running_app().trip_collector.start(triptype, odometer, log_options=["File"], logdir=logdir)
        else:
            App.get_running_app().trip_collector.start(triptype, odometer)

        App.get_running_app().sm.transition.direction = 'left'
        App.get_running_app().sm.current = 'trip'



class TripScreen(Screen):

    __tripdata_changed = signal('tripdata_changed')

    __trip_stopped = signal('current_trip_stopped')
    __trip_started = signal('current_trip_started')
    __trip_paused = signal('current_trip_paused')
    __trip_resumed = signal('current_trip_resumed')

    trip_type = StringProperty("N/A")
    started_on = StringProperty("N/A")
    odometer = StringProperty("N/A")
    duration = StringProperty("N/A")
    dist = StringProperty("N/A")
    avg_speed = StringProperty("N/A")




    def __init__(self, **kw):
        super().__init__(**kw)
        self.__tripdata_changed.connect(self.__update_screen)
        self.__trip_stopped.connect(self.__trip_stop);
        self.__trip_paused.connect(self.__trip_pause);
        self.__trip_resumed.connect(self.__trip_resume);
        self.__trip_started.connect(self.__trip_start)


    @mainthread
    def __update_screen(self, sender, **kw):
        self.trip_type = "Business" if sender.trip_type == BUSINESS else "Non business"
        self.odometer = '{:.0f} km'.format(sender.odometer_start / 1000)
        self.started_on = format_time(sender.started_on)
        self.duration = '{0}'.format(sender.duration)
        self.dist = '{:.1f} km'.format(sender.distance_covered / 1000)
        self.avg_speed = format_speed(sender.average_speed)



    def pause_trip(self):
        App.get_running_app().trip_collector.pause()

    def stop_trip(self):
        App.get_running_app().trip_collector.stop()

    def resume_trip(self):
        App.get_running_app().trip_collector.resume()

    @mainthread
    def __trip_stop(self, sender, **kw):
        App.get_running_app().trip_state = 0
        App.get_running_app().sm.transition.direction = 'left'
        App.get_running_app().sm.current = 'current_data'
        print("Trip stopped. {0}".format(kw))

    @mainthread
    def __trip_start(self, sender, **kw):
        App.get_running_app().trip_state = 1
        print("Trip started")

    @mainthread
    def __trip_pause(self, sender, **kw):
        App.get_running_app().trip_state = 2
        print("Trip paused on {0} at {1} ".format(format_time(kw['time']), get_location_string(kw['position'])))

    @mainthread
    def __trip_resume(self, sender, **kw):
        App.get_running_app().trip_state = 1
        print("Trip resumed on {0} at {1} ".format(format_time(kw['time']), get_location_string(kw['position'])))




