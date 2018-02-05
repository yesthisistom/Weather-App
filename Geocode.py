__author__ = 'tv'

from GeoLocation import GeoLocation, Base

import geocoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



class Geocode:

    def __init__(self):
        self._google_api_key = 'AIzaSyA_Ji-qVkLwMNWfla6gs6c7sWZhGla617I'
        self._bing_api_key = None

        self._engine = create_engine('sqlite:///locations.db')
        Base.metadata.bind = self._engine
        self._session = sessionmaker(bind=self._engine)()

    def geocode_anything(self, location):

        reply = self._session.query(GeoLocation).filter_by(request_str=location.strip().lower())
        if reply.first():
            return reply.first()

        if Geocode.is_coordinate(location):
            lat = location.split(",")[0].strip()
            lon = location.split(",")[1].strip()

            return self.reverse_geocode((lat, lon))

        elif Geocode.is_ip(location):
            return self.geocode_ip(location)
        else:
            return self.geocode(location)

    def reverse_geocode(self, coordinate):
        g = geocoder.google(coordinate, method='reverse', key=self._google_api_key)
        if g.error:
            return None

        geo_loc = GeoLocation(g, coordinate)
        self._session.add(geo_loc)
        self._session.commit()
        return geo_loc

    def geocode(self, location):
        g = geocoder.google(location, key=self._google_api_key)

        if g.error:
            return None

        geo_loc = GeoLocation(g, location)
        self._session.add(geo_loc)
        self._session.commit()
        return geo_loc

    def geocode_ip(self, ip):
        g = geocoder.ip(ip)

        if g.error or not g.latlng:
            return None

        geo_loc = GeoLocation(g, ip)
        self._session.add(geo_loc)
        self._session.commit()
        return geo_loc

    @staticmethod
    def is_coordinate(string):
        if len(string.split(",")) != 2:
            return False

        for x in string.split(","):
            try:
                float(x.strip())
            except ValueError:
                return False

        return True

    @staticmethod
    def is_ip(string):
        num_list = string.split(".")

        if len(num_list) >= 4:
            for num in num_list:
                try:
                    int(num.strip())
                except ValueError:
                    return False
            return True
        if len(string.split(":")) == 6:
            return True

        return False
