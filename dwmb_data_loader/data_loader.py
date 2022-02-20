# 2022-02-14 TK/JS/WO'D; "Dude Where's My Bike" Project
#          Comp30830 Software Engineering Project
"""
PseudoCode Solution:

define a function which
    return 

define a main function
    print finished.

if script is being run as a script (not imported) call main() function

"""

from sqlite3 import complete_statement
import sys
import requests
import json
import traceback
import sqlalchemy as db
from datetime import datetime

def loadCredentials():
    """Load the credentials required for accessing the JCDecaux API

    Returns a JSON object with the required credentials.
    Implemented in a method as Credential storage will be subject to change.
    """
    # Our credentials are just stored in a JSON file (for now)
    # This file is not saved to GitHub and is placed on each EC2 instance
    # by a team member.
    # Load the JSON file
    file = open('dudewmb.json')
    credentials = json.load(file)
    file.close  # Can close the file now we have the data loaded...
    return credentials

#===============================================================================
#===============================================================================
#===============================================================================

def saveStationDataToDb(connection, jsonData, timestamp):
    """
    """
    # Station Data:
    # number ('Id'), contract_name, name, address, position {lat, lng}, banking, bonus
    # (banking indicates whether this station has a payment terminal,
    #  bonus indicates whether this is a bonus station)
    # Availability Data (For station)
    # number ('Id'), bike_stands, available_bike_stands, available_bikes, status, last_update

    # Look over the jsonData, which contains a both static and dynamic information
    # in a big soup...
    for row in jsonData:

        # Each row contains both 'Station' (almost static) data AND activity
        # data for that station.  I seperate them out just to make the code
        # more legible
        station = extractStation(row)
        stationSate = extractStationState(row)

        # Would prefer to use ORM rather than straight SQL - but the
        # priority for now is to have something working. Will return to this
        # if time (and the burndown chart) permits...
        # Session = db.sessionmaker(bind=engine)
        # session = Session()

        # Have we already stored this station?
        if (stationExists(connection, station)):
            # If the stationExists we update it
            # (It's not efficient to update every time... but... yeah...)
            updateStation(connection, station)
        else:
            insertStation(connection, station)

        # Whether we inserted or updated - doesn't matter - the station
        # definitely exists now.  Look up the id so we can insert the detail
        # record...
        stationId = getStationId(connection, station)
        
        # Once we're confident the station exists and is up to date we insert
        # the Status Updata data for this station!
        insertStationState(connection, stationId, timestamp, stationSate)

    return

def stationExists(connection, station):
    """This function checks if station is already listed in the station table

    Returns True if stations already exists
    """
    stationExists = True
    query = db.text("SELECT * from station "
        + "where number = " + str(station['number']) + " "\
        + "and contractName = 'dublin';")
    id_count = connection.execute(query).rowcount # count returned tuples of exisiting stations
    if (id_count == 0):
        stationExists = False
    return stationExists

def getStationId(connection, station):
    """This function returns the station-ID, where ID is the primary key in the station table

    Note: Station-ID is the primary key of the station table and is created by utilising the autoincrement option. 
    This Station-ID is used to uniquely identify a station within the database, 
    since the station number which is returned by the JCDecaux is only unique in combination with the contractName.
    """
    stationId = 0
    count = 0
    result = connection.execute(
        db.text("SELECT ID from station " \
            + "where number = " + str(station['number']) + " "\
            + "and contractName = 'dublin';")
    )
    for tuple in result: # iterate over results - although only one tuple is expected
        stationId = tuple['ID']
        count += 1
    if count != 1: # if more than one tuple is returned, then there is something wrong.
        stationId = 0
        print("Invalid number of tuples!")
    return stationId

def updateStation(connection, station):
    """This function updates the static information of a bike station in the 'station' table
    
    Note: Should static information such as banking, bonus, etc. change over time, 
    this function will update the information for each individual station 
    """
    connection.execute(
        db.text("UPDATE station " \
            + "SET stationName = \"" + station['name'] + "\", " \
            + "address = \"" + station['address'] + "\", " \
            + "latitude = " + str(station['lat']) + ", " \
            + "longitude = " + str(station['lng']) + ", " \
            + "banking = " + str(station['banking']) + ", " \
            + "bonus = " + str(station['bonus']) + " " \
            + "WHERE number = " + str(station['number']) + " " \
            + "and contractName = \"dublin\";")
    )
    return

def insertStation(connection, station):
    """This function inserts a new station to the table in the 'station' table

    """
    connection.execute(
        db.text("INSERT station " \
            + "SET number = " + str(station['number']) + ", " \
            + "contractName = \"dublin\", " \
            + "stationName = \"" + station['name'] + "\", " \
            + "address = \"" + station['address'] + "\", " \
            + "latitude = " + str(station['lat']) + ", " \
            + "longitude = " + str(station['lng']) + ", " \
            + "banking = " + str(station['banking']) + ", " \
            + "bonus = " + str(station['bonus']) + ";")
    )
    return

def insertStationState(connection, stationId, timestamp, stationSate):
    """This function inserts the latest dynamic information about a bike station to the table 'sationState' 
    
    """
    connection.execute(
        db.text("INSERT stationState " \
            + "SET stationId = " + str(stationId) + ", " \
            + "weatherTime = \"" + str(timestamp) + "\", " \
            + "status = \"" + stationSate['status'] + "\", " \
            + "bike_stands = " + str(stationSate['bike_stands']) + ", " \
            + "available_bike_stands = " + str(stationSate['available_bike_stands']) + ", " \
            + "available_bikes = \"" + str(stationSate['available_bikes']) + "\", " \
            + "lastUpdate = " + str(stationSate['last_update']) + ";")
    )

    return

#===============================================================================
#===============================================================================
#===============================================================================

def saveWeatherDataToDb(connection, jsonData, timestamp):
    """
    """
    # Station Data:
    # number ('Id'), contract_name, name, address, position {lat, lng}, banking, bonus
    # (banking indicates whether this station has a payment terminal,
    #  bonus indicates whether this is a bonus station)
    # Availability Data (For station)
    # number ('Id'), bike_stands, available_bike_stands, available_bikes, status, last_update

    # The Weather json object is relatively complex.  Extract the data we require
    # from it and pop it in a simpl dictionary.
    weather = extractWeather(jsonData)

    connection.execute(
        db.text("INSERT weatherHistory " \
            + "SET weatherTime = \"" + str(timestamp) + "\", " \
            + "latitude = " + str(weather['latitude']) + ", " \
            + "longitude = " + str(weather['longitude']) + ", " \
            + "main = \"" + weather['main'] + "\", " \
            + "description = \"" + weather['description'] + "\", " \
            + "temp = " + str(weather['temp']) + ", " \
            + "feels_like = " + str(weather['feels_like']) + ", " \
            + "temp_min = " + str(weather['temp_min']) + ", " \
            + "temp_max = " + str(weather['temp_max']) + ", " \
            + "pressure = " + str(weather['pressure']) + ", " \
            + "humidity = " + str(weather['humidity']) + ", " \
            + "sea_level = " + str(weather['sea_level']) + ", " \
            + "grnd_level = " + str(weather['grnd_level']) + ", " \
            + "wind_speed = " + str(weather['wind_speed']) + ", " \
            + "wind_deg = " + str(weather['wind_deg']) + ", " \
            + "wind_gust = " + str(weather['wind_gust']) + ", " \
            + "clouds_all = " + str(weather['clouds_all']) + ", " \
            + "country = \"" + weather['country'] + "\";")
        )

    return

#===============================================================================
#===============================================================================
#===============================================================================

def extractStation(jsonRow):
    """This function extracts static station information from a json object and stores it in a Python dictionary 
    
    """
    station = {} # Declare a dict to hold the station data
    station['number'] = jsonRow['number']
    station['contract_name'] = jsonRow['contract_name']
    station['name'] = jsonRow['name']
    station['address'] = jsonRow['address']
    station['lat'] = jsonRow['position']['lat']
    station['lng'] = jsonRow['position']['lng']
    station['banking'] = jsonRow['banking']
    station['bonus'] = jsonRow['bonus']

    return station

def extractStationState(jsonRow):
    """This function extracts dynamic station information from a json object and stores it in a Python dictionary 
    
    """
    stationState = {} # Declare a dict to hold the station data
    stationState['number'] = jsonRow['number']
    stationState['bike_stands'] = jsonRow['bike_stands']
    stationState['available_bike_stands'] = jsonRow['available_bike_stands']
    stationState['available_bikes'] = jsonRow['available_bikes']
    stationState['status'] = jsonRow['status']
    stationState['last_update'] = jsonRow['last_update']

    return stationState

def extractWeather(jsonData):
    """This function extracts weather information from a json object and stores it in a Python dictionary 
    
    """
    weather = {} # Declare a dict to hold the station data
    weather['latitude'] = jsonData['coord']['lat']
    weather['longitude'] = jsonData['coord']['lon']
    weather['main'] = jsonData['weather'][0]['main']
    weather['description'] = jsonData['weather'][0]['description']
    weather['temp'] = jsonData['main']['temp']
    weather['feels_like'] = jsonData['main']['feels_like']
    weather['temp_min'] = jsonData['main']['temp_min']
    weather['temp_max'] = jsonData['main']['temp_max']
    weather['pressure'] = jsonData['main']['pressure']
    weather['humidity'] = jsonData['main']['humidity']
    weather['sea_level'] = jsonData['main']['sea_level']
    weather['grnd_level'] = jsonData['main']['grnd_level']
    weather['wind_speed'] = jsonData['wind']['speed']
    weather['wind_deg'] = jsonData['wind']['deg']
    weather['wind_gust'] = jsonData['wind']['gust']
    weather['clouds_all'] = jsonData['clouds']['all']
    weather['country'] = jsonData['sys']['country']

    return weather

#===============================================================================
#===============================================================================
#===============================================================================

def main():
    """Load Data from the JCDecaux API


    """
    # Load our private credentials from a JSON file
    credentials = loadCredentials()

    # The DudeWMB Data Loader uses the 'Cronitor' web service (https://cronitor.io/)
    # to monitor the running data loader process.  This way if there is a failure
    # in the job etc. our team is notified by email.  In addition, if the job
    # or the EC2 instance suspends for some reason, cronitor informs us of the 
    # lack of activity so we can log in and investigate.
    # Send a request to log the start of a run
    cronitorURI = credentials['cronitor']['TelemetryURL']
    requests.get(cronitorURI + "?state=run")

    # "username": "tomas.kelly1@ucdconnect.ie",
        # "password": "lD6>hD4_aP2+yV6?",
        # "api-key": "39fa6066a9e6c316e1bb1f4acaa31b1af3b73c05"

    try:
        # We want to timestamp our records so we can tie station state to
        # weather data etc..  So we generate a timestamp now at the beginning of
        # this 'Data Load' pass and use it a couple of times below:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # We only want to initialise the engine and create a db connection once
        # as its expensive (i.e. time consuming). So we only want to do that once
        connectionString = "mysql+mysqlconnector://" \
            + credentials['amazonrds']['username'] + ":" + credentials['amazonrds']['password'] \
            + "@" \
            + credentials['amazonrds']['endpoint'] + ":3306" \
            + "/dudeWMB?charset=utf8mb4"
        #print("Connection String: " + connectionString + "\n")
        engine = db.create_engine(connectionString)

        # engine.begin() runs a transaction
        with engine.begin() as connection:

            # Retrieve the Station/Activity Data:
            # Hard-code the Station Data URI
            uri = 'https://api.jcdecaux.com/vls/v1/stations'
            # Set the request parameters in JSON format
            parameters = {'contract': 'dublin', 'apiKey': credentials['jcdecaux']['api-key']}
            stationResponse = requests.get(uri, params=parameters)
        
            if (stationResponse.status_code == 200):
                # response.content  # Bytes
                # response.text  # String
                saveStationDataToDb(connection, stationResponse.json(), timestamp)
            else:
                # Our call to the API failed for some reason...  print some information
                # Who knows... someone may even look at the logs!!
                print("ERROR: Call to JCDecaux API failed with status code: ", stationResponse.status_code)
                print("       The response reason was \'" + str(stationResponse.reason) + "\'")

            # Retrieve the Weather Data:
            # Hard-code the Station Data URI
            uri = 'https://api.openweathermap.org/data/2.5/weather'
            # Set the request parameters in JSON format
            parameters = {'lat': credentials['open-weather']['lat'], 'lon': credentials['open-weather']['lon'], 'appid': credentials['open-weather']['api-key']}
            weatherResponse = requests.get(uri, params=parameters)
        
            if (weatherResponse.status_code == 200):
                # response.content  # Bytes
                # response.text  # String
                saveWeatherDataToDb(connection, weatherResponse.json(), timestamp)
            else:
                # Our call to the API failed for some reason...  print some information
                # Who knows... someone may even look at the logs!!
                print("ERROR: Call to JCDecaux API failed with status code: ", weatherResponse.status_code)
                print("       The response reason was \'" + str(weatherResponse.reason) + "\'")
        
        # Make sure to close the connection - a memory leak on this would kill
        # us...
        connection.close()

        # Send a Cronitor request to signal our process has completed.
        requests.get(cronitorURI + "?state=complete")

    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())
        # Send a Cronitor request to signal our process has failed.
        requests.get(cronitorURI + "?state=fail")
    
    print('\r\nFinished!')
    sys.exit()

if __name__ == '__main__':
    main()