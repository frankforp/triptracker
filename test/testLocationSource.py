from unittest import TestCase

import time

from datasources.LocationSource import LocationSource
from datasources.timesource import TimeSource
from utils.ObserverObservable import Observer


class LocationSourceTest(TestCase):
    class LocationSourceObserver(Observer):
        def __init__(self,  testcase):
            Observer.__init__(self)
            self.testcase = testcase

        def update(self, observable, arg):
            print(observable.get_time())
            print(arg)

    def test_update(self):
        observer = LocationSourceTest.LocationSourceObserver(self)
        location_source = LocationSource(1)
        location_source.addObserver(observer)
        location_source.start()
        time.sleep(50)
        location_source.stop()
        location_source.deleteObservers()
