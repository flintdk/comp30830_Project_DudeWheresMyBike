from opcode import hasconst
import requests
import json
from pprint import pprint
from IPython.display import JSON
import sqlalchemy

payload = {'key1': 'value1', 'key2': 'value2',
           'key3': 'value3', 'key4': 'value4'}
URI = 'https://bla'
r = requests.get('URI', params=payload)
print r.url


if len(sys.argv) > 1:
    username = sys.argv[1]
    else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()
    scope = 'user-top-read'
    token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    ranges = ['short_term', 'medium_term', 'long_term']
for range in ranges:
    print("range:", range)
    results = sp.current_user_top_tracks(time_range=range, limit=50)
for i, item in enumerate(results['items']):
    print(i, item['name'], '//', item['artists'][0]['name'])
    print()

    
    Station:
    https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=
    https://api.jcdecaux.com/vls/v1/stations/10?contract=dublin&apiKey=
    Resonse when contract exitst: http/1.1 200 OK
    Content-type: application/json
    Response when not: http/1.1 400 Bad Request

APIKEY = “secret”
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,
    "contract": NAME})

    Dynamic Data:


def main():
# run forever...
while True:
    try:
        r = requests.get(STATIONS,
        params={"apiKey": APIKEY, "contract": NAME})
        store(json.loads(r.text))
        # now sleep for 5 minutes
        time.sleep(5*60)
    except:
        # if there is any problem, print the traceback
        print traceback.format_exc()
    return

conda install sqlalchemy
conda install -c anaconda mysql-connector-python
    sqlalchemy
# default
engine = create_engine('mysql://scott:tiger@localhost/foo')
# mysql-python
engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')
# MySQL-connector-python
engine = create_engine('mysql+mysqlconnector://scott:tiger@localhost/foo')
# OurSQL
engine = create_engine('mysql+oursql://scott:tiger@localhost/foo')


    engine = create_engine(“mysql+mysql-connector://
admin:pass@dbikes.ci1fi3edpsps.eu-west-1.rds.amazonaws.com/
dbikes:3306”)
connection = engine.connect()
result = connection.execute("select username from users")
for row in result:
print("username:", row['username'])
connection.close()