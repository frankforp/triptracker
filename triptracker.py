from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from operations import CurrentDataCollector, Poller
from providers import GpsProvider
from ui.views import CurrentDataScreen
from kivy.garden.mapview import MapView


class TriptrackerApp(App):
    __provider = GpsProvider()
    __poller = Poller(__provider, __provider, __provider)
    curr_data_collector = CurrentDataCollector()

    def build(self):
        Builder.load_file('ui/triptracker.kv')
        # add widgets here
        sm.add_widget(CurrentDataScreen(name='current_data'))

        return sm

    def on_start(self):
        self.__poller.start()

    def on_stop(self):
        self.__poller.stop()


sm = ScreenManager()

if __name__ == '__main__':
    TriptrackerApp().run()
