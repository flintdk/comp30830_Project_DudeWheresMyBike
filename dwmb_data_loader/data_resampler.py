
# 2022-03-31 TK/JS/WO'D; "Dude Where's My Bike" Project
#          Comp30830 Software Engineering Project

import sys
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import sqlalchemy as db

#------------------------------------------------------------------------------------------
# Function to yield the resample time window of the previous hour based on provided datetime object 
#------------------------------------------------------------------------------------------    
def getResampleTimeWindowForPreviousHour(dateTimeObj):

    if isinstance(dateTimeObj, datetime):        
        print("Trigger time was " + dateTimeObj.strftime("%Y-%m-%d, %H:%M:%S"))
    else:
        print("Error: Datatype 'datatime object' expected ")
        sys.exit()
    
    # If the trigger was just arround midnight, then we need to handle this individually!
    if dateTimeObj.hour == 0:

        # Substract one hour from the provided time
        resampleWindow = dateTimeObj - timedelta(hours = 1)
        # At midnight we need to consider the day when setting WindowStart
        # e.g given time: 00:15:00 --> 23:00:00
        resampleWindowStart = datetime(dateTimeObj.year, dateTimeObj.month, resampleWindow.day, resampleWindow.hour)
        resampleWindowEnd = resampleWindowStart + timedelta(hours = 1)

    # In any other hour but midnight we can merely subract one hour. That's it!
    else:
        # Substract one hour from the provided time
        resampleWindow = dateTimeObj - timedelta(hours = 1)
        # Use the given date but only use previous hour instead of entire time
        # e.g given time: 11:15:00 --> 10:00:00
        resampleWindowStart = datetime(dateTimeObj.year, dateTimeObj.month, dateTimeObj.day, resampleWindow.hour)
        resampleWindowEnd = resampleWindowStart + timedelta(hours = 1)
    
    return [resampleWindowStart, resampleWindowEnd] 



#------------------------------------------------------------------------------------------
# Function to to downsample collected station-state data from 2min to 1h intervals 
#------------------------------------------------------------------------------------------    
def resampleStationStateHourly(connectionString):
    """Function to downsample data 'station-state' from 30 samples to 1 sample per hour"""
   
    # Create data-frame variables in outer function so that it can be accessed in inner functions
    df = pd.DataFrame()
    df_resampled = pd.DataFrame()
    
    # That's the time we started collecting occopancy data
    firstRecordDateTime = datetime(2022, 2, 22, 12, 53, 25)

    # The create_engine() function produces an Engine object based on a URL
    engine = db.create_engine(connectionString)
   
    #------------------------------------------------------------------------------------------
    # Inner function to delete all rows in resampled table
    #------------------------------------------------------------------------------------------    
    def deleteRowsInResampledTable(dbConnection):
        dbConnection.execute(
            db.text("Delete FROM dudeWMB.stationStateResampled where ID <> 0;"))

    #------------------------------------------------------------------------------------------
    # Inner function to get date & time of latest sample
    #------------------------------------------------------------------------------------------    
    def getDateTimeLatestSample(dbConnection):

        nonlocal firstRecordDateTime
        
        # Query latest tuple from RDS that is has already been resampled
        result = dbConnection.execute(
        db.text("SELECT * FROM dudeWMB.stationStateResampled ORDER BY stationId, weatherHour DESC LIMIT 1;"))
        for tuple in result: # iterate over results - although only one tuple is expected
            dateTimeSample = tuple['weatherHour']
            break
        else:
            # If table 'stationStateResampled' is empty then use date were data collection began
            dateTimeSample = firstRecordDateTime

        return dateTimeSample

    #------------------------------------------------------------------------------------------
    # Inner function to query entire data set
    #------------------------------------------------------------------------------------------    
    def queryEntireData(dbConnection):

        # define variables which aren't local in this inner function
        nonlocal df
        nonlocal engine
        
        # Intialise data frame
        df = pd.DataFrame()   
        # Read entire table 'stationState' and store it in data frame
        df = pd.read_sql_table('stationState', dbConnection)
    
    #------------------------------------------------------------------------------------------
    # Inner function to query data per hour
    #------------------------------------------------------------------------------------------    
    def queryHourlyData(dbConnection, timeObj):
        """Inner function to query data from the 'stationState' table
        
        DRY principle - Don't Repeat Yourself - that's why we user inner functions
        """
        
        # define variables which aren't local in this inner function
        nonlocal df
        nonlocal engine
        
        df = pd.DataFrame()
        
        # Get resampling time window for previous hour as tuple [WindowStart, WindowEnd]
        resampleWindow = getResampleTimeWindowForPreviousHour(timeObj)
        
        # Convert time windows from datetime object to string
        resampleWindowStartStr = resampleWindow[0].strftime("%Y-%m-%d %H:%M:%S")
        resampleWindowStartStr
        resampleWindowEndStr = resampleWindow[1].strftime("%Y-%m-%d %H:%M:%S")
        resampleWindowEndStr
        print("Resample window start: " + str(resampleWindow[0]))
        print("Resample window end: " + str(resampleWindow[1]))
                  
        # Create SQL query string to query data from the 'stationState' table
        sqlQuery = "select * from dudeWMB.stationState where weatherTime > '"\
            + resampleWindowStartStr + "' and weatherTime < '" + resampleWindowEndStr + "'"

        # TODO - implement some error handling using try & execpt
        
        # Query all given data for the specified hour and store in a pandas dataframe 
        df = pd.read_sql(sqlQuery, dbConnection)
        
    #------------------------------------------------------------------------------------------
    # Inner function to resample data per hour 
    #------------------------------------------------------------------------------------------    
    def resampleHourlyData(dbConnection):
        """Inner function to resample the obtained data from the 'stationState' table
        
        DRY principle - Don't Repeat Yourself - that's why we user inner functions
        """
                                      
        # define variables which aren't local in this inner function
        nonlocal df
        nonlocal df_resampled

        # Downsample occupancy data from 30 samples per hour to 1 sample per hour for each station individually

        # Initialise data frame
        df_resampled = pd.DataFrame()

        # Make sure data frame isn't empty
        # This could happen if there is a gap in the data. Then the query would return a empty data frame
        if df.shape[0] != 0:

            df['weatherTime'] = pd.to_datetime(df['weatherTime'])

            df_resampled = df.groupby(['stationId']).resample('60min', on='weatherTime').apply({"available_bike_stands":"mean", "available_bikes":"mean", "status":"first"})
            df_resampled = df_resampled.round({'available_bike_stands': 0, 'available_bikes': 0})
            # Convert the new multiIndex back to a regular index by dropping the top
            # level and converting it into a column
            #   -> level=0 only removes level zero from the multiindex
            # Dropping the first element of the mulitIndex (stationId) and turning it into a column
            df_resampled = df_resampled.reset_index(level=0, drop=False)
            # Then generate a new column from the index to create new column labeled 'weatherHour'
            df_resampled['weatherHour']=df_resampled.index
            # Now drop the wierd looking index and set it back to numeric
            # --> Getting rid of the weatherTime within the index and turn into a regular index
            df_resampled = df_resampled.reset_index(level=0, drop=True)
            

    #------------------------------------------------------------------------------------------
    # Inner function to write data per hour to RDS
    #------------------------------------------------------------------------------------------    
    def writeHourlyData(dbConnection):
        """Inner function to write resampled data to the 'stationStateResampled' table
        
        DRY principle - Don't Repeat Yourself - that's why we user inner functions
        """

        # define variables which aren't local in this inner function
        nonlocal df_resampled
        
        if df_resampled.shape[0] != 0:
            try:
                with engine.begin() as connection:                   
                    df_resampled.to_sql('stationStateResampled', con=connection,\
                        schema='dudeWMB', index=False, if_exists='append')
                    print(">>> Writing to RDS was successful!")
            except Exception as e:
                print(">>> Something went wrong while writing to RDS!")
                
    #------------------------------------------------------------------------------------------
    # Resampling control
    #------------------------------------------------------------------------------------------    
    with engine.begin() as dbConnection:

        # Get current time
        timeNow = datetime.now()
        print("Time now: " + str(timeNow))
        # Get last sample time
        lastSampleDate = getDateTimeLatestSample(dbConnection)
        print("Last sample date:" + str(lastSampleDate))    

        # Downsampling collected data from a 2min interval to a 1hour interval.
        # Iterating over every day and hour that is listed in the 'stationState' table - this includes all stations in one single fetch
        # Two scenarios:
        # 1) If 'stationStateResampled' table is completely empty, then start resampling from 'firstRecordDateTime' - the time when data recording began
        # 2) Pick up where we've left off last time and resample data until now. 
        while lastSampleDate < datetime.now() - timedelta(hours  = 1):

            print("-------------------------------------------------------------")
            lastSampleDate = lastSampleDate + timedelta(hours  = 1)
            queryHourlyData(dbConnection, lastSampleDate)
            resampleHourlyData(dbConnection)
            print("Length data frame resampled: " + str(df_resampled.shape[0]))
            if df_resampled.shape[0] != 0:
                writeHourlyData(dbConnection)
            print("-------------------------------------------------------------")






def main():
    pass


if __name__ == '__main__':
    main()