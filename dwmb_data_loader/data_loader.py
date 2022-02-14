# 2022-02-14 TK/JS/WO'D; "Dude Where's My Bike" Project
#          Comp30830 Software Engineering 
"""
PseudoCode Solution:

define a function which
    return 

define a main function
    print finished.

if script is being run as a script (not imported) call main() function

"""

import sys
import requests
import json
import traceback
import sqlalchemy as db

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

def saveToDatabase(jsonData, credentials):
    connectionString = "mysql+mysqlconnector://" \
        + credentials['amazonrds']['username'] + ":" + credentials['amazonrds']['password'] \
        + "@" \
        + credentials['amazonrds']['endpoint'] + ":3306" \
        + "/dudeWMB?charset=utf8mb4"
    print("Connection String: " + connectionString)
    engine = db.create_engine(connectionString)

    connection = engine.connect()
    result = connection.execute("select * from Users")
    for row in result:
        print("firstname:", row['firstname'], "lastname:", row['lastname'])
    connection.close()

    return

def main():
    """Load Data from the JCDecaux API


    """
    credentials = loadCredentials()

    # "username": "tomas.kelly1@ucdconnect.ie",
        # "password": "lD6>hD4_aP2+yV6?",
        # "api-key": "39fa6066a9e6c316e1bb1f4acaa31b1af3b73c05"

    try:
        # Retrieve the Station/Activity Data:
        # Set the request parameters in JSON format
        parameters = {'contract': 'dublin', 'apiKey': credentials['jcdecaux']['api-key']}
        # Hard-code the Station Data URI
        uri = 'https://api.jcdecaux.com/vls/v1/stations'
        response = requests.get(uri, params=parameters)
    
        if (response.status_code == 200):
            # response.content  # Bytes
            # response.text  # String
            saveToDatabase(response.json(), credentials)
        else:
            # Our call to the API failed for some reason...  print some information
            # Who knows... someone may even look at the logs!!
            print("ERROR: Call to JCDecaux API failed with status code: ", response.status_code)
            print("       The response reason was \'" + str(response.reason) + "\'")

    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())
    
    print('\r\nFinished!')
    sys.exit()

if __name__ == '__main__':
    main()