
# 2022-03-31 TK/JS/WO'D; "Dude Where's My Bike" Project
#          Comp30830 Software Engineering Project

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime, timedelta
import numpy as np


def getResampleTimeWindowForPreviousHour(dateTimeObj):
    """Function that returns a resample time window (1 hour) based on the previous hour
    
    Returns 'resampleWindowStart' and 'resampleWindowEnd' as datetime objects
    """

    # Check if given argument is of type datetime
    if isinstance(dateTimeObj, datetime):        
        print("Trigger time was " + dateTimeObj.strftime("%Y-%m-%d, %H:%M:%S"))
    else:
        print("Error: Datatype 'datatime object' expected ")
        return
    
    # Substract one hour from the provided time
    resampleWindow = dateTimeObj - timedelta(hours = 1)
    # Set 'resample window start' to the previous full hour     
    resampleWindowStart = datetime(dateTimeObj.year, dateTimeObj.month, dateTimeObj.day, resampleWindow.hour)
    # Add one hour to obtain the 'resample window end' 
    resampleWindowEnd = resampleWindowStart + timedelta(hours = 1)
    # Return start/end of resample window as datatime objects in a tuple
    return [resampleWindowStart, resampleWindowEnd] 



def main():
    pass


if __name__ == '__main__':
    main()