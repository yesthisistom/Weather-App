__author__ = 'tv'

from collections import defaultdict

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class GeoLocation(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    neighborhood = Column(String(80), nullable=False)
    city = Column(String(80), nullable=False)
    state = Column(String(80), nullable=False)
    postal = Column(String(80), nullable=False)
    country = Column(String(80), nullable=False)
    request_str = Column(String(256), nullable=False)

    def __init__(self, geocode_return, request):
        self.request_str = request.strip().lower()

        if geocode_return.latlng:
            self.latitude = float(geocode_return.latlng[0])
            self.longitude = float(geocode_return.latlng[1])

        loc_json = defaultdict(str, "")
        for key in geocode_return.json:
            loc_json[key] = geocode_return.json[key]

        self.neighborhood = str(loc_json["neighborhood"])
        self.city = loc_json["city"]
        self.state = loc_json["state"]
        self.country = loc_json["country"]
        self.postal = loc_json["postal"]

    def get_address_str(self):
        location_str = [self.neighborhood, self.city, self.state, self.postal, self.country]

        return list(filter(lambda x: x.strip() != "", location_str))


engine = create_engine('sqlite:///locations.db')
Base.metadata.create_all(engine)
