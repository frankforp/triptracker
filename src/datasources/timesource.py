import threading
import time

from utils.IntervalTimer import IntervalTimer
from utils.ObserverObservable import Observable


class TimeSource(Observable, threading.Thread):
    def __init__(self, update_rate, time_provider):
        Observable.__init__(self)
        self.update_rate = update_rate
        self.timer = IntervalTimer(update_rate, self.timer_function)
        self.time = None
        self.time_provider = time_provider

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def get_current_epoch_time(self):
        return self.time

    def timer_function(self):
        self.time = self.time_provider.get_time()
        self.setChanged()
        self.notifyObservers(time)
