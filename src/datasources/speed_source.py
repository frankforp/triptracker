import time

from utils.IntervalTimer import IntervalTimer
from utils.ObserverObservable import Observable


class SpeedSource(Observable):
    def __init__(self, update_rate, speed_provider):
        Observable.__init__(self)
        self.update_rate = update_rate
        self.timer = IntervalTimer(update_rate, self.timer_function)
        self.speed = None
        self.speed_provider = speed_provider

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def get_current_speed(self):
        return self.speed

    def timer_function(self):
        self.speed = self.speed_provider.get_speed_in_meter_per_second()
        self.setChanged()
        self.notifyObservers(self.speed)
