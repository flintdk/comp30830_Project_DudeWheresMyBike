# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import requests
import traceback
import sqlalchemy as db
from data_loader import loadCredentials

#===============================================================================
#===============================================================================
#===============================================================================

def main():
    """Resample the data retrieved from JCDecaux to be hourly

    Resample Data collected every two minutes to Hourly Data
    We aggregate the data for each hour using the pandas .resample() method.
    To aggregate or temporal resample the data for a time period, you can take
    all of the values for that period and summarize them.  In this case, we want
    mean availability, etc. figures so we use the resample() method together with .mean().

    df.resample('D').mean()
    #####################################The 'D' specifies that you want to aggregate, or resample, by day.
    """
    # We want to timestamp our records so we can tie station state to
    # weather data etc..  So we generate a timestamp now at the beginning of
    # this 'Data Load' pass and use it a couple of times below:
    timestamp = datetime.now()
    timestampAsStr = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    print("DWMB_Data_Resampler: Start of process (" + timestampAsStr + ")")

    print("\tLoading credentials.")
    # Load our private credentials from a JSON file
    credentials = loadCredentials()

    print("\tRegistering start with cronitor.")
    # The DudeWMB Data Loader uses the 'Cronitor' web service (https://cronitor.io/)
    # to monitor the running data loader process.  This way if there is a failure
    # in the job etc. our team is notified by email.  In addition, if the job
    # or the EC2 instance suspends for some reason, cronitor informs us of the 
    # lack of activity so we can log in and investigate.
    # Send a request to log the start of a run
    cronitorURI = credentials['cronitor']['TelemetryURLSampler']
    requests.get(cronitorURI + "?state=run")

    try:
        print("\tCreating SQLAlchemy db engine.")
        # We only want to initialise the engine and create a db connection once
        # as its expensive (i.e. time consuming). So we only want to do that once
        connectionString = "mysql+mysqlconnector://" \
            + credentials['DB_USER'] + ":" + credentials['DB_PASS'] \
            + "@" \
            + credentials['DB_SRVR'] + ":" + credentials['DB_PORT']\
            + "/" + credentials['DB_NAME'] + "?charset=utf8mb4"
        #print("Connection String: " + connectionString + "\n")
        engine = db.create_engine(connectionString)

        # engine.begin() runs a transaction
        with engine.begin() as connection:


                print("\tSaving station data to database.")
                saveStationDataToDb(connection, stationResponse.json(), timestampAsStr)
            else:
                # Our call to the API failed for some reason...  print some information
                # Who knows... someone may even look at the logs!!
                print("ERROR: Call to JCDecaux API failed with status code: ", stationResponse.status_code)
                print("       The response reason was \'" + str(stationResponse.reason) + "\'")

        
        # Make sure to close the connection - a memory leak on this would kill
        # us...
        connection.close()

        print("\tRegistering completion with cronitor.")
        # Send a Cronitor request to signal our process has completed.
        requests.get(cronitorURI + "?state=complete")

    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())
        print("\tRegistering error with cronitor.")
        # Send a Cronitor request to signal our process has failed.
        requests.get(cronitorURI + "?state=fail")

    # (following returns a timedelta object)
    elapsedTime = datetime.now() - timestamp
    
    # returns (minutes, seconds)
    #minutes = divmod(elapsedTime.seconds, 60) 
    minutes = divmod(elapsedTime.total_seconds(), 60) 
    print('\tIteration Complete! (Elapsed time:', minutes[0], 'minutes',
                                    minutes[1], 'seconds)\n')
    sys.exit()

if __name__ == '__main__':
    main()