import threading
import time

from datasources.timesource import TimeSource
from utils.ObserverObservable import Observable, Observer
import gpsd

class LocationSource(Observable):
    def __init__(self, update_interval):
        Observable.__init__(self)
        self.lat = 0
        self.lon = 0
        self.time_source = TimeSource(update_interval)
        obs = LocationSource.LocationObserver(self)
        self.time_source.addObserver(obs)

    def start(self):
        self.time_source.start()

    def stop(self):
        self.time_source.stop()
        self.time_source.deleteObservers()

    def notify(self):
        self.setChanged()
        self.notifyObservers(arg=(self.lat, self.lon))

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def get_time(self):
        return self.time_source.get_current_epoch_time()

    class LocationObserver(Observer):
        def __init__(self, parent):
            Observer.__init__(self)
            self.parent = parent
            gpsd.connect()

        def update(self, observable, arg):
            try:

                packet = gpsd.get_current()
                print(packet.sats)
                if packet.mode > 1:
                    self.parent.lat = packet.lat.real
                    self.parent.lon = packet.lon.real
                else:
                    print("NOFIX")
                    self.parent.lat = None
                    self.parent.lon = None

                self.parent.notify()
            except Exception as e:
                print("Could not retrieve gps data ",e)


