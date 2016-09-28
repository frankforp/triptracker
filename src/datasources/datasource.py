from utils.IntervalTimer import IntervalTimer
from utils.ObserverObservable import Observable


class DataSource(Observable):
    def __init__(self, update_rate, time_provider, location_provider, speed_provider):
        Observable.__init__(self)
        self.update_rate = update_rate
        self.timer = IntervalTimer(update_rate, self.timer_function)
        self.location = None
        self.time = None
        self.speed = None
        self.location_provider = location_provider
        self.time_provider = time_provider
        self.speed_provider = speed_provider

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def get_current_location(self):
        return self.location

    def get_current_speed(self):
        return self.speed

    def get_current_time(self):
        return self.time

    def timer_function(self):
        if self.location_provider is not None:
            self.location_provider.poll()
            self.location = self.location_provider.get_location()
        if self.time_provider is not None:
            self.time_provider.poll()
            self.time = self.time_provider.get_time()
        if self.speed_provider is not None:
            self.speed_provider.poll()
            self.speed = self.speed_provider.get_speed_in_meter_per_second()

        self.setChanged()
        self.notifyObservers((self.time, self.location, self.speed))
