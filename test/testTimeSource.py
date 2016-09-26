import time
from unittest import TestCase

from datasources.datasource import DataSource
from datasources.providers import SystemTimeProvider
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
            print(int(arg.time()))
            print("*****")
            self.testcase.assertEqual(expected_time, int(arg.time()))

    def test_update_with5secinterval_shouldYieldCurrentTimePlus5Seconds(self):
        observer = TimeSourceTest.TimeSourceObserver(5, self)
        timeprovider = SystemTimeProvider()
        time_source = DataSource(5, timeprovider, None, None)
        time_source.addObserver(observer)
        self.start_time = int(time.time())
        time_source.start()
        time.sleep(5)
        time_source.stop()
        time_source.deleteObservers()
