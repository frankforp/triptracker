from time import strftime, localtime

from datasources.datasource import DataSource
from test.helpers.providers import StubbedProvider
from utils.ObserverObservable import Observer, Observable


class CurrentDataViewModel(Observer, Observable):
    def __init__(self, data_source):
        Observable.__init__(self)
        self.data_source = data_source
        self.time = None
        self.locationString = ""
        self.location = (None, None)
        self.speed = None
        self.data_source.addObserver(self)

    def update(self, observable, arg):
        time = arg[0]
        location = arg[1]
        speed = arg[2]

        if time is not None:
            self.time = strftime("%d-%m-%Y %H:%M:%S", localtime(time))
        else:
            self.time = None

        if location[0] is None or location[1] is None:
            self.locationString = "N/A"
        else:
            if location[0] >= 0:
                latString = '{0:.3f}° N'.format(location[0])
            else:
                latString = '{0:.3f}° S'.format(location[0])

            if location[1] >= 0:
                lonString = '{0:.3f}° E'.format(location[1])
            else:
                lonString = '{0:.3f}° W'.format(location[1])

            self.locationString = '{0} {1}'.format(latString, lonString)
            self.location = location

        if speed is not None:
            self.speed = '{:.1f} km/h'.format(speed * 3.6)
        else:
            self.speed = "N/A"

        print(self)
        self.setChanged()
        self.notifyObservers(arg=(self.time, self.locationString, self.speed, self.location))


    def __str__(self):
        return (self.time, self.locationString, self.speed).__str__()


if __name__ == "__main__":
    provider = StubbedProvider()
    datasource = DataSource(1, provider, provider, provider)

    vm = CurrentDataViewModel(datasource)
    datasource.start()
