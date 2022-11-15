from flask import Flask, render_template, send_from_directory, url_for, request, redirect
import requests
import os

from forms import SelectSensor
from forms import TempSensorV1
from forms import LightSensorV1
from forms import PresenceSensorV1

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'qH1vprMjavek52cv7Lmfe1FoCexrrV8egFnB21jHhkuOHm8hJUe1hwn7pKEZQ1fioUzDb3sWcNK1pJVVIhyrgvFiIrceXpKJBFIn_i9-LTLBCc4cqaI3gjJJHU6kxuT8bnC7Nq'
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
    form = SelectSensor(request.form)
    if request.method == "POST" and form.validate():
        if form.sensor_id.data >= 0 and form.sensor_id.data < 10:
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
        return redirect(url_for('index'))

    return render_template('send_data_light_v1.html', form=form, error=error)

@app.route('/send_data_presence_v1/<id>', methods=['GET', 'POST'])
def send_data_presence_v1(id):
    error = None
    form = PresenceSensorV1()
    form.sensor_id.data = id
    if request.method == "POST" and form.validate():
        return redirect(url_for('index'))

    return render_template('send_data_presence_v1.html', form=form, error=error)


@app.route('/send_data_temp_v1/<id>', methods=['GET', 'POST'])
def send_data_temp_v1(id):
    error = None
    form = TempSensorV1()
    form.sensor_id.data = id
    if request.method == "POST" and form.validate():
        return redirect(url_for('index'))
        # print(requests.Request('POST', 'http://localhost:8080/rest/uploadVideo',
        #                        files=files).prepare().body.decode('utf-8'))
        #REST_SERVER = os.environ.get('REST_SERVER', 'localhost')
        #response = requests.post('http://'+REST_SERVER+':8080/Service/uploadVideo',
        #                         files=files)
        #if response.status_code == 200:
        #    error = "Video uploaded successfully"
        #else:
        #    error = response.text

    return render_template('send_data_temp_v1.html', form=form, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
