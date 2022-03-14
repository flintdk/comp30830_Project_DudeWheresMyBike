import functools
from flask import Flask, g, render_template, jsonify
import json
from jinja2 import Template

# Create our flask app.
# Static files are server from the 'static' directory
app = Flask(__name__, static_url_path='')
app.config.from_object('config')

def connect_to_database():
# implement code as required
    pass

# This route simply serves 'static/index.html'
@app.route('/')
def root():
    return render_template('index.html', MAPS_APIKEY=app.config["MAPS_APIKEY"])

@app.route('/station/<int:station_id>')
def station(station_id):
    # show the station with the given id, the id is an integer
    return 'Retrieving info for Station: {}'.format(station_id)

# Note that in the following we use "functools.lru_cache(maxsize=128, typed=False)"
# functools is a decorator to wrap a function with a memoizing callable that saves
# up to the maxsize most recent calls. Since a dictionary is used to cache results,
# the positional and keyword arguments to the function must be hashable.It can save
# time when an expensive or I/O bound function is periodically called with the same
# arguments.
# If maxsize is set to None, the LRU feature is disabled and the cache can grow
# without bound. The LRU feature performs best when maxsize is a power-of-two.
# (See https://docs.python.org/3/library/functools.html)
@app.route("/stations")
@functools.lru_cache(maxsize=128)
def get_stations():
    conn = get_db()
    # https://docs.python.org/2/library/sqlite3.html#sqlite3.Row
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    stations = []
    rows = cur.execute("SELECT * from stations;")
    for row in rows:
        stations.append(dict(row))
    return jsonify(stations=stations)

    engine = get_db()
    sql = "select * from station;"
    rows = engine.execute(sql).fetchall()
    print('#found {} stations', len(rows))
    return jsonify(stations=[dict(row.items()) for row in rows])

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

# Example of template:
# template = Template('Hello {{ name }}!')
# print(template.render(name='John Doe'))
#<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='bootstrap/bootstrap.min.css') }}">

@app.route("/")
# def hello():
#     return "Hello World!"
def root():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)