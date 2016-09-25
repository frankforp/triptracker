import gpxpy

from datasources.providers.location_providers import LocationProvider


class StubbedLocationProvider(LocationProvider):
    def __init__(self):
        gpx_file = open("./sampledata/sample_locations.gpx")
        print("Loading sample gpx data..")
        gpx = gpxpy.parse(gpx_file)
        self.gpxdata = [point for track in gpx.tracks for segment in track.segments for point in segment.points]
        self.current = 0
        self.lat = None
        self.lon = None

    def get_location(self):
        self.lat = self.gpxdata[self.current].latitude
        self.lon = self.gpxdata[self.current].latitude
        self.current = (self.current + 1) % len(self.gpxdata)
