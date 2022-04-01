
# 2022-03-31 TK/JS/WO'D; "Dude Where's My Bike" Project
#          Comp30830 Software Engineering Project

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime, timedelta
import numpy as np


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




def main():
    pass


if __name__ == '__main__':
    main()