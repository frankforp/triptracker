from kivy.app import App
from kivy.clock import mainthread
from kivy.uix.widget import Widget

from datasources.location_source import LocationSource
from datasources.speed_source import SpeedSource
from datasources.time_source import TimeSource
from test.helpers.providers import StubbedProvider
from utils.ObserverObservable import Observer
from viewmodels.viewmodels import CurrentDataViewModel


class TriptrackerScreen(Widget, Observer):


    def init_stuff(self, vm):
        self.current_data_viewmodel = vm
        self.current_data_viewmodel.addObserver(self)

    def update(self, observable, arg):

        self.updateUI(arg)

    @mainthread
    def updateUI(self, data):
        #print("updatedui "+data)
        timelabel = self.ids['lblTime']
        locationlabel = self.ids['lblLocation']
        speedLabel = self.ids['lblSpeed']


        timelabel.text = str(data[0])
        locationlabel.text = str(data[1])
        speedLabel.text = str(data[2])




class TriptrackerApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        provider = StubbedProvider()
        self.location_source = LocationSource(1, provider)
        self.timer_source = TimeSource(1, provider)
        self.speed_source = SpeedSource(1, provider)
        self.vm = CurrentDataViewModel(self.location_source, self.timer_source, self.speed_source)

    def on_start(self):
        self.timer_source.start()
        self.location_source.start()
        self.speed_source.start()

    def on_stop(self):
        self.timer_source.stop()
        self.location_source.stop()
        self.speed_source.stop()

    def build(self):
        screen = TriptrackerScreen()
        screen.init_stuff(self.vm)

        return screen


if __name__ == '__main__':
    TriptrackerApp().run()
