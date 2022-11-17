from flask import Flask, render_template, send_from_directory, url_for, request, redirect
import requests
import os
import pymongo
import codecs
import datetime
from pymongo import MongoClient
import redis
import pprint

from forms import SelectSensor
from forms import TempSensorV1
from forms import LightSensorV1
from forms import PresenceSensorV1

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'qH1vprMjavek52cv7Lmfe1FoCexrrV8egFnB21jHhkuOHm8hJUe1hwn7pKEZQ1fioUzDb3sWcNK1pJVVIhyrgvFiIrceXpKJBFIn_i9-LTLBCc4cqaI3gjJJHU6kxuT8bnC7Nq'

passw = codecs.encode('ObuvbPbagebyf22', 'rot_13')
client = MongoClient("mongodb://root:%s@mongo" % (passw), 27017)

# readings database
db = client.bohiocontrols
readings = db.readings
r = redis.Redis(host='redis', port=6379, db=0)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Icon!
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    form = SelectSensor()
    if request.method == "POST":
        if form.sensor_id.data < 10:
            return redirect(url_for('send_data_temp_v1',
                                    id=str(form.sensor_id.data)))
        if form.sensor_id.data >= 10 and form.sensor_id.data < 20:
            return redirect(url_for('send_data_light_v1',
                                    id=str(form.sensor_id.data)))
        if form.sensor_id.data >= 20 and form.sensor_id.data < 30:
            return redirect(url_for('send_data_presence_v1',
                                    id=str(form.sensor_id.data)))

    return render_template('index.html', form=form)

@app.route('/send_data_light_v1/<id>', methods=['GET', 'POST'])
def send_data_light_v1(id):
    error = None
    form = LightSensorV1()
    form.sensor_id.data = id
    if request.method == "POST" and form.validate():
        sensor_data = {
            "sensor_id" : id,
            "timestamp" : int(datetime.datetime.timestamp(datetime.datetime.now())*1000),
            "type" : "light_sensor_v1",
            "light_level": form.light_level.data
        }
        readings.insert_one(sensor_data);
        r.set("sensor_id_%d" % (id), pprint.pformat(sensor_data,indent=2))
 
        return redirect(url_for('index'))

    return render_template('send_data_light_v1.html', form=form, error=error)

@app.route('/send_data_presence_v1/<id>', methods=['GET', 'POST'])
def send_data_presence_v1(id):
    error = None
    form = PresenceSensorV1()
    form.sensor_id.data = id
    if request.method == "POST" and form.validate():
        sensor_data = {
            "sensor_id" : id,
            "timestamp" : int(datetime.datetime.timestamp(datetime.datetime.now())*1000),
            "type" : "presence_v1",
            "person_detected": form.presence.data
        }
        readings.insert_one(sensor_data)
        r.set("sensor_id_%d" % (id), pprint.pformat(sensor_data,indent=2))
                 
        return redirect(url_for('index'))

    return render_template('send_data_presence_v1.html', form=form, error=error)


@app.route('/send_data_temp_v1/<id>', methods=['GET', 'POST'])
def send_data_temp_v1(id):
    error = None
    form = TempSensorV1()
    form.sensor_id.data = id
    if request.method == "POST" and form.validate():
        sensor_data = {
            "sensor_id" : id,
            "timestamp" : int(datetime.datetime.timestamp(datetime.datetime.now())*1000),
            "type" : "temp/humidity_v1",
            "temp" : form.temp.data,
            "humidity": form.humidity.data
        }
        readings.insert_one(sensor_data)
        r.set("sensor_id_%d" % (id), pprint.pformat(sensor_data,indent=2))
        return redirect(url_for('index'))

    return render_template('send_data_temp_v1.html', form=form, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
