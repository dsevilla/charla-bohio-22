from flask_wtf import FlaskForm
from wtforms import (StringField, SelectField, IntegerField, BooleanField)
from wtforms.validators import DataRequired, Length
import random

sensor_choices = [(0, '0'),
                  (1, '1'),
                  (2, '2'),
                  (3, '3'),
                  (4, '4'),
                  (5, '5'),
                  (6, '6'),
                  (7, '7'),
                  (8, '8'),
                  (9, '9'),
                  (10, '10'),
                  (11, '11'),
                  (12, '12'),
                  (13, '13'),
                  (14, '14'),
                  (15, '15'),
                  (16, '16'),
                  (17, '17'),
                  (18, '18'),
                  (19, '19'),
                  (20, '20'),
                  (21, '21'),
                  (22, '22'),
                  (23, '23'),
                  (24, '24'),
                  (25, '25'),
                  (26, '26'),
                  (27, '27'),
                  (28, '28'),
                  (29, '29')
                  ]
random.shuffle(sensor_choices)

class SelectSensor(FlaskForm):
    sensor_id = SelectField(u'Sensor ID', 
                            choices=sensor_choices,
                            validators=[DataRequired()],
                            coerce=int)

class TempSensorV1(FlaskForm):
    sensor_id = StringField(u'Id', validators=[DataRequired()])
    temp = IntegerField(u'Temp', validators=[DataRequired()], default=25)
    humidity = IntegerField(u'Humidity', validators=[DataRequired()], default=40)

class LightSensorV1(FlaskForm):
    sensor_id = StringField(u'Id', validators=[DataRequired()])
    light_level = IntegerField(u'Light Level', validators=[DataRequired()], default=80)


class PresenceSensorV1(FlaskForm):
    sensor_id = StringField(u'Id', validators=[DataRequired()])
    presence = BooleanField(u'Person detected', validators=[DataRequired()], default=False)

