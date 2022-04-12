# -*- coding: utf-8 -*-
import functools
from datetime import date, datetime, timedelta
from sqlite3 import Date
from flask import Flask, g, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import gviz_api
from sqlalchemy import text
import json
from jinja2 import Template
from models import db, Station, StationState, StationStateResampled, weatherHistory
# Imports for Model/Pickle Libs
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import os, sys

import requests

def loadCredentials():
    """Load the credentials required for accessing the JCDecaux API

    Returns a JSON object with the required credentials.
    Implemented in a method as Credential storage will be subject to change.
    """
    # Our credentials are just stored in a JSON file (for now)
    # This file is not saved to GitHub and is placed on each EC2 instance
    # by a team member.
    # Load the JSON file
    file = open(os.path.join(dudeWMBParentDir, 'dudewmb.json'), 'r')
    credentials = json.load(file)
    file.close  # Can close the file now we have the data loaded...
    return credentials

# According to the article here:

# ... Python, if needing to use relative paths in order to make it easier to 
# relocate an application, one can determine the directory that a specific code
# module is located in using os.path.dirname(__file__). A full path name can then
# be constructed by using os.path.join()...
# Application Startup...
dudeWMBParentDir = os.path.dirname(os.path.dirname(__file__))
print("===================================================================")
print("DudeWMB: Application Start-up.")
print("\tDudeWMB Parent Dir. is -> " + str(dudeWMBParentDir))

# Load our private credentials from a JSON file.  Nothing runs without these...
credentials = loadCredentials()

def convertWeatherStringToModelCode(weatherString):
    """Convert the Weather string returned by the weather API to a code understood
       and accepted by our prediction model.

    Returns "scattered clouds" (a reasonable default for Ireland) if the received
    weather string is not recognised.
    """
    code = "13"
    if weatherString == 'broken clouds':
        code = 0
    elif weatherString == 'clear sky':
        code = 1
    elif weatherString == 'few clouds':
        code = 2
    elif weatherString == 'fog':
        code = 3
    elif weatherString == 'haze':
        code = 4
    elif weatherString == 'heavy intensity rain':
        code = 5
    elif weatherString == 'light intensity drizzle':
        code = 6
    elif weatherString == 'light intensity drizzle rain':
        code = 7
    elif weatherString == 'light intensity shower rain':
        code = 8
    elif weatherString == 'light rain':
        code = 9
    elif weatherString == 'mist':
        code = 10
    elif weatherString == 'moderate rain':
        code = 11
    elif weatherString == 'overcast clouds':
        code = 12
    elif weatherString == 'scattered clouds':
        code = 13

    return code

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
dudeWMB.config.from_file(os.path.join(dudeWMBParentDir, 'dudewmb.json'), json.load)
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

# Following endpoing caters for BOTH:
#   -> Current state of the stations
#   -> Predicted state of the stations at a future time.  The limit of 48 hours
#      for how far into the future we can go is introduced only by our choice of
#      weather API (and at the time of writing it's there's insufficient lead time
#      to change that).
@dudeWMB.route("/stations")
def get_stations():
    # if get_stations is called with no argument
    #   -> get station data at the current time
    # if get_stations is called with a 'four_hour_interval' argument
    #   -> get predicted station data at the time 'now plus the interval'

    hours_param = request.args.get('hours_in_future')
    if (hours_param != None):
        time_delta = int(hours_param)
    else:
        time_delta = 0  # No time delta was provided, return results as they are
                        # now....

    ########################################################################
    #      vvvvv SqlAlchemy ORM DB Access reference notes BELOW vvvvv
    ########################################################################

    # If you want to access the 'session' using SQL Alchemy - you can do so as
    # follows:
    #   db.session. ...
    # Lots of the SQLAlchemy documentation seem to use the session object whereas
    # documentation on using models appears to be lighter.
    #
    # Station.query gives you a "BaseQuery"
    # To get actual data from a "BaseQuery" you just use .all(), .first(), etc.
    # db.session.query(Station) gives you a "BaseQuery" too (same??)
    # Station.query.all() gives you a result set
    # Station.query.join(StationState).all() seems to give me a result set
    #                                        ... but it's huge and takes forever
    #                                        and eventually just times out.
    # Following are examples of filter_by (gives a BaseQuery)
    # StationState.query.filter_by(stationId=1, weatherTime='2022-02-21 12:35:27')
    # Station.query.filter_by(stationName='SomeRandomStationName').first()
    # StationState.query.filter_by(stationId=1, weatherTime='2022-02-21 12:35:27').all()

    #-----------------------------------------------------------------------
    # Tested, working above this line, in progress below
    #-----------------------------------------------------------------------

    # We can filter results using filter_by
    # db.users.filter_by(name='Joe')
    # The same can be accomplished with filter, not using kwargs, but instead using
    # the '==' equality operator, which has been overloaded on the db.users.name object:
    # db.users.filter(db.users.name=='Joe')
    # db.users.filter(or_(db.users.name=='Ryan', db.users.country=='England'))

    ########################################################################
    #      ^^^^^ SqlAlchemy ORM DB Access reference notes ABOVE ^^^^^
    ########################################################################

    # The slider on the main page sends in a 'four hour interval'.  That interval
    # is 'how far in the future' we want to get the weather from.  Now... we're
    # using the onecall API to get our weather predictions to source our future
    # weather - so this doesn't affect out actual API call.  However it does
    # tell us which weather prediction to use when calling our occupancy prediction
    # model.

    # Add our (hour-based) interval to the current datetime (.now) object...
    info_requested_for_time = datetime.now() + timedelta(hours=time_delta)

    # Retrieve the Weather Data:
    # We're using the free 'onecall' api - which returns BOTH the current weather
    # and the predicted weather in a single call.  So we make that call regardless
    # at the start of our process.  We just treat the results differently if we're
    # looking at the future (predicting availability)
    weather = {} # Declare a dict to hold the forecast weather data
    weather['temp'] = ''
    weather['humidity'] = ''
    weather['wind_speed'] = ''
    weather['description'] = ''

    uri = 'https://api.openweathermap.org/data/2.5/onecall'
    # Set the request parameters in JSON format
    parameters = {'lat': credentials['open-weather']['lat'], 'lon': credentials['open-weather']['lon'],  'exclude':'current,minutely,daily,alerts', 'appid': credentials['open-weather']['api-key']}
    weatherResponse = requests.get(uri, params=parameters)
    if (weatherResponse.status_code == 200):
        jsonWeatherData = weatherResponse.json()
        #print(jsonWeatherData)

        if time_delta == 0:
            # Use the current weather informatio:
            index_of_forecast_we_want = 0
        else:
            # We need to loop over the jsonWeatherData to get find the prediction for
            # the time window the use is interested in.  If the window is more than
            # 48 hours in the future we just return the last weather (it's our best
            # guess...)
            index_of_forecast_we_want = 0
            for idx, hourly_forecast in enumerate(jsonWeatherData['hourly']):
                forecast_time = datetime.utcfromtimestamp(hourly_forecast['dt'])
                if (forecast_time > info_requested_for_time):
                    # if the forecast time is greater than the prediction time then
                    # 'the last hourly_forecast' was the one we were interested in.
                    if idx > 0:
                        index_of_forecast_we_want = idx -1
                    break
            
        forecast = jsonWeatherData['hourly'][index_of_forecast_we_want]
        weather['temp'] = forecast['temp']
        weather['humidity'] = forecast['humidity']
        weather['wind_speed'] = forecast['wind_speed']
        weather['description'] = forecast['weather'][0]['description']
        weather['description_encoded'] = \
            convertWeatherStringToModelCode(weather['description'])
    else:
        # Our call to the API failed for some reason...  print some information
        # Who knows... someone may even look at the logs!!
        print("ERROR: Call to OpenWeather API failed with status code: ", weatherResponse.status_code)
        print("       The response reason was \'" + str(weatherResponse.reason) + "\'")

    # Calculate some of the parameters required by the predictive model.  It's
    # simpler to calculate these all the time.  Technically of course they won't
    # be used if the user has requested occupancy information for the cureent
    # time.
    weather_month = info_requested_for_time.month
    weather_day = info_requested_for_time.day
    weather_hour = info_requested_for_time.year

    # Get our list of all the stations...
    stations = Station.query.all()  ## Returns results as a list...

    # Convert individual station to dicitonary
    #station_dict = dict((col, getattr(station, col)) for col in station.__table__.columns.keys())
    stationsList = []
    for station in stations:
        # Now the fun part... the predictive model!
        # If the time_delta is greater than zero then we want to use our predictive
        # model to estimate the occupancy etc. in the future.  If not we can just
        # use the current statistics.
        if time_delta > 0:
            X_station = pd.DataFrame([[ \
                weather['temp'], weather['humidity'], weather['wind_speed'], weather['description_encoded'], \
                station.bike_stands, \
                weather_month, weather_day, weather_hour]])
            X_station.columns =[\
                'temp', 'humidity','wind_speed', 'num_desc', \
                'cal_bike_stands', \
                'weatherMonth', 'weatherDay', 'weatherHour']

            # Predictive Model - deserialization
            with open('pickles/station' + str(station.id) + '_randomForest_model.pkl', 'rb') as handle:
                model = pickle.load(handle)
                # Our model returns a numpy ndarray, hence the ".item(0)" at the
                # end, to pluck out the prediction value.
                # Also, we use int() to truncate (round down) the result as we
                # can never have a fraction of a bike available!
                randomForest_prediction = int(model.predict(X_station).item(0))
        else:
            # If we're not peering eerily into the future using our random
            # forests voodoo... then use the actual latest data...
            stationState = StationState.query.filter(StationState.stationId==station.id).order_by(text('weatherTime desc')).limit(1).all()[0]

        # Create dictionary for station-info
        stationInfo = {}
        stationInfo['id'] = station.id
        stationInfo['number'] = station.number
        stationInfo['stationName'] = station.stationName
        stationInfo['address'] = station.address
        stationInfo['latitude'] = station.latitude
        stationInfo['longitude'] = station.longitude
        if station.banking == 0:
            stationInfo['banking'] = 'Cash Machine Not Available'
        else:
            stationInfo['banking'] = 'Cash Machine Available'
        stationInfo['bike_stands'] = station.bike_stands
        stationInfo['info_supplied_for_time'] = info_requested_for_time
        # Create nested dictionary for occupancy related data
        stationInfo['occupancy'] = {}
        if time_delta == 0:
            stationInfo['occupancy']['status'] = stationState.status
            stationInfo['occupancy']['bike_stands'] = stationState.bike_stands
            stationInfo['occupancy']['available_bike_stands'] = stationState.available_bike_stands
            stationInfo['occupancy']['available_bikes'] = stationState.available_bikes
        else:
            stationInfo['occupancy']['status'] = '-'  # We don't show status for predicted times
                                                      # Perhaps address in future release?
            stationInfo['occupancy']['bike_stands'] = station.bike_stands
            stationInfo['occupancy']['available_bike_stands'] = station.bike_stands - randomForest_prediction
            stationInfo['occupancy']['available_bikes'] = randomForest_prediction

        # Creating nested dictionary for weather related data
        # THIS MIGHT SEEM WASTEFUL (i.e. why attach weather to a station if all
        # the stations are nearby?)  However we took the view that if this
        # application was used nationally, it would be far more likely the weather
        # would differ from station to station.  Yes - we would have to update how
        # we sourced the weather data.  However our json model and the front end
        # would already be capable of handling the data if send from the back end.
        stationInfo['weather'] = weather
 
        stationsList.append(stationInfo)

    return jsonify(stationsList)

##########################################################################################
##########################################################################################

@dudeWMB.route("/occupancy/<int:station_id>")
def get_occupancy(station_id):

    cutoffDatetime = datetime.now() - timedelta(weeks=1)
    # .filter() and .filter_by:
    # Both are used differently;
    # .filters can write > < and other conditions like where conditions for sql,
    # but when referring to column names, you need to use class names and attribute
    # names.
    # .filter_by can pass conditions using python’s normal parameter passing method,
    # and no additional class names need to be specified when specifying column names.
    # The parameter name corresponds to the attribute name in the name class, but does
    # not seem to be able to use conditions such as > < etc..
    # Each has its own strengths.http://docs.sqlalchemy.org/en/rel_0_7&#8230;

    stStReQuery = StationStateResampled.query
    stStReQuery = stStReQuery.filter(StationStateResampled.stationId == station_id)
    stStReQuery = stStReQuery.filter(StationStateResampled.weatherHour > cutoffDatetime)
    stStReQuery = stStReQuery.order_by(text('weatherHour asc'))

    # Add column headers for our Google Charts chart...
    # Create a schema for our gviz DataTable
    gvizSchema = {'weatherHour': ('datetime', 'Date/Time'), \
                  'available_bikes': ('number', 'Available Bikes')}
    
    occupancyList = []
    for record in stStReQuery.all():
        # What am I missing - why is it stooopid hard to convert an SQLAlchemy
        # model to a dict??

        # A Google Chart histogram appears to accept only two input columns (i.e.
        # we can't send out a chunk of data and just select specific columns to
        # chart...)
        recordInfo = {'weatherHour': record.weatherHour, \
                      'available_bikes': record.available_bikes}
        occupancyList.append(recordInfo)
    
    # Create a data table:
    gvizDataTable = gviz_api.DataTable(gvizSchema, occupancyList)
    response = gvizDataTable.ToJSonResponse(columns_order=("weatherHour", "available_bikes"))
    # I'm not sure why... but I'm under time pressure and can't explore further;
    # -> The ToJSonResponse function seems to wrap the useful JSON in some redundant
    #    text.  I assuming I've skipped a beat somewhere - but for now the expedient
    #    solution has to win...
    startIndex = response.index(':{') + 1
    endIndex   = response.rindex(",\"status\":\"ok\"});")
    jsonText = response[startIndex:endIndex]

    return jsonText

##########################################################################################
##########################################################################################

# Note that in the following we use "functools.lru_cache(maxsize=128, typed=False)"
# functools is a decorator to wrap a function with a memoizing callable that saves
# up to the maxsize most recent calls. Since a dictionary is used to cache results,
# the positional and keyword arguments to the function must be hashable.It can save
# time when an expensive or I/O bound function is periodically called with the same
# arguments.
# If maxsize is set to None, the LRU feature is disabled and the cache can grow
# without bound. The LRU feature performs best when maxsize is a power-of-two.
# (See https://docs.python.org/3/library/functools.html)
@dudeWMB.route('/station/<int:station_id>')
@functools.lru_cache(maxsize=128)
def station(station_id):
    # show the station with the given id, the id is an integer
    # station = load_station(station_id)
    # Handle invalid station id...
    # if not station:
    #     abort(404)
    # return ... station stuff ....
    # ********************* NOT IMPLEMENTED *****************************
    return 'Retrieving info for Station: {}'.format(station_id)


##########################################################################################
##########################################################################################
# Flask will automatically remove database sessions at the end of the request or
# when the application shuts down:
@dudeWMB.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
    # sys.stdout.close()  # Close the file handle we have open
    # sys.stdout = sys.__stdout__ # Reset to the standard output

if __name__ == "__main__":
    # Reassign stdout so any debugs etc. generated by flask won't be lost when
    # running as a service on EC2
    # sys.stdout = open('dwmb_Flask_.logs', 'a')

    # print("DWMB Flask Application is starting: " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    dudeWMB.run(debug=False, host=dudeWMB.config["FLASK_HOST"], port=dudeWMB.config["FLASK_PORT"])