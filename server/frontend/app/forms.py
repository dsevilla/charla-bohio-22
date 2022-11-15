from flask_wtf import FlaskForm
from wtforms import (StringField, SelectField)
from wtforms.validators import DataRequired, Length

class SelectSensor(FlaskForm):
    sensor_id = SelectField(u'Sensor ID', 
                            choices=[(1, '1'), (2, '2'), (3, '3')],
                            validators=[DataRequired()],
                            coerce=int)

class TempSensorV1(FlaskForm):
    sensor_id = StringField(u'Id', validators=[DataRequired()])

