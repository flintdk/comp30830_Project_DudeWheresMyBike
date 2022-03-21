# -*- coding: utf-8 -*-
import functools
from flask import Flask, g, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from jinja2 import Template
from models import db, Station, StationState, weatherHistory

# Create our flask app.
# Static files are server from the 'static' directory
dudeWMB = Flask(__name__, static_url_path='')

# In Flask, regardless of how you load your config, there is a 'config' object
# available which holds the loaded configuration values: The 'config' attribute
# of the Flask object
# The config is actually a subclass of a dictionary and can be modified just like
# any dictionary.  E.g. to update multiple keys at once you can use the dict.update()
# method:
#     dudeWMB.config.update(
#         TESTING=True,
#         SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
#     )
#
# NOTE: Configuration Keys *** MUST BE ALL IN CAPITALS ***
#       (Ask me how I know...)
#
# This first line loads config from a Python object:
#dudeWMB.config.from_object('config')
# This next one loads up our good old json object!!!
dudeWMB.config.from_file("../dudewmb.json", json.load)
# Following line disables some older stuff we don't use that is deprecated (and
# suppresses a warning about using it). Please just leave it hard-coded here.
dudeWMB.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# As recommended here:
#     https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#installation
# ... we used the "flask_sqlachemy" extension for Flask that adds support for
# SQLAlchemy to our application. It simplifies using SQLAlchemy with Flask by
#  providing useful defaults and extra helpers that make it easier to accomplish
# common tasks.
#
# Road to Enlightenment:
# Some of the things you need to know for Flask-SQLAlchemy compared to plain SQLAlchemy are:
# SQLAlchemy gives you access to the following things:
#   -> all the functions and classes from sqlalchemy and sqlalchemy.orm
#   -> a preconfigured scoped session called session
#   -> the metadata
#   -> the engine
#   -> a SQLAlchemy.create_all() and SQLAlchemy.drop_all() methods to create and drop tables according to the models.
#   -> a Model baseclass that is a configured declarative base.
# The Model declarative base class behaves like a regular Python class but has a
# query attribute attached that can be used to query the model. (Model and BaseQuery)
# We have to commit the session, but we don’t have to remove it at the end of the
# request, Flask-SQLAlchemy does that for us.
dudeWMB.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://" \
            + dudeWMB.config['DB_USER'] + ":" + dudeWMB.config['DB_PASS'] \
            + "@" \
            + dudeWMB.config['DB_SRVR'] + ":" + dudeWMB.config['DB_PORT']\
            + "/" + dudeWMB.config['DB_NAME'] + "?charset=utf8mb4"
db.init_app(dudeWMB)

# Note that in the following we use "functools.lru_cache(maxsize=128, typed=False)"
# functools is a decorator to wrap a function with a memoizing callable that saves
# up to the maxsize most recent calls. Since a dictionary is used to cache results,
# the positional and keyword arguments to the function must be hashable.It can save
# time when an expensive or I/O bound function is periodically called with the same
# arguments.
# If maxsize is set to None, the LRU feature is disabled and the cache can grow
# without bound. The LRU feature performs best when maxsize is a power-of-two.
# (See https://docs.python.org/3/library/functools.html)
@dudeWMB.route("/stations")
@functools.lru_cache(maxsize=128)
def get_stations():
    # Example with filter
    #Station.query.filter_by(stationName='SomeRandomStationName').first()
    stations = Station.query.all()  ## Returns results as a list...
    # for station in stations:
    #     print(station.id, station.number)

    # Convert individual station to dicitonary
    #station_dict = dict((col, getattr(station, col)) for col in station.__table__.columns.keys())
    stationsList = []
    for station in stations:
        stationDict = {}
        for col in station.__table__.columns.keys():
            stationDict[col] = getattr(station, col)
        stationsList.append(stationDict)

    return jsonify(stationsList)


@dudeWMB.route('/station/<int:station_id>')
def station(station_id):
    # show the station with the given id, the id is an integer
    # station = load_station(station_id)
    # Handle invalid station id...
    # if not station:
    #     abort(404)
    # return ... station stuff ....
    return 'Retrieving info for Station: {}'.format(station_id)

# @app.route("/occupancy/<int:station_id>")
# def get_occupancy(station_id):
# engine = get_db()
# df = pd.read_sql_query("select * from availability where number = %(number)s", engine, params={"number":
# station_id})
# df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')
# df.set_index('last_update_date', inplace=True)
# res = df['available_bike_stands'].resample('1d').mean()
# #res['dt'] = df.index
# print(res)
# return jsonify(data=json.dumps(list(zip(map(lambda x: x.isoformat(), res.index), res.values))))

# @app.route('/user/<id>')
# def get_user(id):
#     user = load_user(id) if not user:
#     abort(404)
#     return '<h1>Hello, %s</h1>' % user.name

# Example of setting status code:
# @app.route('/')
# def index():
#     return '<h1>Bad Request</h1>', 400

@dudeWMB.route('/')
@dudeWMB.route('/index.html')
def root():
    #print(dudeWMB.config)

    # This route simply serves 'static/index.html'
    #return app.send_static_file('index.html')
    # This route renders a template from the template folder
    return render_template('index.html', MAPS_API_KEY=dudeWMB.config["MAPS_API_KEY"])

@dudeWMB.route('/about.html')
def about():
    # This route simply serves 'static/about.html'
    #return app.send_static_file('about.html')
    # This route renders a template from the template folder
    return render_template('about.html')

# Flask will automatically remove database sessions at the end of the request or
# when the application shuts down:
@dudeWMB.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == "__main__":
    dudeWMB.run(debug=True, host=dudeWMB.config["FLASK_HOST"], port=dudeWMB.config["FLASK_PORT"])