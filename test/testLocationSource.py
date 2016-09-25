import time
from unittest import TestCase

from datasources.location_source import LocationSource
from utils.ObserverObservable import Observer


class LocationSourceTest(TestCase):
    class LocationSourceObserver(Observer):
        def __init__(self,  testcase):
            Observer.__init__(self)
            self.testcase = testcase

        def update(self, observable, arg):
            print(arg)

    def test_update(self):
        observer = LocationSourceTest.LocationSourceObserver(self)
        from test.helpers.providers import StubbedProvider
        location_provider = StubbedProvider()
        location_source = LocationSource(1, location_provider)
        location_source.addObserver(observer)
        location_source.start()
        time.sleep(2)
        location_source.stop()
        location_source.deleteObservers()
