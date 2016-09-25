from datasources.location_source import LocationSource
from datasources.speed_source import SpeedSource
from datasources.time_source import TimeSource
from test.helpers.providers import StubbedProvider
from utils.ObserverObservable import Observer


class CurrentDataViewModel(Observer):
    def __init__(self, location_source, speed_source, time_source):
        self.location_source = location_source
        self.speed_source = speed_source
        self.time_source = time_source
        self.time = None
        self.location = (None, None)
        self.speed = None
        self.location_source.addObserver(self)
        self.time_source.addObserver(self)
        self.speed_source.addObserver(self)

    def update(self, observable, arg):
        if isinstance(observable, TimeSource):
            self.time = arg
        if isinstance(observable, LocationSource):
            self.location = arg
        if isinstance(observable, SpeedSource):
            self.speed = arg

        print(self)

    def __str__(self):
        return (self.time.time(), self.location, self.speed).__str__()


if __name__ == "__main__":
    provider = StubbedProvider()
    location_source = LocationSource(1, provider)
    timer_source = TimeSource(1, provider)
    speed_source = SpeedSource(1, provider)

    vm = CurrentDataViewModel(location_source, timer_source, speed_source)
    timer_source.start()
    location_source.start()
    speed_source.start()
