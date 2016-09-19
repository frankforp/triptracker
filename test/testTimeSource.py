from unittest import TestCase

import time

from datasources.providers.time_providers import SystemTimeProvider
from datasources.timesource import TimeSource
from utils.ObserverObservable import Observer


class TimeSourceTest(TestCase):
    class TimeSourceObserver(Observer):
        def __init__(self, update_rate_in_seconds, testcase):
            Observer.__init__(self)
            self.update_rate = update_rate_in_seconds
            self.testcase = testcase

        def update(self, observable, arg):
            expected_time = self.testcase.start_time + self.update_rate
            print(self.testcase.start_time)
            print(expected_time)
            print(arg)
            print("*****")
            self.testcase.assertEqual(expected_time, arg)

    def test_update_with5secinterval_shouldYieldCurrentTimePlus5Seconds(self):
        observer = TimeSourceTest.TimeSourceObserver(5, self)
        timeprovider = SystemTimeProvider()
        time_source = TimeSource(5, timeprovider)
        time_source.addObserver(observer)
        self.start_time = int(time.time())
        time_source.start()
        time.sleep(10)
        time_source.stop()
        time_source.deleteObservers()
