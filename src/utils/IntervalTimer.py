import threading

import time


class IntervalTimer(threading.Thread):
    def __init__(self, interval_in_seconds, function):
        super().__init__()
        self.isStopped = False
        self.interval_in_seconds = interval_in_seconds
        self.timer_function = function

    def run(self):
        while not self.isStopped:
            time.sleep(self.interval_in_seconds)
            self.timer_function()

    def stop(self):
        self.isStopped = True
