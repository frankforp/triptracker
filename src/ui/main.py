from time import strftime, localtime

from kivy.app import App
from kivy.clock import mainthread
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from datasources.datasource import DataSource
from datasources.providers import GpsProvider, SystemTimeProvider
from test.helpers.providers import StubbedProvider
from utils.ObserverObservable import Observer
from kivy.garden.mapview import MapView


class TripScreen(Screen):
    pass


class InactiveTripScreen(Screen):
    pass


def __get_location_string__(location):
    if location[0] is None or location[1] is None:
        return "N/A"
    else:
        if location[0] >= 0:
            latString = '{0:.3f}° N'.format(location[0])
        else:
            latString = '{0:.3f}° S'.format(location[0])

        if location[1] >= 0:
            lonString = '{0:.3f}° E'.format(location[1])
        else:
            lonString = '{0:.3f}° W'.format(location[1])

        return '{0} {1}'.format(latString, lonString)


def __get_speed__(speed):
    if speed is None:
        return "N/A"
    else:
        return '{:.1f} km/h'.format(speed * 3.6)


def __format_time__(time):
    if time is not None:
        return strftime("%d-%m-%Y %H:%M:%S", localtime(time))
    else:
        return "N/A"


class CurrentDataScreen(Screen, Observer, EventDispatcher):
    time = StringProperty()
    locationString = StringProperty()
    lat = NumericProperty(51)
    lon = NumericProperty(6)
    speed = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.data_source = None

    def init_data_source(self, data_source):
        self.data_source = data_source
        self.data_source.addObserver(self)

    def update(self, observable, arg):
        self.update_ui(arg)

    @mainthread
    def update_ui(self, data):
        self.time = __format_time__(data[0])
        self.locationString = __get_location_string__(data[1])
        if data[1][0] is not None and data[1][1] is not None:
            self.lat = data[1][0]
            self.lon = data[1][1]
            self.__updateMap__()

        self.speed = __get_speed__(data[2])

    def __updateMap__(self):
        the_map = self.ids['map']
        popup = self.ids['popup']
        popup.lat = self.lat
        popup.lon = self.lon
        the_map.center_on(self.lat, self.lon)


class TriptrackerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = GpsProvider(None, None)
        self.time_provider = SystemTimeProvider()
        self.data_source = DataSource(1, self.time_provider, self.provider, self.provider)

    def on_start(self):
        self.provider.connect()
        self.data_source.start()

    def on_stop(self):
        self.data_source.stop()
        self.provider.disconnect()

    def build(self):
        sm = ScreenManager()

        current_screen = CurrentDataScreen(name='current')
        current_screen.init_data_source(data_source=self.data_source)

        sm.add_widget(current_screen)
        sm.add_widget(InactiveTripScreen(name='trip_inactive'))
        sm.add_widget(TripScreen(name='trip'))

        return sm


if __name__ == '__main__':
    TriptrackerApp().run()
