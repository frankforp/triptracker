from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from operations import CurrentDataCollector
from providers import GpsProvider
from ui.views import CurrentDataScreen
from kivy.garden.mapview import MapView


class TriptrackerApp(App):

    _provider = GpsProvider("localhost", 2947)
    curr_datacollector = CurrentDataCollector(position_provider=_provider, time_provider=_provider,
                                              speed_provider=_provider)

    def build(self):
        Builder.load_file('ui/triptracker.kv')
        # add widgets here
        sm.add_widget(CurrentDataScreen(name='current_data'))

        return sm

    def on_start(self):
        self.curr_datacollector.start()


sm = ScreenManager()

if __name__ == '__main__':
    TriptrackerApp().run()
