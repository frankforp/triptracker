import random

import gpxpy
from geopy.distance import great_circle

from datasources.providers import LocationProvider, TimeProvider, SpeedProvider


class StubbedProvider(TimeProvider, LocationProvider, SpeedProvider):
    def __init__(self):
        gpx_file = open("/home/wildfly/development/other/triptracker/test/sampledata/sample_locations.gpx")
        print("Loading sample gpx data..")
        gpx = gpxpy.parse(gpx_file)
        self.gpxdata = [point for track in gpx.tracks for segment in track.segments for point in segment.points]
        self.current_index = 0

    def __update__(self):
        self.current_index = (self.current_index + 1) % len(self.gpxdata)

    def get_location(self):
        result = (self.gpxdata[self.current_index].latitude, self.gpxdata[self.current_index].longitude)
        return result

    def get_time(self):
        return self.gpxdata[self.current_index].time.timestamp()

    def get_speed_in_meter_per_second(self):
        result = None
        if self.current_index > 0:
            curr_location = self.get_location()
            previous_location = (self.gpxdata[self.current_index - 1].latitude, self.gpxdata[self.current_index - 1].longitude)
            curr_time = self.gpxdata[self.current_index].time.timestamp()
            previous_time = self.gpxdata[self.current_index - 1].time.timestamp()
            dist_meters = great_circle(previous_location, curr_location).meters
            duration = curr_time - previous_time

            if duration > 0:
                result = dist_meters / duration

        self.__update__()
        return result

