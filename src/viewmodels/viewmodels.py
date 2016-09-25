from time import strftime, localtime

from datasources.location_source import LocationSource
from datasources.speed_source import SpeedSource
from datasources.time_source import TimeSource
from test.helpers.providers import StubbedProvider
from utils.ObserverObservable import Observer, Observable


class CurrentDataViewModel(Observer, Observable):
    def __init__(self, location_source, speed_source, time_source):
        Observable.__init__(self)
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
            if arg is not None:
                self.time = strftime("%d-%m-%Y %H:%M:%S", localtime(arg))
            else:
                self.time = None
        if isinstance(observable, LocationSource):
            if arg is not None:
                if arg[0] is not None and arg[0] >= 0:
                    latString = '{0:.3f}° N'.format(arg[0])
                else:
                    latString = '{0:.3f}° S'.format(arg[0])

                if arg[1] is not None and arg[1] >= 0:
                    lonString = '{0:.3f}° E'.format(arg[1])
                else:
                    lonString = '{0:.3f}° W'.format(arg[1])

                self.location = '{0} {1}'.format(latString, lonString)
            else:
                self.location = "N/A"

        if isinstance(observable, SpeedSource):
            self.speed = '{:.1f} km/h'.format(arg * 3.6)

        print (self.__str__())
        self.setChanged()
        self.notifyObservers(arg=(self.time, self.location, self.speed))


    def __str__(self):
        return (self.time, self.location, self.speed).__str__()


if __name__ == "__main__":
    provider = StubbedProvider()
    location_source = LocationSource(2, provider)
    timer_source = TimeSource(2, provider)
    speed_source = SpeedSource(2, provider)

    vm = CurrentDataViewModel(location_source, timer_source, speed_source)
    timer_source.start()
    location_source.start()
    speed_source.start()
