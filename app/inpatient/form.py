from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from .model import InPatientTableSet, InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTimeAndBed

class InPatientFromLogin(FlaskForm):
    patientid = StringField('身份证', validators=[
        DataRequired(), Length(16, 18), Regexp('^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')
    ])
    