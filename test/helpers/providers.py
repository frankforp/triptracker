import random

import gpxpy
import time

from datasources.providers import LocationProvider, TimeProvider, SpeedProvider


class StubbedProvider(TimeProvider, LocationProvider, SpeedProvider):
    def __init__(self):
        gpx_file = open("/home/developer/projects/triptracker/test/sampledata/sample_locations.gpx")
        print("Loading sample gpx data..")
        gpx = gpxpy.parse(gpx_file)
        self.gpxdata = [point for track in gpx.tracks for segment in track.segments for point in segment.points]
        self.current_index = 0
        self.lat = None
        self.lon = None

    def get_location(self):
        self.lat = self.gpxdata[self.current_index].latitude
        self.lon = self.gpxdata[self.current_index].longitude
        self.current_index = (self.current_index + 1) % len(self.gpxdata)
        return self.lat, self.lon

    def get_time(self):
        return time.time()

    def get_speed_in_meter_per_second(self):
        return random.uniform(0, 36)

