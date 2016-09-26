from kivy.app import App
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from datasources.datasource import DataSource
from test.helpers.providers import StubbedProvider
from utils.ObserverObservable import Observer
from viewmodels.viewmodels import CurrentDataViewModel
from kivy.garden.mapview import MapView


class TripScreen(Screen):
    pass


class CurrentDataScreen(Screen, Observer):
    def init_stuff(self, vm):
        self.current_data_viewmodel = vm
        self.current_data_viewmodel.addObserver(self)

    def update(self, observable, arg):
        self.updateUI(arg)

    @mainthread
    def updateUI(self, data):
        timelabel = self.ids['lblTime']
        locationlabel = self.ids['lblLocation']
        speedLabel = self.ids['lblSpeed']
        theMap = self.ids['map']
        popup = self.ids['popup']

        timelabel.text = str(data[0])
        locationlabel.text = str(data[1])
        speedLabel.text = str(data[2])

        lat = data[3][0]
        lon = data[3][1]
        if data[3][0] is not None and data[3][1] is not None:
            popup.lat = lat
            popup.lon = lon
            theMap.center_on(lat, lon)


class TriptrackerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        provider = StubbedProvider()
        self.datasource = DataSource(0.1, provider, provider, provider)
        self.vm = CurrentDataViewModel(self.datasource)

    def on_start(self):
        self.datasource.start()

    def on_stop(self):
        self.datasource.stop()

    def build(self):
        sm = ScreenManager()

        currentScreen = CurrentDataScreen(name='current')
        currentScreen.init_stuff(self.vm)

        sm.add_widget(currentScreen)
        sm.add_widget(TripScreen(name='trip'))

        return sm


if __name__ == '__main__':
    TriptrackerApp().run()
