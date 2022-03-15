from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TINYINT

# The flask_sqlalchemy module does not have to be initialized with the app right away
# We declare it here, with our Models, import it into our main app and initialise
# it there...
db = SQLAlchemy()

class Station(db.Model):
    # Note how we never define an __init__ method on the Station class? That’s
    # because SQLAlchemy adds an implicit constructor to all model classes which
    # accepts keyword arguments for all its columns and relationships. If you
    # decide to override the constructor for any reason, make sure to keep accepting
    # **kwargs and call the super constructor with those **kwargs to preserve this
    # behavior.
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=True)
    contractName = db.Column(db.String(45), unique=False, nullable=True)
    stationName = db.Column(db.String(45), unique=False, nullable=True)
    address = db.Column(db.String(60), unique=False, nullable=True)
    latitude = db.Column(db.Float, unique=False, nullable=True)
    longitude = db.Column(db.Float, unique=False, nullable=True)
    banking = db.Column(db.String(120), unique=False, nullable=False)
    bonus = db.Column(TINYINT, unique=False, nullable=False)

    # Notes on SQLAlchemy relationship definitions here:
    # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
    stationStates = db.relationship("StationState", back_populates="station")

    def to_json(self):
        json_station = {
            'station_id': self.id,
            'station_number': self.number,
            'station_contractName': self.contractName,
            'station_stationName': self.stationName,
            'station_address': self.address,
            'station_latitude': self.latitude,
            'station_longitude': self.longitude,
            'station_banking': self.banking,
            'station_bonus': self.bonus
        }

        return json_station

    def __repr__(self):
        return '<Station %r>' % self.stationName

class StationState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stationId = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    weatherTime = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(45), nullable=True)
    bike_stands = db.Column(db.Integer, nullable=True)
    available_bike_stands = db.Column(db.Integer, nullable=True)
    available_bikes = db.Column(db.Integer, nullable=True)
    lastUpdate = db.Column(db.BigInteger, nullable=True)

    station = db.relationship('Station', back_populates='stationStates')

    def __repr__(self):
        return '<Station %r>' % self.stationName

class weatherHistory(db.Model):
    weatherTime = db.Column(db.DateTime, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    main = db.Column(db.String(45), nullable=True)
    description = db.Column(db.String(256), nullable=True)
    temp = db.Column(db.Float, nullable=True)
    feels_like = db.Column(db.Float, nullable=True)
    temp_min = db.Column(db.Float, nullable=True)
    temp_max = db.Column(db.Float, nullable=True)
    pressure = db.Column(db.Integer, nullable=True)
    humidity = db.Column(db.Integer, nullable=True)
    sea_level = db.Column(db.Integer, nullable=True)
    grnd_level = db.Column(db.Integer, nullable=True)
    wind_speed = db.Column(db.Float, nullable=True)
    wind_deg = db.Column(db.Integer, nullable=True)
    wind_gust = db.Column(db.Float, nullable=True)
    clouds_all = db.Column(db.Integer, nullable=True)
    country = db.Column(db.String(64), nullable=True)
    name = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return '<Station %r>' % self.stationName