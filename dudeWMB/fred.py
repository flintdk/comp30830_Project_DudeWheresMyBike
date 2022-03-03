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
    return render_template('index.html', MAPS_APIKEY=app.config["MAPS_APIKEY"]

@app.route('/station/<int:station_id>')
def station(station_id):
    # show the station with the given id, the id is an integer
    return 'Retrieving info for Station: {}'.format(station_id)

# @app.route("/stations")
# def get_stations():
#     conn = get_db()
#     # https://docs.python.org/2/library/sqlite3.html#sqlite3.Row
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     stations = []
#     rows = cur.execute("SELECT * from stations;")
#     for row in rows:
#         stations.append(dict(row))
#     return jsonify(stations=stations)

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