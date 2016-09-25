import time

from utils.IntervalTimer import IntervalTimer
from utils.ObserverObservable import Observable


class LocationSource(Observable):
    def __init__(self, update_rate, location_provider):
        Observable.__init__(self)
        self.update_rate = update_rate
        self.timer = IntervalTimer(update_rate, self.timer_function)
        self.location = None
        self.location_provider = location_provider

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def get_current_location(self):
        return self.location

    def timer_function(self):
        self.location = self.location_provider.get_location()
        self.setChanged()
        self.notifyObservers(self.location)
