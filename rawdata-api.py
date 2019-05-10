
from flask import Flask, jsonify
from flaskext.mysql import MySQL
import requests

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Jirayu1001'
app.config['MYSQL_DATABASE_DB'] = 'sensor_data'
app.config['MYSQL_DATABASE_HOST'] = '35.193.167.78'
mysql.init_app(app)

@app.route('/sensors/')
def allsensors():
    api_data = []
    cur = mysql.connect().cursor()
    cur.execute("SELECT sensorAPI FROM userdata")
    api_data = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]

    sensor_data = []
    if len(api_data) != 0:
        for i in range(len(api_data)):
            api = api_data[i]["sensorAPI"]
            if len(api) != 0:
                response = requests.get(api)
                sensor_data.append(response.json())

        return jsonify(sensor_data)
    return "No data"

@app.route('/sensors/project_id/<project_id>')
def list_by_project(project_id=None):
    api_data = []
    cur = mysql.connect().cursor()
    cur.execute("SELECT sensorAPI FROM userdata where projectID = %s", project_id)
    api_data = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]

    sensor_data = []
    if len(api_data) != 0:
        for i in range(len(api_data)):
            api = api_data[i]["sensorAPI"]
            if len(api) != 0:
                response = requests.get(api)
                sensor_data.append(response.json())

        return jsonify(sensor_data)
    return "No data"

@app.route('/sensors/sensor_id/<sensor_id>')
def sensors_by_sensor_id(sensor_id=None):
    api_data = []
    cur = mysql.connect().cursor()
    cur.execute("SELECT sensorAPI FROM userdata WHERE sensorID = %s", sensor_id)
    api_data = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    api = api_data[0]["sensorAPI"]
    response = requests.get(api)
    bin_data = response.json()
    return jsonify(bin_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

