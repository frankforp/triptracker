from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from operations import CurrentDataCollector, Poller, TripDataCollector
from providers import GpsProvider, StubbedProvider
from ui.views import CurrentDataScreen, InactiveTripScreen, SettingsScreen, TripScreen
from kivy.garden.mapview import MapView


class TriptrackerApp(App):
    #__provider = StubbedProvider()
    __provider = GpsProvider()
    __poller = Poller(__provider, __provider, __provider)
    curr_data_collector = CurrentDataCollector()
    trip_collector = TripDataCollector()
    sm = ScreenManager()


    def build(self):
        Builder.load_file('ui/triptracker.kv')
        # add widgets here
        self.sm.add_widget(CurrentDataScreen(name='current_data'))
        self.sm.add_widget(InactiveTripScreen(name='inactive_trip'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(TripScreen(name='trip'))
        return self.sm

    def on_start(self):
        self.__poller.start()

    def on_stop(self):
        self.__poller.stop()





if __name__ == '__main__':
    TriptrackerApp().run()
